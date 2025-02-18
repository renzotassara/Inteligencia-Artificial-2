import pygame
from queue import PriorityQueue
import random

# Configuración de la ventana
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# Colores
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


# Clase Spot que representa cada celda en la cuadrícula
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED
    #Por otro lado, marcar un nodo como "cerrado" significa que el algoritmo ya
    # ha terminado de considerar este nodo y no necesita volver a visitarlo.
    # Esto generalmente sucede después de que el algoritmo haya explorado todas las
    # posibles expansiones de este nodo y haya tomado una decisión final basada en la información disponible.

    def make_open(self):
        self.color = GREEN
    #Marcar un nodo como "abierto" significa que el algoritmo ha explorado
    # este nodo y lo ha agregado a la lista de nodos que están listos para ser examinados y
    # posiblemente expandidos en el futuro. En otras palabras, el nodo está actualmente siendo considerado activamente por el algoritmo.


    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []  # Reinicia la lista de vecinos de la celda actual

        # Comprueba si la celda debajo de la actual no es una barrera y está dentro de los límites de la cuadrícula
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            # Agrega la celda debajo de la actual a la lista de vecinos
            self.neighbors.append(grid[self.row + 1][self.col])  # DOWN

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])  # UP

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])  # RIGHT

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])  # LEFT


# Función heurística para estimar el costo desde un punto hasta el objetivo
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# Función para reconstruir el camino encontrado por el algoritmo A*
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0  # Contador para asignar prioridades únicas en la cola de prioridad
    open_set = PriorityQueue()  # Cola de prioridad para almacenar los nodos a explorar
    open_set.put((0, count, start))  # Se agrega el nodo inicial a la cola de prioridad con prioridad 0
    came_from = {}  # Diccionario para almacenar el camino reconstruido
    g_score = {spot: float("inf") for row in grid for spot in row}  # Diccionario para almacenar el costo real de llegar a cada nodo
    g_score[start] = 0  # El costo para llegar al nodo inicial es 0
    f_score = {spot: float("inf") for row in grid for spot in row}  # Diccionario para almacenar la estimación del costo total desde el inicio hasta el objetivo a través del nodo actual
    f_score[start] = h(start.get_pos(), end.get_pos())  # Estimación inicial del costo total desde el inicio hasta el objetivo

    open_set_hash = {start}  # Conjunto para realizar verificaciones rápidas de pertenencia al conjunto abierto

    while not open_set.empty():  # Mientras haya nodos en la cola de prioridad
        for event in pygame.event.get():  # Manejo de eventos de pygame
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]  # Selecciona el nodo con la menor f_score de la cola de prioridad
        open_set_hash.remove(current)  # Elimina el nodo actual del conjunto abierto

        if current == end:  # Si se ha llegado al nodo objetivo
            reconstruct_path(came_from, end, draw)  # Reconstruye el camino desde el inicio hasta el objetivo
            end.make_end()  # Marca el nodo objetivo
            start.make_start()  # Marca el nodo inicial
            return True  # Retorna True para indicar que se encontró un camino

        for neighbor in current.neighbors:  # Para cada vecino del nodo actual
            temp_g_score = g_score[current] + 1  # Calcula el costo real para llegar al vecino desde el nodo actual
            if temp_g_score < g_score[neighbor]:  # Si se encontró un camino más corto para llegar al vecino
                came_from[neighbor] = current  # Actualiza el nodo desde el que se llegó al vecino
                g_score[neighbor] = temp_g_score  # Actualiza el costo real para llegar al vecino
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())  # Actualiza la estimación del costo total desde el inicio hasta el objetivo pasando por el vecino
                if neighbor not in open_set_hash:  # Si el vecino no está en el conjunto abierto
                    count += 1  # Incrementa el contador
                    open_set.put((f_score[neighbor], count, neighbor))  # Agrega el vecino a la cola de prioridad con su nueva f_score
                    open_set_hash.add(neighbor)  # Agrega el vecino al conjunto abierto
                    neighbor.make_open()  # Marca el vecino como abierto
        draw()  # Dibuja el estado actual del grafo

        if current != start:  # Si el nodo actual no es el nodo inicial
            current.make_closed()  # Marca el nodo actual como cerrado
            pass
    return False  # Retorna False si no se encontró un camino



def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()



def main(win, width):
    ROWS = 20
    grid = make_grid(ROWS, width)
    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

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

            # Bucle para seleccionar una posición de inicio aleatoria que no sea una barrera ni el punto final
            while not start:
                row = random.randint(0, ROWS - 1)
                col = random.randint(0, ROWS - 1)
                spot = grid[row][col]
                if not spot.is_barrier() and spot != end:
                    start = spot
                    start.make_start()  # Marca el punto de inicio en la cuadrícula

            # Bucle para seleccionar una posición final aleatoria adyacente a una barrera
            while not end:
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
                    # Se elige un punto final adyacente aleatorio que no sea una barrera ni el punto de inicio
                    end = random.choice([spot for spot in adjacent if not spot.is_barrier() and spot != start])
                    end.make_end()  # Marca el punto final en la cuadrícula

            # Si se presiona la tecla de espacio y se han definido el punto de inicio y el punto final
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    # Actualiza los vecinos de cada celda en la cuadrícula
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    # Ejecuta el algoritmo de búsqueda A* para encontrar el camino entre el punto de inicio y el punto final
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    pygame.time.wait(1000)  # Espera 1 segundos antes de continuar
                # Si se presiona la tecla 'c', se reinicia el punto de inicio, el punto final y la cuadrícula
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)