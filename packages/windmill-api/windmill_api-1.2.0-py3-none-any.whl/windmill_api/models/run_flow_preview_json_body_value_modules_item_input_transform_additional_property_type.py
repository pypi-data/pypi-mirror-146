from enum import Enum


class RunFlowPreviewJsonBodyValueModulesItemInputTransformAdditionalPropertyType(str, Enum):
    STATIC = "static"
    OUTPUT = "output"

    def __str__(self) -> str:
        return str(self.value)
