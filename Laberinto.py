import random
import heapq

# Definir el tablero y sus elementos
class Board:
    def __init__(self, size, rene_pos, elmo_pos, galleta_pos, piggy_pos):
        self.size = size
        self.board = [['.' for _ in range(size)] for _ in range(size)]
        self.rene_pos = rene_pos
        self.elmo_pos = elmo_pos
        self.galleta_pos = galleta_pos
        self.piggy_pos = piggy_pos
        
        # Colocar los elementos en el tablero
        self.update_board()

    def update_board(self):
        self.board = [['.' for _ in range(self.size)]]
        self.board[self.rene_pos[0]][self.rene_pos[1]] = 'R'  # René
        self.board[self.elmo_pos[0]][self.elmo_pos[1]] = 'E'  # Elmo
        self.board[self.galleta_pos[0]][self.galleta_pos[1]] = 'G'  # Galleta
        self.board[self.piggy_pos[0]][self.piggy_pos[1]] = 'P'  # Piggy

    def display(self):
        for row in self.board:
            print(' '.join(row))

# Movimiento válido en el tablero
def is_valid_move(position, size):
    return 0 <= position[0] < size and 0 <= position[1] < size

# Algoritmo de búsqueda limitada por profundidad para René
def depth_limited_search(rene_pos, elmo_pos, galleta_pos, depth_limit, size):
    stack = [(rene_pos, 0, False)]  # Pila: (posición actual, costo, ha tomado galleta)
    visited = set()
    
    while stack:
        (current_pos, current_cost, has_galleta) = stack.pop()
        
        if current_pos == elmo_pos:
            return True, current_cost  # Encontró a Elmo
        
        if current_cost >= depth_limit or current_pos in visited:
            continue

        visited.add(current_pos)
        
        # Generar los movimientos posibles (arriba, abajo, izquierda, derecha)
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = (current_pos[0] + move[0], current_pos[1] + move[1])
            
            if is_valid_move(new_pos, size):
                new_cost = current_cost + (0.5 if has_galleta else 1)
                
                # Si toma la galleta, reduce el costo
                if new_pos == galleta_pos:
                    stack.append((new_pos, new_cost, True))
                else:
                    stack.append((new_pos, new_cost, has_galleta))
    
    return False, current_cost  # No encontró a Elmo

# Algoritmo de búsqueda por amplitud para Piggy
def breadth_first_search(piggy_pos, rene_pos, size):
    queue = [(piggy_pos, 0)]  # Cola: (posición actual, costo)
    visited = set()
    
    while queue:
        (current_pos, current_cost) = queue.pop(0)
        
        if current_pos == rene_pos:
            return True, current_cost  # Piggy encontró a René
        
        if current_pos in visited:
            continue
        
        visited.add(current_pos)
        
        # Generar los movimientos posibles (arriba, abajo, izquierda, derecha)
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = (current_pos[0] + move[0], current_pos[1] + move[1])
            
            if is_valid_move(new_pos, size):
                queue.append((new_pos, current_cost + 1))
    
    return False, current_cost  # No encontró a René

# Algoritmo A* para Piggy
def astar_search(piggy_pos, rene_pos, size):
    def heuristic(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    heap = [(0, piggy_pos, 0)]  # Montículo: (costo estimado, posición actual, costo real)
    visited = set()
    
    while heap:
        (estimated_cost, current_pos, current_cost) = heapq.heappop(heap)
        
        if current_pos == rene_pos:
            return True, current_cost  # Piggy encontró a René
        
        if current_pos in visited:
            continue
        
        visited.add(current_pos)
        
        # Generar los movimientos posibles (arriba, abajo, izquierda, derecha)
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = (current_pos[0] + move[0], current_pos[1] + move[1])
            
            if is_valid_move(new_pos, size):
                new_cost = current_cost + 1
                heapq.heappush(heap, (new_cost + heuristic(new_pos, rene_pos), new_pos, new_cost))
    
    return False, current_cost  # No encontró a René

# Simulación del juego
def simulate_game(size, rene_start, elmo_start, galleta_start, piggy_start, depth_limit):
    board = Board(size, rene_start, elmo_start, galleta_start, piggy_start)
    turns = 0

    while True:
        board.display()
        print(f"Turno {turns + 1}")
        
        # Movimiento de René
        rene_found_elmo, rene_cost = depth_limited_search(board.rene_pos, board.elmo_pos, board.galleta_pos, depth_limit, size)
        if rene_found_elmo:
            print(f"René ha encontrado a Elmo en {rene_cost} movimientos.")
            break
        
        # Movimiento de Piggy
        if random.random() < 0.4:
            print("Piggy cambia su estrategia a A*.")
            piggy_found_rene, piggy_cost = astar_search(board.piggy_pos, board.rene_pos, size)
        else:
            print("Piggy sigue con BFS.")
            piggy_found_rene, piggy_cost = breadth_first_search(board.piggy_pos, board.rene_pos, size)
        
        if piggy_found_rene:
            print(f"Piggy ha encontrado a René en {piggy_cost} movimientos.")
            break
        
        # Actualización del turno
        turns += 1
        print()

# Parámetros del juego
size = 10
rene_start = (0, 0)
elmo_start = (4, 4)
galleta_start = (2, 2)
piggy_start = (4, 0)
depth_limit = 10

# Iniciar la simulación
simulate_game(size, rene_start, elmo_start, galleta_start, piggy_start, depth_limit)