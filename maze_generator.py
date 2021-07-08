import pygame
from pygame.locals import *
import sys
import random

# Maze generation using Wilson's Algorithim

pygame.init()

WIDTH, HEIGHT = 400, 400
ROWS, COLS = 20, 20
CELL_WIDTH = WIDTH // ROWS
WHITE = (255, 255, 255)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wilson's Algorithm")

cells = []

def index(i: int, j: int) -> int:
    if 0 <= i < ROWS and 0 <= j < COLS:
        return ROWS * i + j
    return -1


class Cell:
    def __init__(self, i: int, j: int) -> None:
        self.walls = [True, True, True, True]
        self.i = i 
        self.j = j 

    def show(self) -> None:
        x = self.i * CELL_WIDTH
        y = self.j * CELL_WIDTH

        if self.walls[0]:
            pygame.draw.line(WIN, WHITE, (x, y), (x + CELL_WIDTH, y))
        if self.walls[1]:
            pygame.draw.line(WIN, WHITE, (x + CELL_WIDTH, y), (x + CELL_WIDTH, y + CELL_WIDTH))
        if self.walls[2]:
            pygame.draw.line(WIN, WHITE, (x + CELL_WIDTH, y + CELL_WIDTH), (x, y + CELL_WIDTH))
        if self.walls[3]:
            pygame.draw.line(WIN, WHITE, (x, y + CELL_WIDTH), (x, y))

    def restore_wall(self) -> None:
        self.walls[0] = True
        self.walls[1] = True
        self.walls[2] = True
        self.walls[3] = True

    def generate_options(self, path: list) -> list:
        options = []

        top = index(self.i - 1, self.j)
        right = index(self.i, self.j + 1)
        bottom = index(self.i + 1, self.j)
        left = index(self.i, self.j - 1)

        if (top != -1 and top != path[-1]):
            options.append((self.i - 1, self.j))
        if (right != -1 and right != path[-1]):
            options.append((self.i, self.j + 1))
        if (bottom != -1 and bottom != path[-1]):
            options.append((self.i + 1, self.j))
        if (left != -1 and left != path[-1]):
            options.append((self.i, self.j - 1))
        
        return options


def remove_walls(a: Cell, b: Cell) -> None:
    i = a.i - b.i
    j = a.j - b.j

    if i == -1:
        a.walls[1] = False
        b.walls[3] = False
    elif i == 1:
        a.walls[3] = False
        b.walls[1] = False

    if j == -1:
        a.walls[2] = False
        b.walls[0] = False
    elif j == 1:
        a.walls[0] = False
        b.walls[2] = False

def restore_walls(arr: list) -> None:
    for c in arr:
        cells[index(c[0], c[1])].restore_wall()

def main():
    vertices = []
    maze = []

    for i in range(ROWS):
        for j in range(COLS):
            cells.append(Cell(i, j))
            vertices.append((i, j))
    
    first_cell = random.choice(vertices) # pick our first cell for the maze
    maze.append(first_cell)
    vertices.remove(first_cell)

    def random_walk():
        path = []
        coords = random.choice(vertices)
        path.append(coords)
        while coords not in maze: # perform random walk until we reach cell in maze
            curr = cells[index(coords[0], coords[1])]
            options = curr.generate_options(path)
            option = random.choice(options)
            if len(options) > 1 and option in path:
                options.remove(option)
                option = random.choice(options)
            remove_walls(curr, cells[index(option[0], option[1])])
            coords = option
            if coords in path:
                for i in range(len(path)):
                    if path[i] == coords:
                        restore_walls(path[i:])
                        path = path[:i]
                        if len(path) != 0:
                            coords = path[-1]
                        else:
                            path.append(coords)
                        break
            else:
                path.append(coords)
        
        maze.extend(path)
        for i in range(len(path)-1):
            vertices.remove(path[i])
        
    while len(vertices) != 0:
        random_walk()
    
    for i in range(ROWS):
        for j in range(COLS):
            cells[index(i, j)].show()

    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
       
main()
