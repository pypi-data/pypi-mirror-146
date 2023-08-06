# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os
from urllib.parse import urlparse

from contrast import AGENT_CURR_WORKING_DIR

from contrast.agent.framework import Framework, Server
from contrast.agent.heartbeat import Heartbeat
from contrast.agent.protect.mixins.REP_settings import SettingsREPMixin
from contrast.agent.reaction_processor import ReactionProcessor
from contrast.api.settings_pb2 import (
    AccumulatorSettings as DtmAccumulatorSettings,
    AgentSettings as DtmAgentSettings,
    ApplicationSettings as DtmApplicationSettings,
    ServerFeatures as DtmServerFeatures,
)
from contrast.configuration import AgentConfig
from contrast.utils.decorators import cached_property, fail_safely
from contrast.utils.loggers.logger import reset_agent_logger
from contrast.utils.singleton import Singleton
from contrast.utils.string_utils import truncate
from contrast.utils.timer import now_ms
from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


class ServerFeatures:
    def __init__(self, features):
        self.features = features or {}

    @cached_property
    def log_file(self):
        return self.features.get("features", {}).get("logFile", "")

    @cached_property
    def log_level(self):
        return self.features.get("features", {}).get("logLevel", "")

    @cached_property
    def assess_enabled(self):
        return (
            self.features.get("features", {})
            .get("assessment", {})
            .get("enabled", False)
        )

    @cached_property
    def protect_enabled(self):
        return self.features.get("features", {}).get("defend", {}).get("enabled", False)


