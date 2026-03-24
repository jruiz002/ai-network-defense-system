from typing import Dict, List
from core.csp import Constraint, CSP
from network.graph import Graph

class NotEqualConstraint(Constraint[str, str]):
    def __init__(self, server1: str, server2: str):
        super().__init__([server1, server2])
        self.server1 = server1
        self.server2 = server2

    def satisfied(self, assignment: Dict[str, str]) -> bool:
        # If either variable is not yet assigned, the constraint is not yet violated
        if self.server1 not in assignment or self.server2 not in assignment:
            return True
        # If both are assigned, they must not be equal
        return assignment[self.server1] != assignment[self.server2]


def create_network_security_csp(graph: Graph, protocols: List[str]) -> CSP[str, str]:
    variables = graph.nodes
    # Every server can initially be assigned any of the protocols
    domains = {server: list(protocols) for server in variables}
    
    csp = CSP(variables, domains)
    
    # Add a constraint for every connected pair of servers (edge)
    for server1, server2 in graph.edges:
        csp.add_constraint(NotEqualConstraint(server1, server2))
        
    return csp
