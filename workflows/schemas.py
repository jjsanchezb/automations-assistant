from typing import Literal, Union

from pydantic import BaseModel

from integrations.schemas import IntegrationActionSchema, IntegrationSchema, IntegrationTriggerSchema


class Edge(BaseModel):
    source: str
    target: str


class ActionStepSchema(BaseModel):
    id: str
    type: Literal["ACTION"] = "ACTION"
    action: IntegrationActionSchema
    inputs: dict = {}


class ConditionStepSchema(BaseModel):
    id: str
    type: Literal["CONDITION"] = "CONDITION"
    expression: str


WorkflowStep = Union[ActionStepSchema, ConditionStepSchema]


class WorkflowDefinition(BaseModel):
    integration: IntegrationSchema
    trigger: IntegrationTriggerSchema
    steps: list[WorkflowStep]
    edges: list[Edge]
