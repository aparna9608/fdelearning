from pydantic import BaseModel, ConfigDict, Field


class CustomerCreate(BaseModel):
    name: str = Field(min_length=1)
    role: str = Field(min_length=1)


class CustomerResponse(BaseModel):
    id: int
    name: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class CustomerUpdate(BaseModel):
    name: str
    role: str

class CustomerPatch(BaseModel):
    name: str | None = None
    role: str | None = None        



















        