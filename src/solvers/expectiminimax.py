import math
from src.game.game_state import GameState, MAX_PLAYER, MIN_PLAYER
from src.game.eval import evaluar

def expectiminimax(state: GameState, depth: int, player: str, counter: list = None) -> tuple:
    """
    Algoritmo Expectiminimax que modela la incertidumbre (20% de fallo).
    Retorna (valor_esperado, mejor_accion).
    """
    if counter is None:
        counter = [0]
    
    counter[0] += 1

    # Casos base
    if state.is_terminal() or depth == 0:
        return evaluar(state), None

    actions = state.get_actions(player)
    
    # Si no hay acciones, pasar turno
    if not actions:
        next_state = state.pass_turn()
        return expectiminimax(next_state, depth - 1, next_state.current_turn, counter)

    best_action = None

    if player == MAX_PLAYER:
        best_value = -math.inf
        for action in actions:
            # Calcular valor esperado del nodo de azar
            # 80% éxito: nodo capturado
            state_success = state.apply_action(action, MAX_PLAYER)
            val_success, _ = expectiminimax(state_success, depth - 1, MIN_PLAYER, counter)
            
            # 20% fallo: se pierde el turno sin capturar
            state_fail = state.pass_turn()
            val_fail, _ = expectiminimax(state_fail, depth - 1, MIN_PLAYER, counter)
            
            expected_value = 0.8 * val_success + 0.2 * val_fail

            if expected_value > best_value:
                best_value = expected_value
                best_action = action
        return best_value, best_action

    else:
        best_value = math.inf
        for action in actions:
            # Calcular valor esperado del nodo de azar
            # 80% éxito: nodo capturado
            state_success = state.apply_action(action, MIN_PLAYER)
            val_success, _ = expectiminimax(state_success, depth - 1, MAX_PLAYER, counter)
            
            # 20% fallo: se pierde el turno sin capturar
            state_fail = state.pass_turn()
            val_fail, _ = expectiminimax(state_fail, depth - 1, MAX_PLAYER, counter)
            
            expected_value = 0.8 * val_success + 0.2 * val_fail

            if expected_value < best_value:
                best_value = expected_value
                best_action = action
        return best_value, best_action
