from src.game.game_state import crear_juego
from src.game.eval import explicar_eval
from src.game.analisis import (
  comparar_nodos_expandidos,
  graficar_nodos_expandidos,
  simular_partida,
)

D_MAX = 4


def main():
    print("  TASK 2 — DEFENSA ADVERSARIAL (MINIMAX + ALFA-BETA)")

    state = crear_juego(seed=42, num_nodes=20, max_turns=30)

    print("\n- Función de evaluación heurística Eval(s):")
    print("  Eval(s) = 0.5·V(s) + 0.35·M(s) + 0.15·F(s)")
    print()
    explicar_eval(state)

    nodos_puro, nodos_ab, _ = comparar_nodos_expandidos(state, depth=D_MAX)

    graficar_nodos_expandidos(nodos_puro, nodos_ab, depth=D_MAX)

    simular_partida(state, depth=D_MAX, usar_poda=True, verbose=True)


if __name__ == "__main__":
    main()