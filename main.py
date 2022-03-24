from ast import Raise
from cgitb import text
import pygame as pg
import sys
import numpy as np

x_size = 32
y_size = 24

rects = np.empty((y_size,x_size), dtype=object)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

blocksize = WINDOW_WIDTH//x_size

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
        came_from = came_from.came_from

    return path

def A_Algorithm(maze, start, goal):

    closed_set = []
    optimal = check_fx(start, goal)
    st = Node(start[0], start[1], optimal)
    open_set = [st]
    x = st


    while len(open_set) > 0:
        exist = False
        open_set.sort(key=lambda a: a.fx)
        i = open_set[0]
        closed_set.append(i.rect)
        pg.draw.rect(SCREEN, BLUE, i.rect)
        pg.display.update(i.rect)
        x = i
        print(len(open_set))

        for nx, ny in [(0,1),(0,-1),(1,0),(-1,0)]:
            if x.x+nx > x_size-1 or x.y+ny > y_size-1 or x.y+ny < 0 or x.x < 0:
                continue

            fx = check_fx((x.x+nx, x.y+ny), goal)

            if fx == 0:
                return create_path(x)

            neighbour = Node(x.x+nx, x.y+ny, fx, came_from = x)





            if neighbour.rect in walls or neighbour.rect in closed_set:
                continue

            for n in open_set:
                if n.rect == neighbour.rect:
                    exist = True

            if not exist:
                open_set.append(neighbour)

        open_set.remove(x)

    return [None]

def drawGrid():
    global blocksize
    SCREEN.fill(GRAY)

    x_c = 0
    y_c = 0
    for x in range(WINDOW_WIDTH // blocksize):
        for y in range(WINDOW_HEIGHT // blocksize):
            rect = pg.Rect(x*blocksize, y*blocksize, blocksize-2, blocksize-2)
            if rect == clicked_sprite and not start or rect == start:
                pg.draw.rect(SCREEN, RED, rect)
            elif rect == clicked_sprite and rect != start and not walled or rect == end:
                pg.draw.rect(SCREEN, GREEN, rect)
            elif rect in path:
                pg.draw.rect(SCREEN, BLUE, rect)
            elif rect in walls:
                pg.draw.rect(SCREEN, GRAY_2, rect)
            elif path == [None]:
                SCREEN.blit(path_text,(0, 0))
                pg.draw.rect(SCREEN, BLACK, rect)
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
    main_font = pg.font.SysFont('Comic Sans MS', 30)
    path_text = main_font.render('End node is not accessible', False, RED)
    SCREEN = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pg.time.Clock()


    while True:
        CLOCK.tick(200)
        print(CLOCK.get_fps())
        drawGrid()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
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

            elif pg.mouse.get_pressed()[0] and not end:
                pos = pg.mouse.get_pos()
                clicked_sprite = ''
                for s in sprites:
                    if s.collidepoint(pos):
                        clicked_sprite = s
                        if walled:
                            if not clicked_sprite in walls and clicked_sprite != start:

                                walls.append(clicked_sprite)
                                break

            elif pg.mouse.get_pressed()[2] and not end:
                pos = pg.mouse.get_pos()
                print(pos)
                for s in walls:
                    print(s)
                    if s.collidepoint(pos):
                        walls.remove(s)

        pg.display.update()
