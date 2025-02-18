import math
from queue import PriorityQueue
import random
import matplotlib.pyplot as plt

WIDTH = 1000
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.type = ""
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.costo = 0

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.type == "closed"

    def is_open(self):
        return self.type == "open"

    def is_barrier(self):
        return self.type == "barrier"

    def is_start(self):
        return self.type == "start"

    def is_end(self):
        return self.type == "end"
    
    def is_path(self):
        return self.type == "path"

    def reset(self):
        self.type = ""

    def make_start(self):
        self.type = "start"

    def make_closed(self):
        self.type = "closed"

    def make_open(self):
        self.type = "open"

    def make_barrier(self):
        self.type = "barrier"

    def make_end(self):
        self.type = "end"

    def make_path(self):
        self.type = "path"


    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current):
    while current in came_from:
        current = came_from[current]
        current.make_path()


def algorithm(grid, start, end):
    count = 0
    costo = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current.get_pos() == end.get_pos():
            reconstruct_path(came_from, end)
            costo = g_score[end]

            break

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

    return costo



def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def generar_vecino(solution):
    # Función para generar una solución vecina mediante shuffle
    neighbor = solution
    random.shuffle(neighbor)
    return neighbor
    
def temple_simulado(grid, actual_estado, start, initial_temp, cooling_rate):
    
    current_solution = actual_estado
    current_cost = 0

    for end in actual_estado:
        end.make_end()
        for row in grid:
            for spot in row:
                spot.update_neighbors(grid)
        current_cost += algorithm(grid, start, end)  # Calcular el costo inicial
        end.reset()
        start.reset()
        start = end
        start.make_start()

    print("El costo actual", current_cost)
    best_cost = float('inf')  # Inicializar el mejor costo como infinito
    best_solution = current_solution
    # Listas para almacenar los costos finales y las iteraciones
    costos_finales = []
    iteraciones = []
    current_temp = initial_temp
    i = 0
    while current_temp > 1:
        costos_finales.append(current_cost)
        iteraciones.append(i)
        i = i + 1
        neighbor_cost = 0
        neighbor = generar_vecino(current_solution)  # Utiliza una copia de la solución actual
        for end in neighbor:
            end.make_end()
            for row in grid:
                for spot in row:
                    spot.update_neighbors(grid)
            neighbor_cost += algorithm(grid, start, end)  # Sumar el costo de la ruta actual
            end.reset()
            start.reset()
            start = end
            start.make_start()
        
        DE = neighbor_cost - current_cost
        
        # Si el vecino es mejor
        if DE < 0:
            current_solution = neighbor
            current_cost = neighbor_cost
        
        elif math.exp(-DE / current_temp) > random.random():
            current_solution = neighbor
            current_cost = neighbor_cost


        # Actualizar el mejor costo y solución si es necesario
        if current_cost < best_cost:
            best_solution = current_solution
            best_cost = current_cost
        
        # Actualizar la temperatura actual
        current_temp *= cooling_rate

    print("El mejor costo encontrado", best_cost)
    plt.plot(iteraciones, costos_finales)
    plt.title('Costos vs. Iteraciones')
    plt.xlabel('Iteraciones')
    plt.ylabel('Costos')
    plt.grid(True)
    plt.show()

    return best_solution


def generate_adjacent_elements(grid, num_elements, start):
    adjacent_elements = []
    ROWS = len(grid)

    while len(adjacent_elements) < num_elements:
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, ROWS - 1)
        spot = grid[row][col]
        if spot.is_barrier():
            adjacent = []
            if row > 0:
                adjacent.append(grid[row - 1][col])
            if row < ROWS - 1:
                adjacent.append(grid[row + 1][col])
            if col > 0:
                adjacent.append(grid[row][col - 1])
            if col < ROWS - 1:
                adjacent.append(grid[row][col + 1])
            valid_adjacent_spots = [spot for spot in adjacent if not spot.is_barrier() and spot != start]
            if valid_adjacent_spots:
                adjacent_elements.append(random.choice(valid_adjacent_spots))

    return adjacent_elements

