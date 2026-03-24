
from typing import Set
from src.game.game_state import GameState, MAX_PLAYER, MIN_PLAYER


def _frontera(owned_nodes: Set[str], free_nodes: Set[str], graph) -> Set[str]:

    frontera = set()
    for node in owned_nodes:
        for neighbor in graph.get_neighbors(node):
            if neighbor in free_nodes:
                frontera.add(neighbor)
    return frontera


def evaluar(state: GameState) -> float:
    # ── Componente 1: Valor acumulado (ya capturado) ────────────────
    V = (
        sum(state.node_values[n] for n in state.max_nodes)
        - sum(state.node_values[n] for n in state.min_nodes)
    )

    # ── Componente 2: Valor en la frontera de expansión ─────────────
    frontera_max = _frontera(state.max_nodes, state.free_nodes, state.graph)
    frontera_min = _frontera(state.min_nodes, state.free_nodes, state.graph)

    M = (
        sum(state.node_values[n] for n in frontera_max)
        - sum(state.node_values[n] for n in frontera_min)
    )

    # ── Componente 3: Movilidad (número de opciones) ─────────────────
    F = len(frontera_max) - len(frontera_min)

    # ── Combinación lineal ponderada ─────────────────────────────────
    return 0.5 * V + 0.35 * M + 0.15 * F


def explicar_eval(state: GameState):
    frontera_max = _frontera(state.max_nodes, state.free_nodes, state.graph)
    frontera_min = _frontera(state.min_nodes, state.free_nodes, state.graph)

    V = (
        sum(state.node_values[n] for n in state.max_nodes)
        - sum(state.node_values[n] for n in state.min_nodes)
    )
    M = (
        sum(state.node_values[n] for n in frontera_max)
        - sum(state.node_values[n] for n in frontera_min)
    )
    F = len(frontera_max) - len(frontera_min)
    total = 0.5 * V + 0.35 * M + 0.15 * F

    print("  ┌─────────────────────────────────────────┐")
    print("  │        DESGLOSE DE Eval(s)              │")
    print("  ├─────────────────────────────────────────┤")
    print(f"  │  V(s) = valor acumulado       = {V:>+6.1f}  │")
    print(f"  │  M(s) = valor en frontera     = {M:>+6.1f}  │")
    print(f"  │  F(s) = movilidad (# nodos)   = {F:>+6.1f}  │")
    print("  ├─────────────────────────────────────────┤")
    print(f"  │  Eval = 0.5({V:+.0f}) + 0.35({M:+.0f}) + 0.15({F:+.0f})│")
    print(f"  │  Eval(s) = {total:>+8.3f}                    │")
    print("  └─────────────────────────────────────────┘")