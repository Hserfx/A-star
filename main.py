import pygame as pg
import sys
import numpy as np



rects = np.empty((12,16), dtype=object)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

GRAY = (60, 60, 60)
GRAY_2 = (100, 100, 100)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

walls = []
path = []
sprites = []
clicked_sprite = ''
start = False
end = False
walled = False


def restart():
    global path, sprites, clicked_sprite, start, end, walled, walls
    path = []
    sprites = []
    walls = []
    clicked_sprite = ''
    start = False
    end = False
    walled = False

class Node:
    def __init__(self, x, y, fx, came_from = None):
        self.x = x
        self.y = y
        self.fx = fx
        self.rect = pg.Rect(rects[self.y][self.x][0], rects[self.y][self.x][1], blocksize-2, blocksize-2)
        self.came_from = came_from

def find_idx(array, value):
    i = 0
    j = 0
    for x in array[0]:
        for y in array:
            if value == array[j, i]:
                return (i, j)
            j += 1
        i += 1
        j = 0


def check_fx(point, goal):
    return abs(point[0] - goal[0]) + abs(point[1] - goal[1])


def create_path(came_from):
    while came_from is not None:
        path.append(came_from)
        pg.draw.rect(SCREEN, BLUE, came_from.rect)
        pg.display.flip()
        came_from = came_from.came_from
    return path

def A_Algorithm(maze, start, goal):
    closed_set = []
    optimal = check_fx(start, goal)
    st = Node(start[0], start[1], optimal)
    open_set = [st]
    x = st


    while 1:
        open_set.sort(key=lambda a: a.fx)
        i = open_set[0]
        closed_set.append(i.rect)
        x = i

        for nx, ny in [(0,1),(0,-1),(1,0),(-1,0)]:

            if x.x+nx > 15 or x.y+ny > 11 or x.y+ny < 0 or x.x < 0:
                continue
            fx = check_fx((x.x+nx, x.y+ny), goal)

            if fx == 0:
                return create_path(x)

            neighbour = Node(x.x+nx, x.y+ny, fx, came_from = x)



            if neighbour in open_set or neighbour.rect in walls or neighbour.rect in closed_set:
                continue

            open_set.append(neighbour)

        open_set.remove(x)


def drawGrid():
    global blocksize
    blocksize = 50
    x_c = 0
    y_c = 0
    for x in range(0, WINDOW_WIDTH, blocksize):
        for y in range(0, WINDOW_HEIGHT, blocksize):
            rect = pg.Rect(x, y, blocksize-2, blocksize-2)
            if rect == clicked_sprite and not start or rect == start:
                pg.draw.rect(SCREEN, RED, rect)
            elif rect == clicked_sprite and rect != start or rect == end:
                pg.draw.rect(SCREEN, GREEN, rect)
            elif rect in path:
                pg.draw.rect(SCREEN, BLUE, rect)
            elif rect in walls:
                pg.draw.rect(SCREEN, GRAY_2, rect)
            else:
                pg.draw.rect(SCREEN, BLACK, rect)

            if not rect in sprites:
                sprites.append(rect)

            rects[y_c, x_c] = (rect.x, rect.y)

            y_c += 1
        x_c += 1
        y_c = 0

if __name__ == '__main__':
    pg.init()
    SCREEN = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pg.time.Clock()
    SCREEN.fill(GRAY)

    while True:
        drawGrid()
        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == 13:
                    if not start:
                        start = clicked_sprite
                        walled = True
                    elif walled:
                        walled = False
                    elif end:
                        path = A_Algorithm(rects, find_idx(rects, (start.x, start.y)), find_idx(rects, (end.x, end.y)))
                    else:
                        end = clicked_sprite
                if event.key == 114:
                    restart()

            if pg.mouse.get_pressed()[0] and not end:
                pos = pg.mouse.get_pos()

                for s in sprites:
                    if s.collidepoint(pos):
                        clicked_sprite = s
                    if walled:
                        if not clicked_sprite in walls or clicked_sprite != start:
                            walls.append(clicked_sprite)

        pg.display.flip()