def main(width):
    ROWS = 20
    grid = make_grid(ROWS, width)
    spot = grid[3][2]
    spot.make_barrier()
    spot = grid[3][3]
    spot.make_barrier()
    spot = grid[3][4]
    spot.make_barrier()
    spot = grid[3][5]
    spot.make_barrier()

    spot = grid[4][2]
    spot.make_barrier()
    spot = grid[4][3]
    spot.make_barrier()
    spot = grid[4][4]
    spot.make_barrier()
    spot = grid[4][5]
    spot.make_barrier()

    spot = grid[3][8]
    spot.make_barrier()
    spot = grid[3][9]
    spot.make_barrier()
    spot = grid[3][10]
    spot.make_barrier()
    spot = grid[3][11]
    spot.make_barrier()

    spot = grid[4][8]
    spot.make_barrier()
    spot = grid[4][9]
    spot.make_barrier()
    spot = grid[4][10]
    spot.make_barrier()
    spot = grid[4][11]
    spot.make_barrier()

    spot = grid[3][14]
    spot.make_barrier()
    spot = grid[3][15]
    spot.make_barrier()
    spot = grid[3][16]
    spot.make_barrier()
    spot = grid[3][17]
    spot.make_barrier()

    spot = grid[4][14]
    spot.make_barrier()
    spot = grid[4][15]
    spot.make_barrier()
    spot = grid[4][16]
    spot.make_barrier()
    spot = grid[4][17]
    spot.make_barrier()

    spot = grid[9][2]
    spot.make_barrier()
    spot = grid[9][3]
    spot.make_barrier()
    spot = grid[9][4]
    spot.make_barrier()
    spot = grid[9][5]
    spot.make_barrier()

    spot = grid[10][2]
    spot.make_barrier()
    spot = grid[10][3]
    spot.make_barrier()
    spot = grid[10][4]
    spot.make_barrier()
    spot = grid[10][5]
    spot.make_barrier()

    spot = grid[9][8]
    spot.make_barrier()
    spot = grid[9][9]
    spot.make_barrier()
    spot = grid[9][10]
    spot.make_barrier()
    spot = grid[9][11]
    spot.make_barrier()

    spot = grid[10][8]
    spot.make_barrier()
    spot = grid[10][9]
    spot.make_barrier()
    spot = grid[10][10]
    spot.make_barrier()
    spot = grid[10][11]
    spot.make_barrier()

    spot = grid[9][14]
    spot.make_barrier()
    spot = grid[9][15]
    spot.make_barrier()
    spot = grid[9][16]
    spot.make_barrier()
    spot = grid[9][17]
    spot.make_barrier()

    spot = grid[10][14]
    spot.make_barrier()
    spot = grid[10][15]
    spot.make_barrier()
    spot = grid[10][16]
    spot.make_barrier()
    spot = grid[10][17]
    spot.make_barrier()

    spot = grid[15][2]
    spot.make_barrier()
    spot = grid[15][3]
    spot.make_barrier()
    spot = grid[15][4]
    spot.make_barrier()
    spot = grid[15][5]
    spot.make_barrier()

    spot = grid[16][2]
    spot.make_barrier()
    spot = grid[16][3]
    spot.make_barrier()
    spot = grid[16][4]
    spot.make_barrier()
    spot = grid[16][5]
    spot.make_barrier()

    spot = grid[15][8]
    spot.make_barrier()
    spot = grid[15][9]
    spot.make_barrier()
    spot = grid[15][10]
    spot.make_barrier()
    spot = grid[15][11]
    spot.make_barrier()

    spot = grid[16][8]
    spot.make_barrier()
    spot = grid[16][9]
    spot.make_barrier()
    spot = grid[16][10]
    spot.make_barrier()
    spot = grid[16][11]
    spot.make_barrier()

    spot = grid[15][14]
    spot.make_barrier()
    spot = grid[15][15]
    spot.make_barrier()
    spot = grid[15][16]
    spot.make_barrier()
    spot = grid[15][17]
    spot.make_barrier()

    spot = grid[16][14]
    spot.make_barrier()
    spot = grid[16][15]
    spot.make_barrier()
    spot = grid[16][16]
    spot.make_barrier()
    spot = grid[16][17]
    spot.make_barrier()

    start = grid[0][0]
    start.make_start()

    actual_estado = generate_adjacent_elements(grid, 15, start)


    best = temple_simulado(grid, actual_estado, start, 100, 0.99)
    
    print("Solución encontrada:")
    for spot in best:
        print(f"({spot.row}, {spot.col})")

main(WIDTH)



