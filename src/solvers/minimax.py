"""
minimax.py
----------
Implementación de Minimax puro y Minimax con Poda Alfa-Beta.

ALGORITMO MINIMAX
------------------
El árbol de juego alterna entre nodos MAX y MIN:

    MINIMAX(s, profundidad, jugador):
        si TERMINAL(s) o profundidad == 0:
            retornar Eval(s)          ← heurística si no es terminal

        si jugador == MAX:
            v = -∞
            para cada acción a en ACCIONES(s, MAX):
                v = max(v, MINIMAX(aplica(s,a), prof-1, MIN))
            retornar v

        si jugador == MIN:
            v = +∞
            para cada acción a en ACCIONES(s, MIN):
                v = min(v, MINIMAX(aplica(s,a), prof-1, MAX))
            retornar v

PODA ALFA-BETA
--------------
Agrega dos parámetros al recorrido:
  α = mejor valor que MAX puede garantizar en el camino actual (inicia -∞)
  β = mejor valor que MIN puede garantizar en el camino actual (inicia +∞)

Reglas de poda:
  En nodo MAX: si v ≥ β → podar (MIN nunca elegirá este camino)
               actualizar α = max(α, v)
  En nodo MIN: si v ≤ α → podar (MAX nunca elegirá este camino)
               actualizar β = min(β, v)

La poda NO altera el valor óptimo, solo evita expandir ramas irrelevantes.
En el mejor caso reduce O(b^d) a O(b^(d/2)).
"""

import math
from src.game.game_state import GameState, MAX_PLAYER, MIN_PLAYER
from src.game.eval import evaluar


def minimax(state: GameState, depth: int, player: str, counter: list) -> tuple:

    counter[0] += 1   # contar este nodo expandido

    # ── Caso base: terminal o profundidad agotada ───────────────────
    if state.is_terminal() or depth == 0:
        return evaluar(state), None

    actions = state.get_actions(player)

    # Si no hay acciones disponibles, pasar turno al oponente
    if not actions:
        next_state = state.pass_turn()
        return minimax(next_state, depth - 1, next_state.current_turn, counter)

    best_action = None

    if player == MAX_PLAYER:
        # MAX busca el valor más alto
        best_value = -math.inf
        for action in actions:
            new_state = state.apply_action(action, MAX_PLAYER)
            value, _ = minimax(new_state, depth - 1, MIN_PLAYER, counter)
            if value > best_value:
                best_value = value
                best_action = action
        return best_value, best_action

    else:
        # MIN busca el valor más bajo
        best_value = math.inf
        for action in actions:
            new_state = state.apply_action(action, MIN_PLAYER)
            value, _ = minimax(new_state, depth - 1, MAX_PLAYER, counter)
            if value < best_value:
                best_value = value
                best_action = action
        return best_value, best_action


def minimax_alpha_beta(
    state: GameState,
    depth: int,
    player: str,
    counter: list,
    alpha: float = -math.inf,
    beta: float = math.inf,
) -> tuple:
    counter[0] += 1

    # ── Caso base ───────────────────────────────────────────────────
    if state.is_terminal() or depth == 0:
        return evaluar(state), None

    actions = state.get_actions(player)

    if not actions:
        next_state = state.pass_turn()
        return minimax_alpha_beta(
            next_state,
            depth - 1,
            next_state.current_turn,
            counter,
            alpha,
            beta,
        )

    best_action = None

    if player == MAX_PLAYER:
        best_value = -math.inf
        for action in actions:
            new_state = state.apply_action(action, MAX_PLAYER)
            value, _ = minimax_alpha_beta(new_state, depth - 1, MIN_PLAYER,
                                           counter, alpha, beta)
            if value > best_value:
                best_value = value
                best_action = action

            alpha = max(alpha, best_value)
            if best_value >= beta:
                # ✂ PODA BETA: MIN nunca elegiría este camino
                break

        return best_value, best_action

    else:
        best_value = math.inf
        for action in actions:
            new_state = state.apply_action(action, MIN_PLAYER)
            value, _ = minimax_alpha_beta(new_state, depth - 1, MAX_PLAYER,
                                           counter, alpha, beta)
            if value < best_value:
                best_value = value
                best_action = action

            beta = min(beta, best_value)
            if best_value <= alpha:
                # ✂ PODA ALFA: MAX nunca elegiría este camino
                break

        return best_value, best_action


def agente_max(state: GameState, depth: int = 4, usar_poda: bool = True) -> tuple:

    counter = [0]

    if usar_poda:
        _, action = minimax_alpha_beta(state, depth, MAX_PLAYER, counter)
    else:
        _, action = minimax(state, depth, MAX_PLAYER, counter)

    return action, counter[0]


def agente_min_aleatorio(state: GameState) -> str | None:
    import random
    actions = state.get_actions(MIN_PLAYER)
    return random.choice(actions) if actions else None