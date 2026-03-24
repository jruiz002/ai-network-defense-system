from typing import Dict, Optional, Callable, List, TypeVar, Generic, Tuple
from core.csp import CSP

V = TypeVar('V')
D = TypeVar('D')

VariableSelectionStrategy = Callable[[CSP[V, D], Dict[V, D]], V]

InferenceStrategy = Callable[[CSP[V, D], V, D, Dict[V, D]], Tuple[bool, Dict[V, List[D]]]]


def select_unassigned_variable_first(csp: CSP[V, D], assignment: Dict[V, D]) -> V:
    for variable in csp.variables:
        if variable not in assignment:
            return variable
    raise Exception("No unassigned variables remaining")

def select_unassigned_variable_mrv(csp: CSP[V, D], assignment: Dict[V, D]) -> V:
    unassigned = [v for v in csp.variables if v not in assignment]
    return min(unassigned, key=lambda v: len(csp.domains[v]))

def no_inference(csp: CSP[V, D], var: V, value: D, assignment: Dict[V, D]) -> Tuple[bool, Dict[V, List[D]]]:
    return True, {}

def forward_checking(csp: CSP[V, D], var: V, value: D, assignment: Dict[V, D]) -> Tuple[bool, Dict[V, List[D]]]:
    pruned: Dict[V, List[D]] = {}
    
    # Check all constraints that involve the newly assigned variable `var`
    for constraint in csp.constraints[var]:
        # We find which variables are affected (neighbors)
        for neighbor in constraint.variables:
            if neighbor != var and neighbor not in assignment:
                # If the value we just assigned to `var` is still in the neighbor's domain, remove it
                if value in csp.domains[neighbor]:
                    csp.domains[neighbor].remove(value)
                    
                    # Track what we pruned to restore later
                    if neighbor not in pruned:
                        pruned[neighbor] = []
                    pruned[neighbor].append(value)
                    
                    # Lookahead: If neighbor has no remaining values, failure!
                    if len(csp.domains[neighbor]) == 0:
                        return False, pruned 
                        
    return True, pruned


class BacktrackingSolver(Generic[V, D]):
    def __init__(self, 
                 csp: CSP[V, D], 
                 select_unassigned_variable: VariableSelectionStrategy[V, D] = select_unassigned_variable_first,
                 inference: InferenceStrategy[V, D] = no_inference):
        self.csp = csp
        self.select_variable = select_unassigned_variable
        self.inference = inference
        self.assignments_attempted = 0
        
    def solve(self, assignment: Optional[Dict[V, D]] = None) -> Optional[Dict[V, D]]:
        if assignment is None:
            assignment = {}
            
        # Base case: if assignment is complete, return it
        if len(assignment) == len(self.csp.variables):
            return assignment

        # Select an unassigned variable using the current strategy
        var = self.select_variable(self.csp, assignment)
        
        # Make a copy of the available values because inference might modify domains
        available_values = list(self.csp.domains[var])
        
        for value in available_values:
            # Check if the value is consistent with the current assignment
            if self.csp.consistent(var, {**assignment, var: value}):
                
                # 1. Assign value
                assignment[var] = value
                self.assignments_attempted += 1
                
                # 2. Run Inference (Forward Checking)
                success, pruned = self.inference(self.csp, var, value, assignment)
                
                if success:
                    # 3. Proceed Recursively
                    result = self.solve(assignment)
                    if result is not None:
                        return result
                        
                # Backtracking: Restore pruned domains
                for p_var, p_vals in pruned.items():
                    self.csp.domains[p_var].extend(p_vals)
                
                # Backtracking: Unassign value
                del assignment[var]
        
        return None
