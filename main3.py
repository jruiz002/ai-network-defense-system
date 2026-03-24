import sys
import os

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.game.game_state import crear_juego
from src.game.analisis_fase3 import run_phase3_analysis

def main():
    print("=========================================================")
    print(" TASK 3 — INCERTIDUMBRE Y LATENCIA (EXPECTIMINIMAX)")
    print("=========================================================\n")

    # 1. Setup Environment
    print("Configurando entorno (Semilla 42)...")
    # Using specific seed for reproducibility
    state = crear_juego(seed=42, num_nodes=20, max_turns=30)
    
    print("\nEstado Inicial:")
    print(f"  Nodos Totales: {len(state.graph.nodes)}")
    print(f"  Max (Defensa) inicia en: {state.max_nodes}")
    print(f"  Min (Hacker) inicia en: {state.min_nodes}")
    print(f"  Valores de Nodos (Muestra): {list(state.node_values.items())[:5]}...")

    # 2. Run Comparative Analysis    
    DEPTH = 2  # Keeping it low for speed in demonstration
    GAMES = 20 # Number of games for statistical significance
    
    print(f"\nEjecutando simulación con Profundidad={DEPTH} y {GAMES} partidas por agente...")
    run_phase3_analysis(state, n_games=GAMES, depth=DEPTH)

    print("\n=========================================================")
    print(" FIN DE LA TASK 3")
    print("=========================================================")

if __name__ == "__main__":
    main()
