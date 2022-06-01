"""
云函数API
"""

from .base import ScfBaseAPIMixin
from .functions import ScfFunctionAPIMixin, ScfFunctionIntegratedAPIMixin
from .triggers import ScfTriggerAPIMixin


class ScfAPIMixin(
    ScfBaseAPIMixin,
    ScfFunctionAPIMixin,
    ScfFunctionIntegratedAPIMixin,
    ScfTriggerAPIMixin,
):
    """
    云函数API
    """
    pass
