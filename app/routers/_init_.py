"""
FastAPI routers for API endpoints.
"""

from app.routers.node import router as node_router
from app.routers.vertex import router as vertex_router
from app.routers.algorithm import router as algorithm_router
from app.routers.data import router as data_router

__all__ = ["node_router", "vertex_router", "algorithm_router", "data_router"]