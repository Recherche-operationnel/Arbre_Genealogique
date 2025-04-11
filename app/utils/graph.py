from app.models.node import Node
from app.models.vertex import Vertex
from collections import defaultdict
from sqlalchemy.orm import Session

class Graph:
    def __init__(self):
        self.nodes = {}  # id -> Node object
        self.edges = defaultdict(list)  # node_id -> [(node_id, weight)]
        
    @classmethod
    def load_from_db(cls, db: Session):
        graph = cls()
        
        # Load nodes
        db_nodes = db.query(Node).all()
        for node in db_nodes:
            graph.nodes[node.id] = node
        
        # Load edges (vertices)
        db_vertices = db.query(Vertex).all()
        for vertex in db_vertices:
            # Treat each vertex as an edge in both directions with weight=1
            # This creates an undirected graph
            graph.edges[vertex.parent_id].append((vertex.child_id, 1))
            graph.edges[vertex.child_id].append((vertex.parent_id, 1))
            
        return graph
