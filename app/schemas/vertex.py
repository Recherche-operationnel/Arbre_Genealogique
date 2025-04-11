from pydantic import BaseModel
from typing import Optional

class VertexBase(BaseModel):
    rank: int
    parent_id: int
    child_id: int

class VertexCreate(VertexBase):
    pass

class VertexUpdate(BaseModel):
    rank: Optional[int] = None
    parent_id: Optional[int] = None
    child_id: Optional[int] = None

class Vertex(VertexBase):
    id: str

    class Config:
        orm_mode = True