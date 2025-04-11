from fastapi import Depends, APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from app.database import get_db
from sqlalchemy.orm import Session
import tempfile
from pathlib import Path
from app.utils.data_loader import DataLoader
from typing import Optional

router = APIRouter(prefix="/data", tags=["data"])


class JsonData(BaseModel):
    data: dict


@router.post("/load-json")
async def load_from_json(data: JsonData, db: Session = Depends(get_db)):
    try:
        DataLoader.load_from_json(db, data.data)
        return {"message": "Data loaded successfully from JSON"}
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error loading data: {str(e)}")


@router.post("/load-csv")
async def load_from_csv(
    nodes: UploadFile = File(...),
    vertices: UploadFile = File(...),
    spouses: Optional[UploadFile] = File(None)
):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded files temporarily
            nodes_path = Path(temp_dir) / "nodes.csv"
            with open(nodes_path, "wb") as f:
                f.write(await nodes.read())

            vertices_path = Path(temp_dir) / "vertices.csv"
            with open(vertices_path, "wb") as f:
                f.write(await vertices.read())

            spouses_path = None
            if spouses:
                spouses_path = Path(temp_dir) / "spouses.csv"
                with open(spouses_path, "wb") as f:
                    f.write(await spouses.read())

            # Load data from CSV files
            DataLoader.load_from_csv(nodes_path, vertices_path, spouses_path)

        return {"message": "Data loaded successfully from CSV files"}
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error loading data: {str(e)}")
