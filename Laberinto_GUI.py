import tkinter as tk
import random
import heapq

# Definir el tamaño del tablero y los personajes
CELL_SIZE = 60

class GameGUI:
    def __init__(self, master, size, rene_start, elmo_start, galleta_start, piggy_start, obstacles):
        self.master = master
        self.size = size
        self.rene_pos = rene_start
        self.elmo_pos = elmo_start
        self.galleta_pos = galleta_start
        self.piggy_pos = piggy_start
        self.obstacles = obstacles
        
        # Crear el lienzo
        self.canvas = tk.Canvas(master, width=size * CELL_SIZE, height=size * CELL_SIZE)
        self.canvas.pack()
        
        # Dibujar el tablero inicial
        self.draw_board()
        
    def draw_board(self):
        self.canvas.delete("all")
        
        # Dibujar las celdas del tablero
        for i in range(self.size):
            for j in range(self.size):
                x1, y1 = j * CELL_SIZE, i * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                
                # Dibujar los obstáculos
                if (i, j) in self.obstacles:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="black")
        
        # Dibujar a René
        self.draw_character(self.rene_pos, "green")
        
        # Dibujar a Elmo
        self.draw_character(self.elmo_pos, "red")
        
        # Dibujar la galleta
        self.draw_character(self.galleta_pos, "yellow")
        
        # Dibujar a Piggy
        self.draw_character(self.piggy_pos, "pink")
    
    def draw_character(self, pos, color):
        x1, y1 = pos[1] * CELL_SIZE, pos[0] * CELL_SIZE
        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
        self.canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill=color, outline=color)
    
    # Actualizar las posiciones y redibujar el tablero
    def update_positions(self, rene_pos, piggy_pos):
        self.rene_pos = rene_pos
        self.piggy_pos = piggy_pos
        self.draw_board()

# Algoritmos y lógica del juego
def is_valid_move(position, size, obstacles):
    return (
        0 <= position[0] < size and 0 <= position[1] < size and position not in obstacles
    )

def depth_limited_search(rene_pos, elmo_pos, galleta_pos, depth_limit, size, obstacles):
    stack = [(rene_pos, 0, False)]  # Pila: (posición actual, costo, ha tomado galleta)
    visited = set()
    
    while stack:
        (current_pos, current_cost, has_galleta) = stack.pop()
        
        if current_pos == elmo_pos:
            return True, current_pos  # René encontró a Elmo
        
        if current_cost >= depth_limit or current_pos in visited:
            continue

        visited.add(current_pos)
        
        # Generar los movimientos posibles (arriba, abajo, izquierda, derecha)
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = (current_pos[0] + move[0], current_pos[1] + move[1])
            
            if is_valid_move(new_pos, size, obstacles):
                new_cost = current_cost + (0.5 if has_galleta else 1)
                
                # Si toma la galleta, reduce el costo
                if new_pos == galleta_pos:
                    stack.append((new_pos, new_cost, True))
                else:
                    stack.append((new_pos, new_cost, has_galleta))
    
    return False, current_pos  # No encontró a Elmo

def breadth_first_search(piggy_pos, rene_pos, size, obstacles):
    queue = [(piggy_pos, 0)]  # Cola: (posición actual, costo)
    visited = set()
    
    while queue:
        (current_pos, current_cost) = queue.pop(0)
        
        if current_pos == rene_pos:
            return True, current_pos  # Piggy encontró a René
        
        if current_pos in visited:
            continue
        
        visited.add(current_pos)
        
        # Generar los movimientos posibles (arriba, abajo, izquierda, derecha)
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = (current_pos[0] + move[0], current_pos[1] + move[1])
            
            if is_valid_move(new_pos, size, obstacles):
                queue.append((new_pos, current_cost + 1))
    
    return False, current_pos  # No encontró a René

def astar_search(piggy_pos, rene_pos, size, obstacles):
    def heuristic(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    heap = [(0, piggy_pos, 0)]  # Montículo: (costo estimado, posición actual, costo real)
    visited = set()
    
    while heap:
        (estimated_cost, current_pos, current_cost) = heapq.heappop(heap)
        
        if current_pos == rene_pos:
            return True, current_pos  # Piggy encontró a René
        
        if current_pos in visited:
            continue
        
        visited.add(current_pos)
        
        # Generar los movimientos posibles (arriba, abajo, izquierda, derecha)
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = (current_pos[0] + move[0], current_pos[1] + move[1])
            
            if is_valid_move(new_pos, size, obstacles):
                new_cost = current_cost + 1
                heapq.heappush(heap, (new_cost + heuristic(new_pos, rene_pos), new_pos, new_cost))
    
    return False, current_pos  # No encontró a René

# Simulación del juego con interfaz gráfica
def simulate_game_with_gui(master, size, rene_start, elmo_start, galleta_start, piggy_start, depth_limit, obstacles):
    gui = GameGUI(master, size, rene_start, elmo_start, galleta_start, piggy_start, obstacles)
    rene_pos = rene_start
    piggy_pos = piggy_start
    turns = 0

    def game_turn():
        nonlocal rene_pos, piggy_pos, turns
        
        # Movimiento de René
        rene_found_elmo, new_rene_pos = depth_limited_search(rene_pos, elmo_start, galleta_start, depth_limit, size, obstacles)
        rene_pos = new_rene_pos
        
        if rene_found_elmo:
            print(f"René ha encontrado a Elmo en el turno {turns + 1}.")
            return  # Fin del juego
        
        # Movimiento de Piggy
        if random.random() < 0.4:
            print("Piggy cambia su estrategia a A*.")
            piggy_found_rene, new_piggy_pos = astar_search(piggy_pos, rene_pos, size, obstacles)
        else:
            print("Piggy sigue con BFS.")
            piggy_found_rene, new_piggy_pos = breadth_first_search(piggy_pos, rene_pos, size, obstacles)
        
        piggy_pos = new_piggy_pos
        
        if piggy_found_rene:
            print(f"Piggy ha encontrado a René en el turno {turns + 1}.")
            return  # Fin del juego
        
        # Actualizar el tablero gráfico
        gui.update_positions(rene_pos, piggy_pos)
        
        # Incrementar el contador de turnos
        turns += 1
        
        # Pausar un poco antes del siguiente turno
        master.after(500, game_turn)

    # Iniciar el primer turno
    master.after(500, game_turn)

# Configuración del juego
size = 6
rene_start = (0, 0)
elmo_start = (5, 5)
galleta_start = (3, 3)
piggy_start = (5, 0)
depth_limit = 15
obstacles = [(1, 1), (1, 2), (2, 2), (3, 1), (4, 4)]

# Crear la ventana principal de la interfaz gráfica
root = tk.Tk()
root.title("René y Piggy - Búsqueda Gráfica")

# Ejecutar la simulación con la interfaz gráfica
simulate_game_with_gui(root, size, rene_start, elmo_start, galleta_start, piggy_start, depth_limit, obstacles)

# Ejecutar la interfaz gráfica
root.mainloop()
