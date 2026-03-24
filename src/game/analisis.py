import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from src.game.game_state import GameState, MAX_PLAYER, MIN_PLAYER
from src.solvers.minimax import (
    agente_max,
    agente_min_aleatorio,
    minimax,
    minimax_alpha_beta,
)
import math


# ═══════════════════════════════════════════════════════════════════
#  COMPARACIÓN: NODOS EXPANDIDOS
# ═══════════════════════════════════════════════════════════════════

def comparar_nodos_expandidos(state: GameState, depth: int = 4):
    print()
    print("=" * 55)
    print("  COMPARACIÓN: NODOS EXPANDIDOS EN EL ÁRBOL")
    print(f"  (profundidad d_max = {depth})")
    print("=" * 55)

    # Minimax puro
    counter_puro = [0]
    val_puro, accion_puro = minimax(state, depth, MAX_PLAYER, counter_puro)

    # Minimax con Alfa-Beta
    counter_ab = [0]
    val_ab, accion_ab = minimax_alpha_beta(state, depth, MAX_PLAYER, counter_ab,
                                            -math.inf, math.inf)

    nodos_puro = counter_puro[0]
    nodos_ab   = counter_ab[0]
    reduccion  = (1 - nodos_ab / nodos_puro) * 100 if nodos_puro > 0 else 0

    print(f"  {'Algoritmo':<30} {'Nodos expandidos':>18} {'Acción elegida':>15}")
    print("-" * 55)
    print(f"  {'Minimax Puro':<30} {nodos_puro:>18,} {str(accion_puro):>15}")
    print(f"  {'Minimax + Poda Alfa-Beta':<30} {nodos_ab:>18,} {str(accion_ab):>15}")
    print("-" * 55)
    print(f"  Reducción de nodos : {reduccion:.1f}%")
    print(f"  Misma decisión     : {'✓ Sí' if accion_puro == accion_ab else '✗ No (revisar)'}")
    print("=" * 55)

    # Verificación importante: la poda no debe cambiar la decisión
    if accion_puro != accion_ab:
        print("  [AVISO] Las acciones difieren — puede haber empates en valor.")

    return nodos_puro, nodos_ab, accion_ab


def graficar_nodos_expandidos(nodos_puro: int, nodos_ab: int, depth: int = 4):
    etiquetas = ['Minimax\nPuro', 'Minimax +\nAlfa-Beta']
    valores   = [nodos_puro, nodos_ab]
    colores   = ['#e74c3c', '#2ecc71']

    fig, ax = plt.subplots(figsize=(7, 5))
    barras = ax.bar(etiquetas, valores, color=colores, edgecolor='black', width=0.45)
    ax.set_title(f'Nodos Expandidos en el Árbol de Juego\n(d_max = {depth})',
                 fontsize=13, fontweight='bold')
    ax.set_ylabel('Cantidad de nodos expandidos')
    ax.set_ylim(0, max(valores) * 1.22)

    for barra, val in zip(barras, valores):
        ax.text(barra.get_x() + barra.get_width() / 2,
                barra.get_height() + max(valores) * 0.02,
                f'{val:,}', ha='center', va='bottom', fontweight='bold')

    reduccion = (1 - nodos_ab / nodos_puro) * 100 if nodos_puro > 0 else 0
    ax.text(0.5, 0.92, f'Reducción: {reduccion:.1f}%',
            transform=ax.transAxes, ha='center', fontsize=11,
            color='#27ae60', fontweight='bold')

    plt.tight_layout()
    plt.savefig('nodos_expandidos.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("[analisis] Gráfica guardada: nodos_expandidos.png")


def simular_partida(state: GameState, depth: int = 4, usar_poda: bool = True,
                    verbose: bool = True) -> dict:
    nombre_algo = "Alfa-Beta" if usar_poda else "Minimax Puro"
    if verbose:
        print()
        print("=" * 55)
        print(f"  SIMULACIÓN: MAX ({nombre_algo}) vs MIN (aleatorio)")
        print("=" * 55)

    total_nodos_expandidos = 0
    turno = 0

    while not state.is_terminal():
        turno += 1
        if verbose:
            print(f"\n  Turno {turno} | {state}")

        if state.current_turn == MAX_PLAYER:
            accion, nodos_exp = agente_max(state, depth, usar_poda)
            total_nodos_expandidos += nodos_exp
            if accion:
                if verbose:
                    print(f"  MAX captura: {accion}  "
                          f"(valor={state.node_values[accion]}, "
                          f"nodos_exp={nodos_exp})")
                state = state.apply_action(accion, MAX_PLAYER)
            else:
                if verbose:
                    print("  MAX no tiene acciones disponibles, pasa turno.")
                state = state.pass_turn()

        else:  # MIN aleatorio
            accion = agente_min_aleatorio(state)
            if accion:
                if verbose:
                    print(f"  MIN captura: {accion}  "
                          f"(valor={state.node_values[accion]})")
                state = state.apply_action(accion, MIN_PLAYER)
            else:
                if verbose:
                    print("  MIN no tiene acciones disponibles, pasa turno.")
                state = state.pass_turn()

    score_final = state.score()
    ganador = "MAX (Defensa)" if score_final > 0 else ("MIN (Hacker)" if score_final < 0 else "Empate")

    if verbose:
        print()
        print("=" * 55)
        print("  RESULTADO FINAL")
        print("=" * 55)
        print(f"  Nodos MAX : {len(state.max_nodes)} nodos | "
              f"Valor total: {sum(state.node_values[n] for n in state.max_nodes)}")
        print(f"  Nodos MIN : {len(state.min_nodes)} nodos | "
              f"Valor total: {sum(state.node_values[n] for n in state.min_nodes)}")
        print(f"  Score final (MAX - MIN) : {score_final:+d}")
        print(f"  Ganador   : {ganador}")
        print(f"  Nodos árbol expandidos (total MAX) : {total_nodos_expandidos:,}")
        print("=" * 55)

    return {
        'score': score_final,
        'ganador': ganador,
        'nodos_max': len(state.max_nodes),
        'nodos_min': len(state.min_nodes),
        'nodos_expandidos': total_nodos_expandidos,
        'turnos': turno,
    }