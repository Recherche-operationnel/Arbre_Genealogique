from sqlalchemy.orm import Session
from app.models.node import Node
from app.models.vertex import Vertex
from typing import Dict, Any, List, Optional
from collections import defaultdict, deque
import heapq

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

class SolverService:
    @staticmethod
    def solve_dijkstra(db: Session, start_node_id: int, end_node_id: int) -> Dict[str, Any]:
        # Load graph from database
        graph = Graph.load_from_db(db)
        
        if start_node_id not in graph.nodes or end_node_id not in graph.nodes:
            return {"error": "Start or end node not found"}
        
        # Initialize distances with infinity for all nodes except the start node
        distances = {node_id: float('infinity') for node_id in graph.nodes}
        distances[start_node_id] = 0
        
        # Priority queue for Dijkstra's algorithm
        pq = [(0, start_node_id)]
        
        # To reconstruct the path
        previous = {node_id: None for node_id in graph.nodes}
        
        # Dijkstra's algorithm
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            # If we reached the end node
            if current_node == end_node_id:
                break
                
            # Skip if we already found a better path
            if current_distance > distances[current_node]:
                continue
                
            # Check all neighbors
            for neighbor, weight in graph.edges[current_node]:
                distance = current_distance + weight
                
                # If we found a better path
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))
        
        # Reconstruct path
        path = []
        current = end_node_id
        
        while current is not None:
            path.append(current)
            current = previous[current]
            
        path.reverse()
        
        # If there's no path
        if path[0] != start_node_id:
            return {
                "algorithm": "Dijkstra",
                "start_node": start_node_id,
                "end_node": end_node_id,
                "path": [],
                "distance": float('infinity')
            }
            
        return {
            "algorithm": "Dijkstra",
            "start_node": start_node_id,
            "end_node": end_node_id,
            "path": path,
            "distance": distances[end_node_id]
        }

    @staticmethod
    def solve_bellman_ford(db: Session, start_node_id: int, end_node_id: int) -> Dict[str, Any]:
        graph = Graph.load_from_db(db)
        
        if start_node_id not in graph.nodes or end_node_id not in graph.nodes:
            return {"error": "Start or end node not found"}
        
        # Initialize distances with infinity for all nodes except the start node
        distances = {node_id: float('infinity') for node_id in graph.nodes}
        distances[start_node_id] = 0
        
        # To reconstruct the path
        previous = {node_id: None for node_id in graph.nodes}
        
        # Collect all edges for Bellman-Ford
        edges = []
        for u in graph.edges:
            for v, weight in graph.edges[u]:
                edges.append((u, v, weight))
        
        # Bellman-Ford algorithm
        for _ in range(len(graph.nodes) - 1):
            for u, v, weight in edges:
                if distances[u] != float('infinity') and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    previous[v] = u
        
        # Check for negative weight cycles
        for u, v, weight in edges:
            if distances[u] != float('infinity') and distances[u] + weight < distances[v]:
                return {"error": "Graph contains a negative weight cycle"}
        
        # Reconstruct path
        path = []
        current = end_node_id
        
        while current is not None:
            path.append(current)
            current = previous[current]
            
        path.reverse()
        
        # If there's no path
        if path[0] != start_node_id:
            return {
                "algorithm": "Bellman-Ford",
                "start_node": start_node_id,
                "end_node": end_node_id,
                "path": [],
                "distance": float('infinity')
            }
            
        return {
            "algorithm": "Bellman-Ford",
            "start_node": start_node_id,
            "end_node": end_node_id,
            "path": path,
            "distance": distances[end_node_id]
        }

    @staticmethod
    def solve_prim(db: Session) -> Dict[str, Any]:
        graph = Graph.load_from_db(db)
        
        if not graph.nodes:
            return {"error": "No nodes in the graph"}
            
        # Start with the first node
        start_node_id = next(iter(graph.nodes.keys()))
        
        # Set of visited nodes
        visited = {start_node_id}
        
        # Priority queue for edges
        edges = [(weight, start_node_id, neighbor) 
                for neighbor, weight in graph.edges[start_node_id]]
        heapq.heapify(edges)
        
        # MST edges and total weight
        mst_edges = []
        total_weight = 0
        
        # Prim's algorithm
        while edges and len(visited) < len(graph.nodes):
            weight, u, v = heapq.heappop(edges)
            
            if v in visited:
                continue
                
            visited.add(v)
            mst_edges.append({"from": u, "to": v, "weight": weight})
            total_weight += weight
            
            # Add all edges from v to the priority queue
            for neighbor, edge_weight in graph.edges[v]:
                if neighbor not in visited:
                    heapq.heappush(edges, (edge_weight, v, neighbor))
        
        return {
            "algorithm": "Prim",
            "mst_edges": mst_edges,
            "total_weight": total_weight
        }

    @staticmethod
    def solve_kruskal(db: Session) -> Dict[str, Any]:
        graph = Graph.load_from_db(db)
        
        if not graph.nodes:
            return {"error": "No nodes in the graph"}
            
        # Collect all edges
        edges = []
        for u in graph.edges:
            for v, weight in graph.edges[u]:
                if u < v:  # To avoid duplicate edges
                    edges.append((weight, u, v))
        
        # Sort edges by weight
        edges.sort()
        
        # Union-Find data structure
        parent = {node_id: node_id for node_id in graph.nodes}
        rank = {node_id: 0 for node_id in graph.nodes}
        
        def find(node_id):
            if parent[node_id] != node_id:
                parent[node_id] = find(parent[node_id])
            return parent[node_id]
            
        def union(u, v):
            root_u = find(u)
            root_v = find(v)
            
            if root_u == root_v:
                return
                
            if rank[root_u] < rank[root_v]:
                parent[root_u] = root_v
            else:
                parent[root_v] = root_u
                if rank[root_u] == rank[root_v]:
                    rank[root_u] += 1
        
        # MST edges and total weight
        mst_edges = []
        total_weight = 0
        
        # Kruskal's algorithm
        for weight, u, v in edges:
            if find(u) != find(v):
                union(u, v)
                mst_edges.append({"from": u, "to": v, "weight": weight})
                total_weight += weight
        
        return {
            "algorithm": "Kruskal",
            "mst_edges": mst_edges,
            "total_weight": total_weight
        }

    @staticmethod
    def solve_dfs(db: Session, start_node_id: int) -> Dict[str, Any]:
        graph = Graph.load_from_db(db)
        
        if start_node_id not in graph.nodes:
            return {"error": "Start node not found"}
            
        # DFS traversal
        visited = set()
        traversal_order = []
        
        def dfs(node_id):
            visited.add(node_id)
            traversal_order.append(node_id)
            
            for neighbor, _ in graph.edges[node_id]:
                if neighbor not in visited:
                    dfs(neighbor)
        
        dfs(start_node_id)
        
        return {
            "algorithm": "DFS",
            "start_node": start_node_id,
            "traversal_order": traversal_order
        }

    @staticmethod
    def solve_bfs(db: Session, start_node_id: int) -> Dict[str, Any]:
        graph = Graph.load_from_db(db)
        
        if start_node_id not in graph.nodes:
            return {"error": "Start node not found"}
            
        # BFS traversal
        visited = {start_node_id}
        queue = deque([start_node_id])
        traversal_order = []
        
        while queue:
            node_id = queue.popleft()
            traversal_order.append(node_id)
            
            for neighbor, _ in graph.edges[node_id]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return {
            "algorithm": "BFS",
            "start_node": start_node_id,
            "traversal_order": traversal_order
        }