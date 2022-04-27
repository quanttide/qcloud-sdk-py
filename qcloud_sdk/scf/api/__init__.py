"""
云函数API
"""

from .base import ScfBaseAPIMixin
from .functions import ScfFunctionMixin
from .triggers import ScfTriggerAPIMixin


class ScfAPIMixin(
    ScfBaseAPIMixin,
    ScfFunctionMixin,
    ScfTriggerAPIMixin,
):
    """
    云函数API
    """
    pass
