from fastapi import Depends
from app.database import get_db
import csv
from pathlib import Path
from sqlalchemy.orm import Session
from app.models.node import Node
from app.models.vertex import Vertex
from app.models.spouse import Spouse
from typing import Dict, Any

class DataLoader:
    @staticmethod
    def load_from_json(db: Session, json_data: Dict[str, Any]):
        """Load data from a JSON object"""
        # Process nodes
        nodes_map = {}  # To keep track of node ids
        
        if "nodes" in json_data:
            for node_data in json_data["nodes"]:
                node = Node(
                    name=node_data["name"],
                    surname=node_data["surname"],
                    avatar=node_data.get("avatar"),
                    birthday=node_data.get("birthday"),
                    sex=node_data.get("sex")
                )
                db.add(node)
                db.flush()  # To get the ID
                nodes_map[node_data.get("id", len(nodes_map) + 1)] = node.id
        
        # Process vertices
        if "vertices" in json_data:
            for vertex_data in json_data["vertices"]:
                parent_id = nodes_map.get(vertex_data["parent_id"])
                child_id = nodes_map.get(vertex_data["child_id"])
                
                if parent_id and child_id:
                    vertex_id = f"v_{parent_id}_{child_id}_{vertex_data['rank']}"
                    vertex = Vertex(
                        id=vertex_id,
                        rank=vertex_data["rank"],
                        parent_id=parent_id,
                        child_id=child_id
                    )
                    db.add(vertex)
        
        # Process spouses
        if "spouses" in json_data:
            for spouse_data in json_data["spouses"]:
                node1_id = nodes_map.get(spouse_data["node1_id"])
                node2_id = nodes_map.get(spouse_data["node2_id"])
                
                if node1_id and node2_id:
                    spouse = Spouse(
                        node1_id=node1_id,
                        node2_id=node2_id
                    )
                    db.add(spouse)
        
        db.commit()
    
    @staticmethod
    def load_from_csv(db: Session, nodes_path: Path, vertices_path: Path, spouses_path: Path = None):
        """Load data from CSV files"""
        nodes_map = {}  # To keep track of node ids
        
        # Load nodes from CSV
        if nodes_path.exists():
            with open(nodes_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Convert sex field to boolean if present
                    sex_value = None
                    if "sex" in row:
                        sex_value = row["sex"].lower() in ("true", "1", "t", "yes")
                    
                    node = Node(
                        name=row["name"],
                        surname=row["surname"],
                        avatar=row.get("avatar"),
                        birthday=row.get("birthday"),
                        sex=sex_value
                    )
                    db.add(node)
                    db.flush()  # To get the ID
                    nodes_map[int(row.get("id", len(nodes_map) + 1))] = node.id
        
        # Load vertices from CSV
        if vertices_path.exists():
            with open(vertices_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    parent_id = nodes_map.get(int(row["parent_id"]))
                    child_id = nodes_map.get(int(row["child_id"]))
                    
                    if parent_id and child_id:
                        rank = int(row["rank"])
                        vertex_id = f"v_{parent_id}_{child_id}_{rank}"
                        
                        vertex = Vertex(
                            id=vertex_id,
                            rank=rank,
                            parent_id=parent_id,
                            child_id=child_id
                        )
                        db.add(vertex)
        
        # Load spouses from CSV
        if spouses_path and spouses_path.exists():
            with open(spouses_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    node1_id = nodes_map.get(int(row["node1_id"]))
                    node2_id = nodes_map.get(int(row["node2_id"]))
                    
                    if node1_id and node2_id:
                        spouse = Spouse(
                            node1_id=node1_id,
                            node2_id=node2_id
                        )
                        db.add(spouse)
        
        db.commit()