import sys
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

sys.path.append('..')
from models import Carro
from models import Basura

# Set up display and camera
screen_width = 700
screen_height = 700

FOVY = 60.0
ZNEAR = 0.01
ZFAR = 900.0

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

DimBoard = 200

pygame.init()

carros = []
ncarros = 4

basuras = []
nbasuras = 10

robotpositions = [
    (DimBoard,-DimBoard),
    (-DimBoard,-DimBoard),
    (DimBoard,DimBoard),
    (-DimBoard,DimBoard)
]

velocidad = 2.0

textures = []
filename1 = "src/img/metalAmarillo.bmp"
filename2 = "src/img/cemento.bmp"
filename3 = "src/img/carro.bmp"
filename4 = "src/img/carroAtras.bmp"
filename5 = "src/img/carroVentana.bmp"
filename6 = "src/img/carroPuerta.bmp"
filename7 = "src/img/basura.bmp"

Theta  = 0
Direction = [300.0,200.0,300.0]
ELEVATION_ANGLE = 0.0

def DegToRad(g):
    return ((g*math.pi)/180.0)

def LookAt(vertical):
    global EYE_X, EYE_Y, EYE_Z
    radius = math.sqrt((EYE_X - CENTER_X)**2 + (EYE_Z - CENTER_Z)**2)
    new_angle = math.atan2(EYE_Z - CENTER_Z, EYE_X - CENTER_X) + math.radians(Theta)
    EYE_X = CENTER_X + radius * math.cos(new_angle)
    EYE_Z = CENTER_Z + radius * math.sin(new_angle)
    if vertical:
        EYE_Y = CENTER_Y + radius * math.sin(math.radians(ELEVATION_ANGLE))

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

    LoadTexture(filename1)
    LoadTexture(filename2)
    LoadTexture(filename3)
    LoadTexture(filename4)
    LoadTexture(filename5)
    LoadTexture(filename6)
    LoadTexture(filename7)

    for i in range(ncarros):
        carros.append(Carro(DimBoard, velocidad, robotpositions[i], i))
    for i in range(nbasuras):
        basuras.append(Basura(DimBoard))

def DisplayPlane():

    glColor3f(230, 230, 230)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-DimBoard, 0.0, -DimBoard)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(DimBoard, 0.0, -DimBoard)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(DimBoard, 0.0, DimBoard)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-DimBoard, 0.0, DimBoard)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def display():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    DisplayAxis()
    DisplayPlane()

    for bas in basuras:
        # bas.draw(textures,6)
        bas.drawTrash(textures,6)
    for obj in carros:
        obj.drawCar(textures,0, 2, 3, 4, 5)
        obj.update()
        #Si la condición de la basura es 0 (buscando)
        #pasar por la función buscaColision
        if obj.condition == 0:
            obj.buscaColision(basuras)

done = False

#Mover aleatoriamente el vector de direccion
def LoadTexture(filepath):
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image, "RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,w,h,0,GL_RGBA,GL_UNSIGNED_BYTE,image_data)
    glGenerateMipmap(GL_TEXTURE_2D)

def main():
    InitSimulation()
    done = False
    global Theta, ELEVATION_ANGLE
    while not done:
        for event in pygame.event.get():
            vertical = False
            Theta = 0.0
            if event.type == pygame.KEYDOWN:
                if Theta > 359.0:
                    Theta = 0.0
                elif Theta < 1.0:
                    Theta = 360.0
                if event.key==pygame.K_RIGHT:
                    Theta += 1.0
                if event.key == pygame.K_LEFT:
                    Theta -= 1.0
                elif event.key == pygame.K_UP:
                    ELEVATION_ANGLE += 1.0
                    vertical = True
                elif event.key == pygame.K_DOWN:
                    ELEVATION_ANGLE -= 1.0
                    vertical = True
            elif event.type == pygame.QUIT:
                done = True

            LookAt(vertical)
            glLoadIdentity()
            gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)

        display()
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()