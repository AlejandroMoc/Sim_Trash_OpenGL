import math
import pygame

from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import (
    glShadeModel, glLineWidth, glColor3f, glBegin, glVertex3f, glEnd, glMatrixMode,
    glLoadIdentity, glClearColor, glEnable, glPolygonMode, glBindTexture, glTexParameteri,
    glTexImage2D, glGenerateMipmap, glClear, glDisable, glVertex3d, glTexCoord2f, glGenTextures,
    GL_FLAT, GL_LINES, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_PROJECTION,
    GL_MODELVIEW, GL_DEPTH_TEST, GL_FRONT_AND_BACK, GL_FILL, GL_TEXTURE_2D,
    GL_CLAMP, GL_LINEAR, GL_RGBA, GL_UNSIGNED_BYTE, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T,
    GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_QUADS
)
from OpenGL.GLU import (
    gluPerspective, gluLookAt
)

from models import Carro
from models import Basura

# Set up display and camera
screen_width = 700
screen_height = 700

FOVY = 60.0
ZNEAR = 0.01
ZFAR = 900.0

BASE_RADIUS = 400.0
BASE_HEIGHT = 150.0
ELEVATION_ANGLE = 0.0
Theta = 45.0
EYE_Y = BASE_HEIGHT

EYE_X = 300.0
EYE_Y = 200.0
EYE_Z = 300.0
CENTER_X = 0
CENTER_Y = 0
CENTER_Z = 0
UP_X = 0
UP_Y = 1
UP_Z = 0

# Set up axis and plane dimensions
X_MIN = -700
X_MAX = 700
Y_MIN = -700
Y_MAX = 700
Z_MIN = -700
Z_MAX = 700

board_limit = 200

pygame.init()

car_list = []
car_number = 4

trash_list = []
trash_number = 10

robot_positions = [
    (board_limit,-board_limit),
    (-board_limit,-board_limit),
    (board_limit,board_limit),
    (-board_limit,board_limit)
]

velocity = 2.0

texture_list = []
filename_1 = "src/img/metalAmarillo.bmp"
filename_2 = "src/img/cemento.bmp"
filename_3 = "src/img/carro.bmp"
filename_4 = "src/img/carroAtras.bmp"
filename_5 = "src/img/carroVentana.bmp"
filename_6 = "src/img/carroPuerta.bmp"
filename_7 = "src/img/basura.bmp"


def DegToRad(g):
    return ((g*math.pi)/180.0)

def LookAt():
    global EYE_X, EYE_Y, EYE_Z
    rad = math.radians(Theta)
    EYE_X = CENTER_X + BASE_RADIUS * math.cos(rad)
    EYE_Z = CENTER_Z + BASE_RADIUS * math.sin(rad)
    EYE_Y = BASE_HEIGHT + ELEVATION_ANGLE


def DisplayAxis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)

    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()

    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()

    #Z axis in blue
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)


def InitSimulation():
    screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: Carros recogedores")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    LoadTexture(filename_1)
    LoadTexture(filename_2)
    LoadTexture(filename_3)
    LoadTexture(filename_4)
    LoadTexture(filename_5)
    LoadTexture(filename_6)
    LoadTexture(filename_7)

    for i in range(car_number):
        car_list.append(Carro(board_limit, velocity, robot_positions[i], i))
    for i in range(trash_number):
        trash_list.append(Basura(board_limit))

def DisplayPlane():

    glColor3f(230, 230, 230)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_list[1])
    glBegin(GL_QUADS)

    glTexCoord2f(0.0, 0.0)
    glVertex3d(-board_limit, 0.0, -board_limit)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(board_limit, 0.0, -board_limit)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(board_limit, 0.0, board_limit)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-board_limit, 0.0, board_limit)

    glEnd()
    glDisable(GL_TEXTURE_2D)

def display():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    DisplayAxis()
    DisplayPlane()

    for trash in trash_list:
        trash.drawTrash(texture_list,6)

    for car in car_list:
        car.drawCar(texture_list,0, 2, 3, 4, 5)
        car.update()
        # If the trash condition is 0 (searching)
        # call the buscaColision function
        if car.condition == 0:
            car.buscaColision(trash_list)

done = False


def LoadTexture(filepath):
    # Generate a new texture ID and add it to the texture list
    texture_list.append(glGenTextures(1))
    id = len(texture_list) - 1

    # Bind the texture and set parameters
    glBindTexture(GL_TEXTURE_2D, texture_list[id])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    # Load the image and convert it to a suitable format
    image = pygame.image.load(filepath).convert()
    width, height = image.get_rect().size
    image_data = pygame.image.tostring(image, "RGBA")

    # Upload the image data to the currently bound texture
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    # Generate mipmaps for the texture
    glGenerateMipmap(GL_TEXTURE_2D)

def HandleKeyEvent(event):
    global Theta, ELEVATION_ANGLE, CENTER_X, CENTER_Z
    move_step = 10.0

    if event.key == pygame.K_RIGHT:
        Theta += 2.0
        if Theta > 359.0:
            Theta -= 360.0
    elif event.key == pygame.K_LEFT:
        Theta -= 2.0
        if Theta < 0.0:
            Theta += 360.0
    elif event.key == pygame.K_UP:
        ELEVATION_ANGLE += 5.0
    elif event.key == pygame.K_DOWN:
        ELEVATION_ANGLE -= 5.0

    # WASD camera translation
    elif event.key == pygame.K_w:
        CENTER_X -= move_step * math.cos(math.radians(Theta))
        CENTER_Z -= move_step * math.sin(math.radians(Theta))
    elif event.key == pygame.K_s:
        CENTER_X += move_step * math.cos(math.radians(Theta))
        CENTER_Z += move_step * math.sin(math.radians(Theta))
    elif event.key == pygame.K_d:
        CENTER_X += move_step * math.cos(math.radians(Theta - 90))
        CENTER_Z += move_step * math.sin(math.radians(Theta - 90))
    elif event.key == pygame.K_a:
        CENTER_X += move_step * math.cos(math.radians(Theta + 90))
        CENTER_Z += move_step * math.sin(math.radians(Theta + 90))

    elif event.key == pygame.K_q:
        ELEVATION_ANGLE -= move_step
    elif event.key == pygame.K_r:
        ELEVATION_ANGLE += move_step

def main():
    global Theta, ELEVATION_ANGLE
    Theta = 45.0
    ELEVATION_ANGLE = 0.0
    InitSimulation()
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                HandleKeyEvent(event)
            elif event.type == pygame.QUIT:
                done = True

        LookAt()
        glLoadIdentity()
        gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)

        display()
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()


if __name__ == "__main__":
    main()