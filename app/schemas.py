from pydantic import BaseModel, ConfigDict


class EntityBase(BaseModel):
    userDocument: str
    creditCardToken: str
    value: int


class EntityCreate(EntityBase):
    pass


class EntityUpdate(EntityBase):
    pass


class EntityRead(EntityBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
