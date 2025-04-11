from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.database import get_db
from app.services.solver_service import SolverService

router = APIRouter(prefix="/algorithms", tags=["algorithms"])

@router.get("/dijkstra/{start_node_id}/{end_node_id}")
def solve_dijkstra(start_node_id: int, end_node_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    result = SolverService.solve_dijkstra(db, start_node_id, end_node_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/bellman-ford/{start_node_id}/{end_node_id}")
def solve_bellman_ford(start_node_id: int, end_node_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    result = SolverService.solve_bellman_ford(db, start_node_id, end_node_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/prim")
def solve_prim(db: Session = Depends(get_db)) -> Dict[str, Any]:
    result = SolverService.solve_prim(db)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/kruskal")
def solve_kruskal(db: Session = Depends(get_db)) -> Dict[str, Any]:
    result = SolverService.solve_kruskal(db)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/dfs/{start_node_id}")
def solve_dfs(start_node_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    result = SolverService.solve_dfs(db, start_node_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/bfs/{start_node_id}")
def solve_bfs(start_node_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    result = SolverService.solve_bfs(db, start_node_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result