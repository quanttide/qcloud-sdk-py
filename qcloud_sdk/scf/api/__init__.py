"""
云函数API
"""

from .base import ScfBaseAPIMixin
from .functions import ScfFunctionAPIMixin, ScfFunctionCustomAPIMixin
from .triggers import ScfTriggerAPIMixin


class ScfAPIMixin(
    ScfBaseAPIMixin,
    ScfFunctionAPIMixin,
    ScfFunctionCustomAPIMixin,
    ScfTriggerAPIMixin,
):
    """
    云函数API
    """
    pass
