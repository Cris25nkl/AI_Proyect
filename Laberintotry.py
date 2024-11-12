import random
import heapq
import matplotlib.pyplot as plt

# Definir el tablero y sus elementos
class Board:
    def __init__(self, size, rene_pos, elmo_pos, galleta_pos, piggy_pos, obstacles):
        self.size = size
        self.board = [['.' for _ in range(size)] for _ in range(size)]
        self.rene_pos = rene_pos
        self.elmo_pos = elmo_pos
        self.galleta_pos = galleta_pos
        self.piggy_pos = piggy_pos
        self.obstacles = obstacles  # Lista de posiciones con obstáculos
        
        # Colocar los elementos en el tablero
        self.update_board()

    def update_board(self):
        self.board = [['.' for _ in range(self.size)] for _ in range(self.size)]
        for obs in self.obstacles:
            self.board[obs[0]][obs[1]] = 'X'
        self.board[self.rene_pos[0]][self.rene_pos[1]] = 'R'  # René
        self.board[self.elmo_pos[0]][self.elmo_pos[1]] = 'E'  # Elmo
        self.board[self.galleta_pos[0]][self.galleta_pos[1]] = 'G'  # Galleta
        self.board[self.piggy_pos[0]][self.piggy_pos[1]] = 'P'  # Piggy

    def display(self):
        for row in self.board:
            print(' '.join(row))

# Función para visualizar el tablero en tiempo real usando matplotlib
def visualize_board(board):
    # Mapeo de caracteres a valores numéricos
    symbol_to_number = {
        '.': 0,  # Espacio vacío
        'X': 1,  # Obstáculo
        'R': 2,  # René
        'E': 3,  # Elmo
        'G': 4,  # Galleta
        'P': 5   # Piggy
    }
    # Convertir el tablero en una matriz numérica
    numeric_board = [[symbol_to_number[cell] for cell in row] for row in board]
    
    # Visualizar la matriz numérica
    plt.clf()
    plt.imshow(numeric_board, cmap="Pastel1", vmin=0, vmax=6)
    plt.xticks([]), plt.yticks([])
    plt.draw()
    plt.pause(0.3)

# Verificar si un movimiento es válido (dentro del tablero y no es obstáculo)
def is_valid_move(position, size, obstacles):
    return (
        0 <= position[0] < size and 0 <= position[1] < size and position not in obstacles
    )

def heuristic(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def reconstruct_path(node):
    """Reconstruct the path by following parent nodes."""
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]

def main(rene_pos, elmo_pos, galleta_pos, depth_limit, size, obstacles, piggy_pos):
    board = Board(size, rene_pos, elmo_pos, galleta_pos, piggy_pos, obstacles)
    stack = [(rene_pos, 0, False)]  # Pila: (posición actual, costo, ha tomado galleta)
    heap = []  # Montículo: (costo estimado, posición actual, costo real)
    queue = [(piggy_pos, 0)]  # Cola: (posición actual, costo)
    visited_R = set()
    visited_p = set()

    current_pos_R = rene_pos
    current_pos_p = piggy_pos
    current_cost_R = 0

    
    # Inicialización de Piggy en el A* 
    heapq.heappush(heap, (heuristic(piggy_pos, rene_pos), piggy_pos, 0))

    # Inicializar la visualización
    plt.ion()  # Modo interactivo de matplotlib
    fig, ax = plt.subplots()

    while stack:
        #print("Rene avanza")
        print(f"René está en {current_pos_R} con costo {current_cost_R}")
        (current_pos_R, current_cost_R, has_galleta) = stack.pop()

        if current_pos_R not in visited_R:
           board.rene_pos = current_pos_R
           board.update_board()
           visualize_board(board.board)
        
        if current_pos_R == elmo_pos:
            print(f"\nRené ha encontrado a Elmo en {current_cost_R} movimientos.\n")
            break  # Encontró a Elmo
        
        if current_cost_R >= depth_limit or current_pos_R in visited_R:
            continue
        visited_R.add(current_pos_R)     
        
        # Generar los movimientos posibles (arriba, abajo, izquierda, derecha)
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = (current_pos_R[0] + move[0], current_pos_R[1] + move[1])
            if is_valid_move(new_pos, size, obstacles):
                new_cost = current_cost_R + 1
                # Si toma la galleta, reduce el costo
                if new_pos == galleta_pos:
                    new_cost = current_cost_R - 2
                    print('galleta')
                    stack.append((new_pos, new_cost, True))
                else:
                    stack.append((new_pos, new_cost, has_galleta))

        #print("piggy avanza")
        if random.random() <= 0.4:
            print("Piggy cambia su estrategia a A*.")
            
            board.piggy_pos = current_pos_p
            board.update_board()
            visualize_board(board.board)
            
            if not heap:
                continue
            estimated_cost, current_pos_p, current_cost_p = heapq.heappop(heap)
            print(f"Piggy (A*) está en {current_pos_p} con costo {current_cost_p}")
            
            if current_pos_p == current_pos_R:
                print(f"Piggy ha encontrado a René en {current_cost_p} movimientos.")
                return  # Piggy encontró a René y termina
            
            if current_pos_p in visited_p:
                continue
            visited_p.add(current_pos_p)
            
            # Generar los movimientos posibles para A*
            for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_pos_p = (current_pos_p[0] + move[0], current_pos_p[1] + move[1])
                if is_valid_move(new_pos_p, size, obstacles) and new_pos_p not in visited_p:
                    new_cost_p = current_cost_p + 1
                    estimated_cost = new_cost_p + heuristic(new_pos_p, current_pos_R)
                    heapq.heappush(heap, (estimated_cost, new_pos_p, new_cost_p))
        else:
            print("Piggy sigue con BFS.")
            if not queue:
                continue
            current_pos, current_cost_p = queue.pop(0)
            board.piggy_pos = current_pos
            board.update_board()
            visualize_board(board.board)

            print(f"Piggy (BFS) está en {current_pos} con costo {current_cost_p}")
            
            if current_pos == rene_pos:
                print(f"Piggy ha encontrado a René en {current_cost_p} movimientos.")
                break # Piggy encontró a René y termina
            
            if current_pos in visited_p:
                continue
            visited_p.add(current_pos)
            
            # Generar los movimientos posibles para BFS
            for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_pos = (current_pos[0] + move[0], current_pos[1] + move[1])
                if is_valid_move(new_pos, size, obstacles) and new_pos not in visited_p:
                    queue.append((new_pos, current_cost_p + 1))

    plt.ioff()  # Desactivar modo interactivo
    plt.show()

# Parámetros del juego
size = 6
rene_start = (0, 0)
elmo_start = (5, 5)
galleta_start = (3, 3)
piggy_start = (5, 0)
depth_limit = 15

# Definir obstáculos (posiciones que no se pueden atravesar)
obstacles = [(1, 1), (1, 2), (2, 2), (3, 1), (4, 4)]

# Iniciar la simulación
main(rene_start, elmo_start, galleta_start, depth_limit, size, obstacles, piggy_start)
