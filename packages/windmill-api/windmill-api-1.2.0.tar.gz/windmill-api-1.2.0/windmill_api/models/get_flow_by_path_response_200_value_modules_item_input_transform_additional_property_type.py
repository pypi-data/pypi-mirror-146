from enum import Enum


class GetFlowByPathResponse200ValueModulesItemInputTransformAdditionalPropertyType(str, Enum):
    STATIC = "static"
    OUTPUT = "output"

    def __str__(self) -> str:
        return str(self.value)