class Settings(Singleton, SettingsREPMixin):
    def init(self, app_name=None):
        """
        Agent settings for the entire lifetime of the agent.

        Singletons should override init, not __init__.
        """
        self.config = None
        self.config_features = {}
        self.last_update = None
        self.last_update_time_ms = 0
        self.heartbeat = None
        self.framework = Framework()
        self.server = Server()
        self.sys_module_count = 0
        self.rewriter_enabled = False

        # Features and Settings from Service
        self.server_features = DtmServerFeatures()

        self.application_settings = DtmApplicationSettings()
        self.accumulator_settings = DtmAccumulatorSettings()

        # Server
        self.server_name = None
        self.server_path = None
        self.server_type = None

        self.exclusion_matchers = []

        # Rules
        self.protect_rules = dict()

        # circular import
        from contrast.agent.assess.rules.response.autocomplete_missing_rule import (
            AutocompleteMissingRule,
        )
        from contrast.agent.assess.rules.response.cache_controls_rule import (
            CacheControlsRule,
        )

        self.assess_response_rules = [
            AutocompleteMissingRule(),
            CacheControlsRule(),
        ]

        # Initialize config
        self.config = AgentConfig()

        if self.config.is_service_bypassed:
            self.direct_teamserver_server_features = ServerFeatures(None)

        self.disabled_assess_rules = set(
            self.config.get("assess.rules.disabled_rules", [])
        )

        # Initialize application metadata
        self.app_name = self.get_app_name(app_name)

        self.agent_runtime_window = now_ms()

        logger.info("Contrast Agent finished loading settings.")

    def _is_defend_enabled_in_server_features(self):
        if self.config.is_service_bypassed:
            return self.direct_teamserver_server_features.protect_enabled
        return (
            self.server_features
            and self.server_features.defend
            and self.server_features.defend.enabled
        )

    @cached_property
    def is_proxy_enabled(self):
        return self.config.get("api.proxy.enable")

    @cached_property
    def proxy_url(self):
        return self.config.get("api.proxy.url")

    @cached_property
    def proxy_scheme(self):
        scheme = urlparse(self.proxy_url).scheme or "http"
        return scheme

    @cached_property
    def is_cert_verification_enabled(self):
        return self.config.get("api.certificate.enable")

    @cached_property
    def ca_file(self):
        return self.config.get("api.certificate.ca_file")

    @cached_property
    def client_cert_file(self):
        return self.config.get("api.certificate.cert_file")

    @cached_property
    def client_private_key(self):
        return self.config.get("api.certificate.key_file")

    @cached_property
    def api_service_key(self):
        return self.config.get("api.service_key")

    @cached_property
    def api_url(self):
        return self.config.get("api.url")

    @cached_property
    def api_key(self):
        return self.config.get("api.api_key")

    @cached_property
    def api_user_name(self):
        return self.config.get("api.user_name")

    def is_agent_config_enabled(self):
        return self.config.get("enable", True)

    @cached_property
    def is_profiler_enabled(self):
        return self.config.get("agent.python.enable_profiler")

    @cached_property
    def max_sources(self):
        return self.config.get("assess.max_context_source_events")

    @cached_property
    def max_propagation(self):
        return self.config.get("assess.max_propagation_events")

    @cached_property
    def max_vulnerability_count(self):
        """Max number of vulnerabilities per rule type to report for one
        agent run `time_limit_threshold` time period"""
        return self.config.get("assess.max_rule_reported")

    @cached_property
    def agent_runtime_threshold(self):
        return self.config.get("assess.time_limit_threshold")

    @cached_property
    def is_bundled_enabled(self):
        """The default across agents is to use the bundled service by default"""
        return self.config.get("agent.service.enable", True)

    @cached_property
    def app_path(self):
        return self.config.get("application.path")

    @cached_property
    def app_version(self):
        return self.config.get("application.version")

    @property
    def pid(self):
        """
        pid is used by Speedracer to recognize a unique worker process for an application.

        pid must be unique for each worker process of an app.
        :return: int current process id
        """
        return os.getpid()

    def get_app_name(self, app_name):
        if self.config.get("application.name"):
            return self.config.get("application.name")

        return app_name if app_name else "root"

    def establish_heartbeat(self):
        """
        Initialize Heartbeat between Agent and SR if it has not been already initialized.
        """
        if self.heartbeat is None:
            self.heartbeat = Heartbeat(self)
            self.heartbeat.start()

    def process_responses(self, responses):
        """
        :param responses: list of Message responses from SR
        """
        self.establish_heartbeat()

        logger.debug("Processing %s responses", len(responses))

        for response in responses:
            if self.process_service_response(response):
                self.set_protect_rules()

    def process_service_response(self, data):
        reload_rules = False

        if data and isinstance(data, DtmAgentSettings):
            self.last_update = data.sent_ms

            reload_rules = self.process_server_features(data) or reload_rules
            reload_rules = self.process_application_settings(data) or reload_rules
            reload_rules = self.process_accumulator_settings(data) or reload_rules

        if reload_rules:
            logger.debug(
                "Finished processing Contrast Service message and reloading rules."
            )

        return reload_rules

    def apply_ts_server_settings(self, response_body):
        self.direct_teamserver_server_features = ServerFeatures(response_body)
        self.last_update_time_ms = now_ms() - self.last_update_time_ms

        self.update_logger_from_features()

        self.log_server_features(self.direct_teamserver_server_features)

        self.set_protect_rules()

    def process_server_features(self, data):
        if not data.HasField("server_features"):
            return False

        self.server_features = data.server_features
        self.update_logger_from_features()

        self.log_server_features(data.server_features)

        return True

    def log_server_features(self, server_features):
        """
        Record server features received from teamserver (via the contrast service)
        Remove the rule_definitions field before logging because it's long and ugly
        """
        if self.config.is_service_bypassed and isinstance(
            server_features, ServerFeatures
        ):
            logger.debug(
                "Received updated server features logFile=%s logLevel=%s Protect=%s Assess=%s",
                server_features.log_file,
                server_features.log_level,
                server_features.protect_enabled,
                server_features.assess_enabled,
            )
        else:
            server_features_copy = DtmServerFeatures()
            server_features_copy.CopyFrom(server_features)
            del server_features_copy.defend.rule_definitions[:]
            logger.debug(
                "Received updated server features (excluding rule_definitions from"
                " log):\n%s",
                server_features_copy,
            )

    @property
    def code_exclusion_matchers(self):
        return [x for x in self.exclusion_matchers if x.is_code]

    def process_application_settings(self, data):
        if not data.HasField("application_settings"):
            return False

        self.application_settings = data.application_settings

        ReactionProcessor.process(data.application_settings, self)

        self.reset_transformed_settings()

        logger.debug(
            "Received updated application settings:\n%s", data.application_settings
        )

        return True

    def reset_transformed_settings(self):
        self.exclusion_matchers = []

    def process_accumulator_settings(self, data):
        if data.HasField("accumulator_settings"):
            self.accumulator_settings = data.accumulator_settings

    def update_logger_from_features(self):
        if self.config.is_service_bypassed:
            logger_reset = reset_agent_logger(
                self.direct_teamserver_server_features.log_file,
                self.direct_teamserver_server_features.log_level,
            )
        else:
            logger_reset = reset_agent_logger(
                self.server_features.log_file, self.server_features.log_level
            )

        if logger_reset:
            self.config.log_config()

    def is_inventory_enabled(self):
        """
        inventory.enable = false: Disables both route coverage and library analysis and reporting
        """
        return self.config.get("inventory.enable", True)

    def is_analyze_libs_enabled(self):
        """
        inventory.analyze_libraries = false: Disables only library analysis/reporting
        """
        return (
            self.config is not None
            and self.config.get("inventory.analyze_libraries", True)
            and self.is_inventory_enabled()
        )

    def is_assess_enabled(self):
        """
        We do not allow assess and defend to be on at the same time. As defend
        is arguably the more important of the two, it will take precedence

        The agent config may enable assess even if it is turned off in TS. This
        allows unlicensed apps to send findings to TS, where they will appear
        as obfuscated results.
        """

        # https://contrast.atlassian.net/browse/PROD-530
        if self.config is None:
            return False

        assess_enabled = self.config.get("assess.enable", None)
        if assess_enabled is not None:
            return assess_enabled

        if self.config.is_service_bypassed:
            return self.direct_teamserver_server_features.assess_enabled
        return (
            self.server_features
            and self.server_features.assess
            and self.server_features.assess.enabled
        )

    def is_protect_enabled(self):
        """
        Protect is enabled only if both configuration and server features enable it.
        """
        if self.config is None:
            return False
        config_protect_enabled = self.config.get("protect.enable", None)
        if config_protect_enabled is not None:
            return config_protect_enabled

        return self._is_defend_enabled_in_server_features()

    def set_protect_rules(self):
        if not self._is_defend_enabled_in_server_features():
            self.protect_rules = dict()
            return

        from contrast.agent.protect.rule.rules_builder import build_protect_rules

        self.protect_rules = build_protect_rules()

    def get_server_name(self):
        """
        Hostname of the server

        Default is socket.gethostname() or localhost
        """
        if self.server_name is None:
            self.server_name = self.config.get("server.name")

        return self.server_name

    def get_server_path(self):
        """
        Working Directory of the server

        Default is root
        """
        if self.server_path is None:
            self.server_path = self.config.get("server.path") or truncate(
                AGENT_CURR_WORKING_DIR
            )

        return self.server_path

    def get_server_type(self):
        """
        Web Framework of the Application either defined in common config or via discovery.
        """
        if self.server_type is None:
            self.server_type = (
                self.config.get("server.type") or self.framework.name_lower
            )

        return self.server_type

    @property
    def response_scanning_enabled(self):
        return self.is_assess_enabled() and self.config.get(
            "assess.enable_scan_response"
        )

    def is_assess_rule_disabled(self, rule_id):
        """
        Rules disabled in config override all disabled rules from TS per common config
        """
        return (
            rule_id in self.disabled_assess_rules
            if self.disabled_assess_rules
            else rule_id in self.application_settings.disabled_assess_rules
        )

    def enabled_response_rules(self):
        return [
            rule
            for rule in self.assess_response_rules
            if not self.is_assess_rule_disabled(rule.name)
        ]

    def is_collect_stacktraces_all(self):
        return (
            self.config is not None and self.config.get("assess.stacktraces") == "ALL"
        )

    def is_collect_stacktraces_some(self):
        return (
            self.config is not None and self.config.get("assess.stacktraces") == "SOME"
        )

    def is_collect_stacktraces_none(self):
        return (
            self.config is not None and self.config.get("assess.stacktraces") == "NONE"
        )

    def build_proxy_url(self):
        if self.proxy_url:
            return {self.proxy_scheme: self.proxy_url}

        return {}

    @fail_safely("Unable to ignore request", return_value=False)
    def ignore_request(self, path):
        """
        Determine if the given path exactly matches any of the
        configured url_exclusion_patterns.

        :param path: path for current request
        :return: bool whether the path matches any url_exclusion patterns
        """
        patterns = self.config.get("agent.python.url_exclusion_patterns")
        if not patterns:
            return False

        for pattern in patterns:
            if pattern.fullmatch(path):
                logger.debug("Path %s matched on pattern %s", path, pattern)
                return True
        return False
