import pygame
import math

from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Se carga el archivo de la clase Cubo
import sys
sys.path.append('..')
from Carro import Carro
from Carro import Basura
screen_width = 700
screen_height = 700
#vc para el obser.
FOVY=60.0
ZNEAR=0.01
ZFAR=900.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X=300.0
EYE_Y=200.0
EYE_Z=300.0
CENTER_X=0
CENTER_Y=0
CENTER_Z=0
UP_X=0
UP_Y=1
UP_Z=0
#Variables para dibujar los ejes del sistema
X_MIN=-700
X_MAX=700
Y_MIN=-700
Y_MAX=700
Z_MIN=-700
Z_MAX=700
#Dimension del plano
DimBoard = 200

pygame.init()

#cubo = Cubo(DimBoard, 1.0)
carros = []
ncarros = 5

basuras = []
nbasuras = 10

textures = []
filename1 = "metalAmarillo.bmp"
filename2 = "cemento.bmp"
filename3 = "carro.bmp"
filename4 = "carroAtras.bmp"
filename5 = "carroVentana.bmp"
filename6 = "carroPuerta.bmp"
Theta  = 0
Direction = [300.0,200.0,300.0]
PI = 3.14159265359



def DegToRad(g):
    return ((g*PI)/180.0)

def LookAt():
    global EYE_X, EYE_Z
    radius = math.sqrt((EYE_X - CENTER_X)**2 + (EYE_Z - CENTER_Z)**2)
    new_angle = math.atan2(EYE_Z - CENTER_Z, EYE_X - CENTER_X) + math.radians(Theta)
    EYE_X = CENTER_X + radius * math.cos(new_angle)
    EYE_Z = CENTER_Z + radius * math.sin(new_angle)
    
def Axis():
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

def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
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
    Texturas(filename1)
    Texturas(filename2)
    Texturas(filename3)
    Texturas(filename4)
    Texturas(filename5)
    Texturas(filename6)
    for i in range(ncarros):
        carros.append(Carro(DimBoard, 2.0))
    for i in range(nbasuras):
        basuras.append(Basura(DimBoard))
        


def PlanoTexturizado():
    
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
    Axis()
    #Se dibuja el plano 
    PlanoTexturizado()
    for bas in basuras:
        bas.draw()
    for obj in carros:
        obj.drawCube(textures,0, 2, 3, 4, 5)
        obj.update()


done = False

#Mover aleatoriamente el vector de direccion


def Texturas(filepath):
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

Init()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if Theta > 359.0:
                    Theta = 0.0
                else:
                    Theta -= 1.0
                LookAt()
            if event.key == pygame.K_LEFT:
                if Theta < 1.0:
                    Theta = 360.0
                else:
                    Theta += 1.0 
                LookAt()
        
        glLoadIdentity()
        gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    
    display()

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()