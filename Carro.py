# Librerías
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import math

class Basura:
    def __init__(self, dim):
        self.radio = 5.0
        self.Position = [0.0, 2.0, 0.0]
        #Se inicializa las coordenadas de los vertices del cubo
        self.vertexCoords = [  
                   1,1,1,   1,1,-1,   1,-1,-1,   1,-1,1,
                  -1,1,1,  -1,1,-1,  -1,-1,-1,  -1,-1,1 ]
        
        #Vertice de los diferentes colores
        self.vertexColors = [ 
                   1,1,1,   1,0,0,   1,1,0,   0,1,0,
                   0,0,1,   1,0,1,   0,0,0,   0,1,1 ]

        self.elementArray = [
                  0,1,2,3, 0,3,7,4, 0,4,5,1,
                  6,2,1,5, 6,5,4,7, 6,7,3,2 ]
        
    
        self.DimBoard = dim
        #Se inicializa una posicion aleatoria en el tablero
        self.Position[0] = random.randint(-self.DimBoard, self.DimBoard)
        self.Position[2] = random.randint(-self.DimBoard, self.DimBoard)
    
    #AQUI CAMBIAR ESTE
    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(5,5,5)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertexCoords)
        glColorPointer(3, GL_FLOAT, 0, self.vertexColors)
        glDrawElements(GL_QUADS,24,GL_UNSIGNED_INT,self.elementArray)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glPopMatrix()
        
    #PARA USAR TEXTURAS COMO EN ESTE  
    # def draw(self,textura,id, id2, id3, id4, id5):
    #     glPushMatrix()
    #     glTranslatef(self.Position[0], self.Position[1], self.Position[2])
    #     glScaled(5,5,5)
    #     glColor3f(1.0, 1.0, 1.0)
    #     #Activar texturas
    #     glEnable(GL_TEXTURE_2D)
    #     #frente
    #     glBindTexture(GL_TEXTURE_2D, textura[id2])
    #     self.drawFace(-1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0)
    #     #derecha
    #     glBindTexture(GL_TEXTURE_2D, textura[id5])
    #     self.drawFace(1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0)
    #     #atrás
    #     glBindTexture(GL_TEXTURE_2D, textura[id3])
    #     self.drawFace(1.0, 1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0)
    #     #izquierda
    #     glBindTexture(GL_TEXTURE_2D, textura[id5])
    #     self.drawFace(-1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0)
    #     # Arriba
    #     glBindTexture(GL_TEXTURE_2D, textura[id4])
    #     self.drawFace(-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, -1.0)
    #      # Dibujar cubo a la derecha
    #     glDisable(GL_TEXTURE_2D)
    #     glPushMatrix()
    #     glColor3f(0.0,0.0,0.0)
    #     glTranslatef(1.5, 0.0, 0.0)  # Ajusta la traslación para el cubo a la derecha
    #     glRotatef(90,0,1,0)
    #     self.cilindro.draw()
    #     glPopMatrix()
    #     # Dibujar cubo a la izquierda
    #     glPushMatrix()
    #     glTranslatef(-1.5, 0.0, 0.0)  # Ajusta la traslación para el cubo a la izquierda
    #     glRotatef(90,0,1,0)
    #     self.cilindro.draw()
    #     glPopMatrix()
    #     glPushMatrix()
    #     glTranslatef(0.0, 1.5, -0.5)
    #     glScaled(0.5,0.5,0.5)
    #     glColor3f(1.0, 1.0, 1.0)
    #     #Activar texturas
    #     glEnable(GL_TEXTURE_2D)
    #     #frente
    #     glBindTexture(GL_TEXTURE_2D, textura[id4])
    #     self.drawFace(-1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0)
    #     #derecha
    #     glBindTexture(GL_TEXTURE_2D, textura[id4])
    #     self.drawFace(1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0)
    #     #atrás
    #     glBindTexture(GL_TEXTURE_2D, textura[id4])
    #     self.drawFace(1.0, 1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0)
    #     #izquierda
    #     glBindTexture(GL_TEXTURE_2D, textura[id4])
    #     self.drawFace(-1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0)
    #     # Arriba
    #     glBindTexture(GL_TEXTURE_2D, textura[id4])
    #     self.drawFace(-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, -1.0)
    #     glPopMatrix()
    #     glPopMatrix()

    def update(self):
        self.Position[0] = 0.0
        self.Position[2] = 0.0

