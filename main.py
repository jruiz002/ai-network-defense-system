import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import time
from network.graph import Graph
from network.security_csp import create_network_security_csp
from solvers.backtracking import (
    BacktrackingSolver,
    select_unassigned_variable_first,
    select_unassigned_variable_mrv,
    no_inference,
    forward_checking
)

def run_experiment():
    print("=========================================================")
    print(" Sistema de Defensa de Red con IA - Task 1: Configuración CSP ")
    print("=========================================================\n")
    
    # 1. Generate the network
    print("Generando red de 20 servidores...")
    graph = Graph(num_nodes=20, edge_probability=0.3)
    print(f"Generado: {graph}")
    print("---------------------------------------------------------")
    
    protocols = ["Rojo", "Verde", "Azul", "Amarillo"]
    print("Protocolos Disponibles:", protocols)
    
    csp_pure = create_network_security_csp(graph, protocols)
    csp_opt = create_network_security_csp(graph, protocols)

    # 2. Pure Backtracking
    print("\n--- Ejecutando Backtracking Puro ---")
    solver_pure = BacktrackingSolver(
        csp=csp_pure,
        select_unassigned_variable=select_unassigned_variable_first,
        inference=no_inference
    )
    
    start_time = time.perf_counter()
    solution_pure = solver_pure.solve()
    end_time = time.perf_counter()
    
    time_pure = end_time - start_time
    assignments_pure = solver_pure.assignments_attempted
    
    if solution_pure is not None:
        print("-> ¡Backtracking Puro encontró una solución!")
    else:
        print("-> ¡Backtracking Puro NO pudo encontrar una solución!")
        
    print(f"Tiempo Tomado:                {time_pure:.6f} segundos")
    print(f"Sub-asignaciones intentadas:  {assignments_pure}")

    # 3. Optimized Backtracking (FC + MRV)
    print("\n--- Ejecutando Backtracking Optimizado (Forward Checking + MRV) ---")
    solver_opt = BacktrackingSolver(
        csp=csp_opt,
        select_unassigned_variable=select_unassigned_variable_mrv,
        inference=forward_checking
    )
    
    start_time = time.perf_counter()
    solution_opt = solver_opt.solve()
    end_time = time.perf_counter()
    
    time_opt = end_time - start_time
    assignments_opt = solver_opt.assignments_attempted
    
    if solution_opt is not None:
        print("-> ¡Backtracking Optimizado encontró una solución!")
    else:
        print("-> ¡Backtracking Optimizado NO pudo encontrar una solución!")
        
    print(f"Tiempo Tomado:                {time_opt:.6f} segundos")
    print(f"Sub-asignaciones intentadas:  {assignments_opt}")

    
    # 4. Analysis
    print("\n=========================================================")
    print(" ANÁLISIS DE RENDIMIENTO ")
    print("=========================================================")
    if time_opt > 0:
        speedup = time_pure / time_opt
        print(f"Aceleración: El enfoque optimizado fue {speedup:.2f}x más rápido.")
    
    if assignments_pure > 0:
        reduction = (assignments_pure - assignments_opt) / assignments_pure * 100
        print(f"Eficiencia de Asignaciones: Intentó {reduction:.2f}% menos asignaciones.")
        
    if solution_opt is not None:
        print("\nVerificando restricciones de la solución...")
        valid = True
        for s1, s2 in graph.edges:
            if solution_opt[s1] == solution_opt[s2]:
                print(f"ERROR: {s1} y {s2} están conectados y ambos tienen el protocolo {solution_opt[s1]}")
                valid = False
        if valid:
            print("ÉXITO: La configuración de la solución optimizada es perfectamente segura.")

if __name__ == "__main__":
    sys.setrecursionlimit(2000)
    run_experiment()
