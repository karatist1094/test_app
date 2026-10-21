from pydantic import BaseModel, ConfigDict


class CategoryReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str

class CategoryCreateUpdateSchema(BaseModel):
    name: str
