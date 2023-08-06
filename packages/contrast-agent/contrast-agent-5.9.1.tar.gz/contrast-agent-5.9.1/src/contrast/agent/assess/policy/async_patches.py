# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import contrast

from contrast.agent.assess.policy.analysis import analyze
from contrast.utils.patch_utils import add_watermark


def build_assess_async_method(original_method, patch_policy):
    """
    Build a generic async method which instruments original_method.

    :param original_method: method to call for result
    :param patch_policy: PatchLocationPolicy containing all policy nodes for this patch
    :return: Newly created async patch function
    """

    async def assess_method(*args, **kwargs):
        context = contrast.CS__CONTEXT_TRACKER.current()
        result = None

        try:
            result = await original_method(*args, **kwargs)
        finally:
            analyze(context, patch_policy, result, args, kwargs)

        return result

    return add_watermark(assess_method)
