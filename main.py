from fastapi import FastAPI
from app.database import init_db
from app.routers import node, vertex, algorithm, data

app = FastAPI(
    title="Family Graph API",
    description="API for managing family relationships and running graph algorithms",
    version="1.0.0",
)

# Initialize the database on startup
@app.on_event("startup")
async def startup():
    init_db()

# Include all routers
app.include_router(node.router)
app.include_router(vertex.router)
app.include_router(algorithm.router)
app.include_router(data.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Family Graph API",
        "documentation": "/docs",
    }