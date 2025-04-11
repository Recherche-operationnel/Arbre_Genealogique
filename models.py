from typing import List, Union
from pathlib import Path
from abc import ABC, abstractmethod


class Node:
    id: int
    name: str
    surname: str
    avatar: str
    birthday: str
    sex: bool

    parent_in: List[Union['Vertex', int]],
    child_in: List[Union['Vertex', int]],
    spouses_in: List[Vertex]
    # on peut rajouter autre chose si on veut


class Vertex:
    id: str
    rank: int

    parent: Union[Node, int]  # parent
    child: Union[Node, int]  # enfant

# Contraintes: - le nombre max de parents de rank k pour un noeud est de 2^k

class Graph:
    nodes: List[Node]
    vertices: List[Vertex]

class UseCases:
    def create_node(self, node: Node):
        pass

    def update_node(self, id: int, name: str, surname: str...):
        pass

    def delete_node(self, id: int):
        node: Node = Node(id)
        for relation in node.relationships:
            self.deleteVertex(relation)
        pass

    def create_vertex(self, rank: int, parent: Node, child: Node):
        return Vertex(7, rank, parent, child)

    def delete_vertex(self, id: int):
        pass

    def updateVertex(self, id: int, rank: int, parent: int = None, child: int = None):
        pass

    
    def loadFromJson(self, json: object):
        pass

    def load_from_csv(self, nodes_path: Path, vertices_path: Path, spouses_path: Path):
        pass
    

class Solver(ABC):
    
    @abstractmethod
    def solve(self):
        pass

class DijkstraSolver(Solver):
    startNode: Node
    endNode: Node
    def solve(self):
        return super().solve()
    

class BellmanFordSolver(Solver):
    startNode: Node
    endNode: Node
    def solve(self):
        return super().solve()
    
class PrimSolver(Solver):
    initialGraph: Graph
    def solve(self):
        return super().solve()

class KruskalSolver(Solver):
    initialGraph: Graph
    def solve(self):
        return super().solve()

class DepthFirstSearchSolver(Solver):
    initialGraph: Graph
    def solve(self):
        return super().solve()

class BreadthFirstSearchSolver(Solver):
    initialGraph: Graph
    def solve(self):
        return super().solve()
