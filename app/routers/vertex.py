from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.vertex import VertexCreate, VertexUpdate, Vertex
from app.services.vertex_service import VertexService

router = APIRouter(prefix="/vertices", tags=["vertices"])

@router.post("/", response_model=Vertex)
def create_vertex(vertex: VertexCreate, db: Session = Depends(get_db)):
    db_vertex = VertexService.create_vertex(db, vertex)
    if not db_vertex:
        raise HTTPException(
            status_code=400, 
            detail="Could not create vertex. Check that parent and child nodes exist and the rank constraint is satisfied."
        )
    return db_vertex

@router.get("/", response_model=List[Vertex])
def get_all_vertices(db: Session = Depends(get_db)):
    return VertexService.get_all_vertices(db)

@router.get("/{vertex_id}", response_model=Vertex)
def get_vertex(vertex_id: str, db: Session = Depends(get_db)):
    vertex = VertexService.get_vertex(db, vertex_id)
    if vertex is None:
        raise HTTPException(status_code=404, detail=f"Vertex with ID {vertex_id} not found")
    return vertex

@router.put("/{vertex_id}", response_model=Vertex)
def update_vertex(vertex_id: str, vertex: VertexUpdate, db: Session = Depends(get_db)):
    updated_vertex = VertexService.update_vertex(db, vertex_id, vertex)
    if not updated_vertex:
        raise HTTPException(
            status_code=400, 
            detail="Update failed. Check that the rank constraint is satisfied."
        )
    return updated_vertex

@router.delete("/{vertex_id}")
def delete_vertex(vertex_id: str, db: Session = Depends(get_db)):
    deleted = VertexService.delete_vertex(db, vertex_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Vertex with ID {vertex_id} not found")
    return {"message": f"Vertex with ID {vertex_id} deleted successfully"}