from enum import Enum


class DeleteCompletedJobResponse200RawFlowFailureModuleInputTransformAdditionalPropertyType(str, Enum):
    STATIC = "static"
    OUTPUT = "output"

    def __str__(self) -> str:
        return str(self.value)
