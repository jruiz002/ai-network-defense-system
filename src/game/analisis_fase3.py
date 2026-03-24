import random
import time
from typing import Callable
import matplotlib.pyplot as plt

from src.game.game_state import GameState, MAX_PLAYER
from src.solvers.minimax import minimax_alpha_beta
from src.solvers.expectiminimax import expectiminimax

def agent_random(state: GameState) -> str:
    """Retorna una acción aleatoria válida."""
    actions = state.get_actions(state.current_turn)
    if not actions:
        return None
    return random.choice(actions)

def agent_minimax(state: GameState, depth: int) -> str:
    """Retorna la mejor acción según Minimax Alpha-Beta (asume determinismo)."""
    counter = [0]
    _, action = minimax_alpha_beta(state, depth, state.current_turn, counter)
    return action

def agent_expectiminimax(state: GameState, depth: int) -> str:
    """Retorna la mejor acción según Expectiminimax (considera incertidumbre)."""
    counter = [0]
    _, action = expectiminimax(state, depth, state.current_turn, counter)
    return action

def simulate_stochastic_game(
    state: GameState, 
    max_agent_func: Callable[[GameState], str],
    min_agent_func: Callable[[GameState], str],
    failure_prob: float = 0.2,
    verbose: bool = True
) -> int:
    """
    Simula una partida con incertidumbre (probabilidad de fallo en la acción).
    Retorna el score final desde la perspectiva de MAX.
    """
    current_state = state
    turn = 0
    
    if verbose:
        print(f"\nIniciando simulación estocástica (Fallo={failure_prob*100}%)")
        print(f"MAX Agent: {max_agent_func.__name__}")
        print(f"MIN Agent: {min_agent_func.__name__}")

    while not current_state.is_terminal():
        turn += 1
        player = current_state.current_turn
        
        # Selección de Agente
        if player == MAX_PLAYER:
            action = max_agent_func(current_state)
        else:
            action = min_agent_func(current_state)

        if verbose:
            print(f"-- Turno {turn} [{player}] --")
            print(f"  Estado actual (MAX: {len(current_state.max_nodes)}, MIN: {len(current_state.min_nodes)})")
        
        if action is None:
            if verbose: print(f"  No hay acciones disponibles. Pasa turno.")
            current_state = current_state.pass_turn()
            continue

        # Simulación de Incertidumbre
        if random.random() < failure_prob:
            if verbose: print(f"  Intento de capturar {action}... ¡FALLÓ! (Pierde turno)")
            current_state = current_state.pass_turn()
        else:
            if verbose: print(f"  Intento de capturar {action}... ¡ÉXITO!")
            current_state = current_state.apply_action(action, player)
            
    final_score = current_state.score()
    if verbose:
        print("Iteminalizado el juego.")
        print(f"Score Final: {final_score}")
    
    return final_score

def run_phase3_analysis(initial_state: GameState, n_games: int = 10, depth: int = 3):
    print("\n=========================================================")
    print(" TASK 3: ANÁLISIS COMPARATIVO (INCERTIDUMBRE Y LATENCIA)")
    print("=========================================================")

    # 1. Minimax vs Random
    print(f"\n--- Experimento A: Minimax (Tradicional) vs Random ---")
    scores_minimax = []
    wins_minimax = 0
    t_start = time.time()
    for i in range(n_games):
        # Clonar estado inicial si es necesario o asumir inmutabilidad/reinicio
        # GameState es inmutable en su estructura básica, pero 'simular' avanza sobre estados nuevos.
        # Usamos el initial_state base.
        print(f"  Juego {i+1}/{n_games}...", end="\r")
        score = simulate_stochastic_game(
            initial_state, 
            lambda s: agent_minimax(s, depth), 
            agent_random, 
            verbose=False
        )
        scores_minimax.append(score)
        if score > 0: wins_minimax += 1
    t_minimax = time.time() - t_start
    avg_minimax = sum(scores_minimax) / len(scores_minimax)
    print(f"  Resultados Minimax: Promedio Score={avg_minimax:.2f}, WinRate={wins_minimax/n_games:.2%}, Tiempo={t_minimax:.2f}s")


    # 2. Expectiminimax vs Random
    print(f"\n--- Experimento B: Expectiminimax (Consciente del Riesgo) vs Random ---")
    scores_expecti = []
    wins_expecti = 0
    t_start = time.time()
    for i in range(n_games):
        print(f"  Juego {i+1}/{n_games}...", end="\r")
        score = simulate_stochastic_game(
            initial_state, 
            lambda s: agent_expectiminimax(s, depth), 
            agent_random, 
            verbose=False
        )
        scores_expecti.append(score)
        if score > 0: wins_expecti += 1
    t_expecti = time.time() - t_start
    avg_expecti = sum(scores_expecti) / len(scores_expecti)
    print(f"  Resultados Expectiminimax: Promedio Score={avg_expecti:.2f}, WinRate={wins_expecti/n_games:.2%}, Tiempo={t_expecti:.2f}s")

    # Comparación
    print("\n--- Conclusiones Preliminares ---")
    print(f"Diferencia de Score Promedio: {avg_expecti - avg_minimax:.2f}")
    
    # Gráfica simple
    labels = ['Minimax', 'Expectiminimax']
    avgs = [avg_minimax, avg_expecti]
    plt.bar(labels, avgs, color=['blue', 'green'])
    plt.title('Score Promedio en Entorno Estocástico (vs Random)')
    plt.ylabel('Score Final (MAX - MIN)')
    plt.savefig('comparacion_fase3.png')
    print("Gráfica guardada en 'comparacion_fase3.png'")
