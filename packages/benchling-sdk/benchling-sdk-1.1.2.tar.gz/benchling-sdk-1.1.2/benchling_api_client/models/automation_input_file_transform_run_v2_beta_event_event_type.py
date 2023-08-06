from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AutomationInputFileTransformRunV2BetaEventEventType(Enums.KnownString):
    V2_BETAAUTOMATIONINPUTFILETRANSFORMRUN = "v2-beta.automationInputFileTransform.run"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AutomationInputFileTransformRunV2BetaEventEventType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AutomationInputFileTransformRunV2BetaEventEventType must be a string (encountered: {val})"
            )
        newcls = Enum("AutomationInputFileTransformRunV2BetaEventEventType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AutomationInputFileTransformRunV2BetaEventEventType, getattr(newcls, "_UNKNOWN"))
