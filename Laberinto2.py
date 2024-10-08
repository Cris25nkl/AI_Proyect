class Laberinto:
    def __init__(self, size, rene_pos, elmo_pos, galleta_pos, piggy_pos):
        self.size = size
        self.board = [['.' for _ in range(size)] for _ in range(size)]
        self.rene_pos = rene_pos
        self.elmo_pos = elmo_pos
        self.galleta_pos = galleta_pos
        self.piggy_pos = piggy_pos
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
        
        if current_pos in visited:
            continue
        
        visited.add(current_pos)
        
        if current_cost < depth_limit:
            # Generar movimientos válidos (arriba, abajo, izquierda, derecha)
            for move in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_pos = (current_pos[0] + move[0], current_pos[1] + move[1])
                if is_valid_move(new_pos, size):
                    stack.append((new_pos, current_cost + 1, has_galleta))
    
    return False, -1  # No encontró a Elmo

# Ejemplo de uso
laberinto = Laberinto(9, (0, 0), (4, 8), (7, 2), (5, 3))
laberinto.display()
found, cost = depth_limited_search((0, 0), (4, 4), (2, 2), 10, 5)
print(f"Found: {found}, Cost: {cost}")