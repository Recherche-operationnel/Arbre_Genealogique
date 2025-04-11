from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class NodeBase(BaseModel):
    name: str
    surname: str
    avatar: Optional[str] = None
    birthday: Optional[str] = None
    sex: Optional[bool] = None

class NodeCreate(NodeBase):
    pass

class NodeUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    avatar: Optional[str] = None
    birthday: Optional[str] = None
    sex: Optional[bool] = None

class Node(NodeBase):
    id: int

    class Config:
        orm_mode = True

class VertexBase(BaseModel):
    id: str
    rank: int
    
    class Config:
        orm_mode = True

class NodeDetail(Node):
    parents: List[Dict[str, Any]] = []
    children: List[Dict[str, Any]] = []
    spouses: List[Dict[str, Any]] = []

    class Config:
        orm_mode = True