class Cilindro:
    def __init__(self, radio, altura, slices=30, stacks=30):
        self.radio = radio
        self.altura = altura
        self.slices = slices
        self.stacks = stacks

    def draw(self):
        glPushMatrix()
        glColor3f(0.0, 0.0, 0.0)  # Color del cilindro (blanco en este caso)

        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluQuadricTexture(quadric, GL_TRUE)
        
        # Dibujar la parte lateral del cilindro
        gluCylinder(quadric, self.radio, self.radio, self.altura, self.slices, self.stacks)
        
        # Tapas del cilindro
        glPushMatrix()
        glTranslatef(0.0, 0.0, self.altura)
        gluDisk(quadric, 0.0, self.radio, self.slices, 1)
        glPopMatrix()

        gluDeleteQuadric(quadric)
        glPopMatrix()

class Carro:
    
    def __init__(self, dim, vel):
        self.radio = 5.0
        self.Position = [0.0, 5.0, 0.0]
        self.Direction = [0.0, 5.0, 0.0]
        self.cilindro = Cilindro(radio=0.5, altura=0.5)

        #Se inicializa las coordenadas de los vertices del cubo
        self.vertexCoords = [  
                   1,1,1,   1,1,-1,   1,-1,-1,   1,-1,1,
                  -1,1,1,  -1,1,-1,  -1,-1,-1,  -1,-1,1 ]
        
        #Vertice de los diferentes colores
        self.vertexColors = [ 
                   1,1,1,   1,0,0,   1,1,0,   0,1,0,
                   0,0,1,   1,0,1,   0,0,0,   0,1,1 ]

        self.elementArray = [
                  0,1,2,3, 0,3,7,4, 0,4,5,1,
                  6,2,1,5, 6,5,4,7, 6,7,3,2 ]
        
    
        self.DimBoard = dim
        #Se inicializa una posicion aleatoria en el tablero
        self.Position[0] = random.randint(-self.DimBoard, self.DimBoard)
        self.Position[2] = random.randint(-self.DimBoard, self.DimBoard)
        
        #Inicializar las coordenadas (x,y,z) del cubo en el tablero
        #almacenandolas en el vector Position
        #...
        #Se inicializa un vector de direccion aleatorio
        self.Direction[0] = random.randint(-self.DimBoard, self.DimBoard)
        self.Direction[1] = random.randint(-self.DimBoard, self.DimBoard)
        self.Direction[2] = random.randint(-self.DimBoard, self.DimBoard)
        #El vector aleatorio debe de estar sobre el plano XZ (la altura en Y debe ser fija)
        #Se normaliza el vector de direccion
        m = math.sqrt(self.Direction[0]*self.Direction[0] + self.Direction[1]*self.Direction[1] + self.Direction[2]*self.Direction[2])
        self.Direction[0] /= m
        self.Direction[1] /= m
        self.Direction[2] /= m
        #...
        #Se cambia la maginitud del vector direccion con la variable vel
        #...
        self.Direction[0] *= vel
        self.Direction[1] *= vel
        self.Direction[2] *= vel

    def update(self):
        #Se debe de calcular la posible nueva posicion del cubo a partir de su
        #posicion acutual (Position) y el vector de direccion (Direction)
        #...
        
        #Se debe verificar que el objeto cubo, con su nueva posible direccion
        #no se salga del plano actual (DimBoard)
        #...
    
        new_x = self.Position[0] + self.Direction[0]
        new_z = self.Position[2] + self.Direction[2]

        #print ("(X =", self.Position[0], ", Z =", self.Position[2],")")

        if (abs(new_x) <= self.DimBoard):
            self.Position[0] = new_x
        else: 
            self.Direction[0] *= -1.0
            self.Position[0] += self.Direction[0]
        

        if (abs(new_z) <= self.DimBoard):
            self.Position[2] = new_z
        else: 
            self.Direction[2] *= -1.0
            self.Position[2] += self.Direction[2]
        
        #print ("(X =", self.Position[0], ", Z =", self.Position[2],")")

    def drawFace(self, x1,  y1, z1, x2, y2, z2,x3, y3, z3,x4,  y4,  z4):
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x1, y1, z1)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(x2, y2, z2)

        glTexCoord2f(1.0, 1.0)
        glVertex3f(x3, y3, z3)

        glTexCoord2f(1.0, 0.0)
        glVertex3f(x4, y4, z4)
        glEnd()
        
    # Dibujado base
    # def draw(self):
    #     glPushMatrix()
    #     glTranslatef(self.Position[0], self.Position[1], self.Position[2])
    #     glScaled(5,5,5)
    #     #Se dibuja el cubo
    #     #...
    #     glEnableClientState(GL_VERTEX_ARRAY)
    #     glEnableClientState(GL_COLOR_ARRAY)
    #     glVertexPointer(3, GL_FLOAT, 0, self.vertexCoords)
    #     glColorPointer(3, GL_FLOAT, 0, self.vertexColors)
    #     glDrawElements(GL_QUADS,24,GL_UNSIGNED_INT,self.elementArray)
    #     glDisableClientState(GL_VERTEX_ARRAY)
    #     glDisableClientState(GL_COLOR_ARRAY)
    #     glPopMatrix()

    def drawCar(self,textura,id, id2, id3, id4, id5):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(5,5,5)
        glColor3f(1.0, 1.0, 1.0)
        #Activar texturas
        glEnable(GL_TEXTURE_2D)
        #frente
        glBindTexture(GL_TEXTURE_2D, textura[id2])
        self.drawFace(-1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0)
        #derecha
        glBindTexture(GL_TEXTURE_2D, textura[id5])
        self.drawFace(1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0)
        #atrás
        glBindTexture(GL_TEXTURE_2D, textura[id3])
        self.drawFace(1.0, 1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0)
        #izquierda
        glBindTexture(GL_TEXTURE_2D, textura[id5])
        self.drawFace(-1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0)
        # Arriba
        glBindTexture(GL_TEXTURE_2D, textura[id4])
        self.drawFace(-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, -1.0)
         # Dibujar cubo a la derecha
        glDisable(GL_TEXTURE_2D)
        glPushMatrix()
        glColor3f(0.0,0.0,0.0)
        glTranslatef(1.5, 0.0, 0.0)  # Ajusta la traslación para el cubo a la derecha
        glRotatef(90,0,1,0)
        self.cilindro.draw()
        glPopMatrix()
        # Dibujar cubo a la izquierda
        glPushMatrix()
        glTranslatef(-1.5, 0.0, 0.0)  # Ajusta la traslación para el cubo a la izquierda
        glRotatef(90,0,1,0)
        self.cilindro.draw()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0.0, 1.5, -0.5)
        glScaled(0.5,0.5,0.5)
        glColor3f(1.0, 1.0, 1.0)
        #Activar texturas
        glEnable(GL_TEXTURE_2D)
        #frente
        glBindTexture(GL_TEXTURE_2D, textura[id4])
        self.drawFace(-1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0)
        #derecha
        glBindTexture(GL_TEXTURE_2D, textura[id4])
        self.drawFace(1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0)
        #atrás
        glBindTexture(GL_TEXTURE_2D, textura[id4])
        self.drawFace(1.0, 1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0)
        #izquierda
        glBindTexture(GL_TEXTURE_2D, textura[id4])
        self.drawFace(-1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0)
        # Arriba
        glBindTexture(GL_TEXTURE_2D, textura[id4])
        self.drawFace(-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, -1.0)
        glPopMatrix()
        glPopMatrix()
    
    def buscaColision(self,basuras):
        for basura in basuras:  
            dx = self.Position[0] - basura.Position[0]
            dz = self.Position[2] - basura.Position[2]
            distancia = math.sqrt(dx*dx + dz*dz)
            if distancia < self.radio + basura.radio:
                print("Encontrado")
                basura.update()
