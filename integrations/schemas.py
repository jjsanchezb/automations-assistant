from pydantic import BaseModel


class IntegrationSchema(BaseModel):
    id: str | None
    key: str | None
    version: int | None
    name: str | None
    description: str | None
    is_active: bool | None
    source_code: str | None
    runtime: str | None


class IntegrationActionSchema(BaseModel):
    id: str | None
    key: str | None
    integration: str | None
    name: str | None
    description: str | None
    is_active: bool | None
    entrypoint_function: str | None
    input_schema: dict | None
    output_schema: dict | None


class IntegrationTriggerSchema(BaseModel):
    id: str | None
    key: str | None
    integration: str | None
    name: str | None
    description: str | None
    is_active: bool | None
    entrypoint_function: str | None
    input_schema: dict | None
    output_schema: dict | None
