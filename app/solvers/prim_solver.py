
import heapq
from app.utils.graph import Graph
from solver import Solver


class PrimSolver(Solver):
    initialGraph: Graph
    def solve(self):
        if not self.initialGraph.nodes:
            return {"error": "The Graph is empty"}

        start_node_id = next(iter(self.initialGraph.nodes.keys()))
        nodes_visited = {start_node_id}
        edges = [(weight, start_node_id, neighbor) for neighbor, weight in self.initialGraph.edges[start_node_id]]
        heapq.heapify(edges)
        edges_traversed = []
        total_weight = 0

        while len(nodes_visited) < len(self.initialGraph.nodes):
            weight, u, v = heapq.heappop(edges)

            if v in nodes_visited:
                continue

            nodes_visited.add(v)
            edges_traversed.append({"from": u, "to": v, "weight": weight})
            total_weight += weight

            for neighbor, edge_weight in self.initialGraph.edges[v]:
                if neighbor not in nodes_visited:
                    heapq.heappush(edges, (edge_weight, v, neighbor))
        

        return {
            "algorithm": "Prim",
            "mst_edges": edges_traversed,
            "total_weight": total_weight
        }
