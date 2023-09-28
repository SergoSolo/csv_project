from pydantic import BaseModel


class DocumentSchemaDB(BaseModel):
    id: int
    name: str
    columns: list[str]
    size: int

    class Config:
        orm_mode = True
