
import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_i:
            RED = (0, 255, 255)
            GREEN = (255, 0, 255)
            BLUE = (255, 0, 255)
            YELLOW = (0, 0, 255)
            WHITE = (0, 0, 0)
            BLACK = (255, 255, 255)
            PURPLE = (0, 128, 0)
            ORANGE = (0, 90 ,255)
            GREY = (128, 128, 128)
            TURQUOISE = (191, 31, 47)

class Node:
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
        return self.color == RED #Color of spaces made along the path, being cut off by the border (is_open)

    def is_open(self):
        return self.color == GREEN #Color of the border which cuts off the is_closed color from spreading to the whole map

    def is_barrier(self):
        return self.color == BLACK #Color of barrier path doesn't go through

    def is_start(self):
        return self.color == ORANGE #Color of start point

    def is_end(self):
        return self.color == PURPLE #Color of end point

    def reset(self):
        self.color = WHITE #Color of the grid on restart

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = PURPLE

    def make_path(self):
        self.color = TURQUOISE #Color of Path made

    def draw(self, win): #Draw a rectangle
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # Down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # Up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # Right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # Left
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2): #Hurustic function used to guess the length of the distance. Determined by absolute values (Removes -ve's) of a pair of co-ordinates
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw): #Purple path shows quickest route
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end): #Our algorithm to determine quickets path
    count = 0
    open_set = PriorityQueue() #Priorises smallest element first, i.e: shows smallest F score
    open_set.put((0, count, start))
    came_from = {} #Dict
    g_score = {node: float("inf") for row in grid for node in row}# Recall the table from earlier, this puts infinity in all g-score boxes
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}# Same as before, but with f-scores
    f_score[start] = h(start.get_pos(), end.get_pos()) #Huristic func for the guessing feature

    open_set_hash = {start} #Keeps check of things in Priority Queue

    while not open_set.empty(): #All possibilities considered
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #If red x is pressed
                pygame.quit()

        current = open_set.get()[2] #The algorithm stores the F-score, count and node. This gets Node i.e: square
        open_set_hash.remove(current) #And removes it

        if current == end: #If removed node was the endpoint (Path found)
            reconstruct_path(came_from, end, draw) #Draws purple path
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 #We're going 1 extra node over, as neighbours are 1 square away

            if temp_g_score < g_score[neighbor]: #If path is better:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())# Gives row / col of both
                if neighbor not in open_set_hash: #If neighbour not in dict
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start: #If node we just saw is not the start, make it red
            current.make_closed()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width): #draw is redefined
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win) #Redraws map

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # Left pressed
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # Right pressed
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN: #If key pressed
                if event.key == pygame.K_SPACE and start and end: #If key was spacebar and there is a start / end
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end) #Lambda allows you to create a function in one line

                if event.key == pygame.K_c: #If c is pressed
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)
