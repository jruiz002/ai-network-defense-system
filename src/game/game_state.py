
import random
from typing import Dict, Set, List, Optional
from src.network.graph import Graph


# Identificadores de jugador
MAX_PLAYER = "MAX"   # Defensa
MIN_PLAYER = "MIN"   # Hacker


class GameState:

    def __init__(
        self,
        graph: Graph,
        node_values: Dict[str, int],
        max_start: str,
        min_start: str,
        max_turns: int = 30,
        current_turn: str = MAX_PLAYER,
    ):
        self.graph       = graph
        self.node_values = node_values
        self.max_turns   = max_turns
        self.turn_number = 0
        self.current_turn = current_turn

        # Asignar nodos iniciales
        self.max_nodes: Set[str] = {max_start}
        self.min_nodes: Set[str] = {min_start}
        self.free_nodes: Set[str] = (
            set(graph.nodes) - self.max_nodes - self.min_nodes
        )

    # ── Consultas de estado ─────────────────────────────────────────

    def is_terminal(self) -> bool:

        return len(self.free_nodes) == 0 or self.turn_number >= self.max_turns

    def score(self) -> int:

        return (
            sum(self.node_values[n] for n in self.max_nodes)
            - sum(self.node_values[n] for n in self.min_nodes)
        )

    def get_actions(self, player: str) -> List[str]:

        owned = self.max_nodes if player == MAX_PLAYER else self.min_nodes
        capturable = set()
        for node in owned:
            for neighbor in self.graph.get_neighbors(node):
                if neighbor in self.free_nodes:
                    capturable.add(neighbor)
        return list(capturable)

    # ── Transición de estado ────────────────────────────────────────

    def apply_action(self, node: str, player: str) -> "GameState":
        new_state = GameState.__new__(GameState)
        new_state.graph       = self.graph
        new_state.node_values = self.node_values
        new_state.max_turns   = self.max_turns
        new_state.turn_number = self.turn_number + 1

        # Copiar conjuntos y aplicar cambio
        new_state.max_nodes  = set(self.max_nodes)
        new_state.min_nodes  = set(self.min_nodes)
        new_state.free_nodes = set(self.free_nodes)

        if player == MAX_PLAYER:
            new_state.max_nodes.add(node)
        else:
            new_state.min_nodes.add(node)
        new_state.free_nodes.discard(node)

        # Cambiar turno
        new_state.current_turn = (
            MIN_PLAYER if player == MAX_PLAYER else MAX_PLAYER
        )
        return new_state

    def pass_turn(self) -> "GameState":
        new_state = GameState.__new__(GameState)
        new_state.graph = self.graph
        new_state.node_values = self.node_values
        new_state.max_turns = self.max_turns
        new_state.turn_number = self.turn_number + 1
        new_state.max_nodes = set(self.max_nodes)
        new_state.min_nodes = set(self.min_nodes)
        new_state.free_nodes = set(self.free_nodes)
        new_state.current_turn = (
            MIN_PLAYER if self.current_turn == MAX_PLAYER else MAX_PLAYER
        )
        return new_state

    # ── Utilidades de visualización ─────────────────────────────────

    def __str__(self) -> str:
        return (
            f"Turno {self.turn_number} | Juega: {self.current_turn} | "
            f"Score: {self.score():+d} | "
            f"MAX={len(self.max_nodes)} nodos | "
            f"MIN={len(self.min_nodes)} nodos | "
            f"Libres={len(self.free_nodes)}"
        )


# ── Función de inicialización del juego ────────────────────────────────────

def crear_juego(seed: int = 42, num_nodes: int = 20, max_turns: int = 30) -> GameState:
    random.seed(seed)
    graph = Graph(num_nodes=num_nodes, edge_probability=0.35)

    # Valores de información: enteros aleatorios entre 1 y 20
    node_values = {node: random.randint(1, 20) for node in graph.nodes}

    # MAX empieza en Server_0, MIN en el nodo más alejado (último)
    max_start = graph.nodes[0]
    min_start = graph.nodes[-1]

    print("=" * 52)
    print("  INICIALIZACIÓN DEL JUEGO ADVERSARIAL")
    print("=" * 52)
    print(f"  {graph}")
    print(f"  Nodo inicial MAX (Defensa) : {max_start}")
    print(f"  Nodo inicial MIN (Hacker)  : {min_start}")
    print(f"  Límite de turnos           : {max_turns}")
    print()
    print("  Valores de Información por nodo:")
    for node, val in node_values.items():
        print(f"    {node:<12} : {val:>3}")
    print("=" * 52)

    return GameState(graph, node_values, max_start, min_start, max_turns)