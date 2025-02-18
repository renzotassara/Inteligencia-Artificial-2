import pygame
import math
from queue import PriorityQueue
import random

WIDTH = 1000
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.neighbors1 = []
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

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

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


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

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
                    neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()
            pass
    return False



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
    start1 = None
    end1 = None
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

            # quiero que el punto de inicio sea en un lugar aleatorio que no coincida con las barrera o el fin y que se definan en código, no con el mouse
            # Generate a random start position that is not a barrier or the end point

            while not start:
                row = random.randint(0, ROWS - 1)
                col = random.randint(0, ROWS - 1)
                spot = grid[row][col]
                row1 = random.randint(0, ROWS - 1)
                col1 = random.randint(0, ROWS - 1)
                spot1 = grid[row1][col1]
                if not spot.is_barrier() and spot != end and not spot1.is_barrier() and spot1 != end1:
                    start1 = spot1
                    start1.make_start()
                    start = spot
                    start.make_start()

            # Al codigo de abajo quiero agregarle que el punto final siempre esté adyacente a una barrera
            # Generate an end position but limited to adjacent positions to a barrier
            # But i dont want a random position, i want it to be a random adjacent position to a barrier
            # check the end position and if it is not a barrier, get the adjacent positions and choose one of them
            # as the end position

            # to this code add that the end position cant colide with a barrier or the start position

            while not end:
                row = random.randint(0, ROWS - 1)
                col = random.randint(0, ROWS - 1)
                spot = grid[row][col]
                row1 = random.randint(0, ROWS - 1)
                col1 = random.randint(0, ROWS - 1)
                spot1 = grid[row1][col1]
                if spot.is_barrier() and spot1.is_barrier():
                    # Get adjacent spots
                    # Choose a random up, down, right or left spot from a barrier

                    adjacent1 = []
                    adjacent = []
                    if row > 0:
                        adjacent.append(grid[row - 1][col])
                        adjacent1.append(grid[row1 - 1][col1])
                    if row < ROWS - 1:
                        adjacent.append(grid[row + 1][col])
                        adjacent1.append(grid[row1 + 1][col1])
                    if col > 0:
                        adjacent.append(grid[row][col - 1])
                        adjacent1.append(grid[row1][col1 - 1])
                    if col < ROWS - 1:
                        adjacent.append(grid[row][col + 1])
                        adjacent1.append(grid[row1][col1 + 1])
                    # Choose a random adjacent spot
                    end1 = random.choice([spot1 for spot1 in adjacent1 if not spot1.is_barrier() and spot1 != start1])
                    end1.make_end()
                    end = random.choice([spot for spot in adjacent if not spot.is_barrier() and spot != start])
                    end.make_end()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start1, end1)
                    # quiero esperar 2 segundos antes de que el segundo agente comience a buscar su camino
                    pygame.time.wait(1000)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    start1 = None
                    end1 = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)