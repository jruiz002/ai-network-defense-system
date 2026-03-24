import random
from typing import Dict, List, Tuple

class Graph:
    def __init__(self, num_nodes: int, edge_probability: float = 0.3):
        self.num_nodes = num_nodes
        self.nodes = [f"Server_{i}" for i in range(num_nodes)]
        self.adjacency_list: Dict[str, List[str]] = {node: [] for node in self.nodes}
        self.edges: List[Tuple[str, str]] = []
        
        self._generate_random_edges(edge_probability)
        
    def _generate_random_edges(self, edge_probability: float):
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                if random.random() < edge_probability:
                    self.add_edge(self.nodes[i], self.nodes[j])
                    
    def add_edge(self, node1: str, node2: str):
        if node1 in self.adjacency_list and node2 in self.adjacency_list:
            self.adjacency_list[node1].append(node2)
            self.adjacency_list[node2].append(node1)
            self.edges.append((node1, node2))

    def get_neighbors(self, node: str) -> List[str]:
        return self.adjacency_list.get(node, [])

    def __str__(self):
        return f"Grafo con {self.num_nodes} nodos y {len(self.edges)} aristas"
