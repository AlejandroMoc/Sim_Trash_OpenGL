# Librerías
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import math

def distancia_entre_puntos(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

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

class Basura:
    RECOLECTADA = 0
    TIRADA = 1
    def __init__(self, dim):
        self.angulo = 0
        self.radio = 7.0
        self.Position = [0.0, 2.0, 0.0]
        #Se inicializa las coordenadas de los vertices del cubo
        self.vertexCoords = [  
                   1,1,1,   1,1,-1,   1,-1,-1,   1,-1,1,
                  -1,1,1,  -1,1,-1,  -1,-1,-1,  -1,-1,1 ]
        
        #Colores de los vertices
        self.vertexColors = [ 
                   1,1,1,   1,1,1,   1,1,1,   1,1,1,
                   1,1,1,   1,1,1,   1,1,1,   1,1,1 ]
        
        self.vertexColorful = [ 
                   1,1,1,   1,0,0,   1,1,0,   0,1,0,
                   0,0,1,   1,0,1,   0,0,0,   0,1,1 ]

        self.elementArray = [
                  0,1,2,3, 0,3,7,4, 0,4,5,1,
                  6,2,1,5, 6,5,4,7, 6,7,3,2 ]
        
        self.DimBoard = dim
        #Posicion aleatoria
        self.Position[0] = random.randint(-self.DimBoard, self.DimBoard)
        self.Position[2] = random.randint(-self.DimBoard, self.DimBoard)
        self.condition = self.TIRADA
    
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
      
    #AQUI CAMBIAR ESTE
    def draw(self, textura, id):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(5,5,5)
        glColor3f(1.0, 1.0, 1.0)
        # #Activar texturas
        # glEnable(GL_TEXTURE_2D)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glBindTexture(GL_TEXTURE_2D, textura[id])
        glVertexPointer(3, GL_FLOAT, 0, self.vertexCoords)
        glColorPointer(3, GL_FLOAT, 0, self.vertexColors)
        glDrawElements(GL_QUADS,24,GL_UNSIGNED_INT,self.elementArray)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glPopMatrix()
        
    #PARA USAR TEXTURAS COMO EN ESTE  
    def drawTrash(self,textura,id):
        
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(5,5,5)
        glRotatef(self.angulo, 0, 1, 0)
        glColor3f(1.0, 1.0, 1.0)
        
        #Activar texturas
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textura[id])
        self.drawFace(-1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0)
        self.drawFace(1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0)
        self.drawFace(1.0, 1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0)
        self.drawFace(-1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0)
        self.drawFace(-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, -1.0)
        glDisable(GL_TEXTURE_2D)
        
        glPopMatrix()
    
    def update(self, pos):
        self.Position[0] = pos[0]
        self.Position[1] = pos[1] + 13.0
        self.Position[2] = pos[2]

    def centrar(self):
        self.Position[0] = 0.0
        self.Position[1] = 2.0
        self.Position[2] = 0.0

class Carro:
    BUSCANDO = 0
    CARGADO = 1
    REGRESANDO = 2
    def __init__(self, dim, vel, pos, id):
        self.id = id
        self.condition = self.BUSCANDO
        self.radio = 7.0
        self.Position = [0.0, 5.0, 0.0]
        self.Direction = [0.0, 5.0, 0.0]
        self.cilindro = Cilindro(radio=0.5, altura=0.5)

        self.DimBoard = dim
        
        #Ultima basura encontrada
        self.basuraPos = None
        self.basura = None
                
        self.Position[0] = pos[0]
        self.Position[2] = pos[1]

        self.Direction[0] = 1.0
        self.Direction[1] = 0.0
        self.Direction[2] = 1.0

        self.Direction[0] *= vel
        self.Direction[1] *= vel
        self.Direction[2] *= vel
        
        self.ZigzagDir = [1,1]
        self.contadorSubida = 0
        
        self.angulo = 0
        
        if self.id == 0:
            # self.angulo = 90
            for i in range(5):
                self.angulo += 18
        elif self.id == 1:
            # self.angulo = 90
            for i in range(5):
                self.angulo += 18
        elif self.id == 2:
            # self.angulo = -90
            self.angulo = 0
            for i in range(5):
                self.angulo -= 18
        elif self.id == 3:
            # self.angulo = 90
            for i in range(5):
                self.angulo += 18
        else:
            self.angulo = 0
            
        self.AlturaPlataforma = -1.5
        
    def update(self):
        x,z = self.Position[0],self.Position[2]
        if self.condition == self.BUSCANDO:
            
            #Intentos raro de hacer que girase
            # if self.id == 0:
            #     for i in range(5):
            #         #Primeros movimientos
            #         if x < 200 and self.ZigzagDir[0] == 1:
            #             next_move = (x + self.Direction[0], z)
            #         elif x == 200 and self.ZigzagDir[0] == 1:
            #             if (z == 0 - self.Direction[2]):
            #                 return
            #             else:
            #                 next_move = (x, z + self.Direction[2])
            #                 self.contadorSubida += 1
            #                 if self.contadorSubida == 1:
            #                     # self.angulo += 90
            #                     # for i in range(1):
            #                     #     self.angulo += 18
            #                     self.angulo += 18
            #                 if self.contadorSubida == 10:  
            #                     self.ZigzagDir = [-1, 1]
            #                     # self.angulo += 90
            #                     # for i in range(1):
            #                     #     self.angulo += 18
            #                     self.angulo += 18
            #                     self.contadorSubida = 0
            #         #Segundos movimientos
            #         elif x > 15 and self.ZigzagDir[0] == -1:
            #             next_move = (x - self.Direction[0], z)
            #         elif x == 15 and self.ZigzagDir[0] == -1:
            #             if (z == 0 - self.Direction[2]):
            #                 return
            #             else:
            #                 next_move = (x, z +  self.Direction[2])
            #                 self.contadorSubida += 1
            #                 if self.contadorSubida == 1:
            #                     # self.angulo += 90
            #                     # for i in range(1):
            #                     #     self.angulo += 18
            #                     self.angulo += 18
            #                 if self.contadorSubida == 10:
            #                     self.ZigzagDir = [1, 1]
            #                     # self.angulo += 90
            #                     # for i in range(1):
            #                     #     self.angulo += 18
            #                     self.angulo += 18
            #                     self.contadorSubida = 0
                                
            #         self.Position[0] = next_move[0]
            #         self.Position[2] = next_move[1]

            # if self.id == 0:
            #     #Primeros movimientos
            #     if x < 200 and self.ZigzagDir[0] == 1:
            #         next_move = (x + self.Direction[0], z)
            #         self.Position[0] = next_move[0] 
            #         self.Position[2] = next_move[1] 
            #     elif x == 200 and self.ZigzagDir[0] == 1:
            #         if (z == 0 - self.Direction[2]):
            #             return
            #         else:
            #             next_move = (x, z + self.Direction[2])
            #             self.contadorSubida += 1
            #             if self.contadorSubida == 1:
            #                 # self.angulo += 90
            #                 for i in range(5):
            #                     self.angulo += 18
            #                     next_move = (x, z + self.Direction[2])
            #                     self.Position[0] = next_move[0] 
            #                     self.Position[2] = next_move[1]
                                
            #             if self.contadorSubida == 10:  
            #                 self.ZigzagDir = [-1, 1]
            #                 # self.angulo += 90
                           
            #                 for i in range(5):
            #                     self.angulo += 18
            #                     next_move = (x, z + self.Direction[2])
            #                     self.Position[0] = next_move[0] 
            #                     self.Position[2] = next_move[1] 
            #                 self.contadorSubida = 0
                            
            #     #Segundos movimientos
            #     elif x > 15 and self.ZigzagDir[0] == -1:
            #         next_move = (x - self.Direction[0], z)
            #         self.Position[0] = next_move[0] 
            #         self.Position[2] = next_move[1] 
            #     elif x == 15 and self.ZigzagDir[0] == -1:
            #         if (z == 0 - self.Direction[2]):
            #             return
            #         else:
            #             next_move = (x, z +  self.Direction[2])
            #             self.contadorSubida += 1
            #             if self.contadorSubida == 1:
            #                 # self.angulo += 90
            #                 for i in range(5):
            #                     self.angulo += 18
            #                     next_move = (x, z +  self.Direction[2])
            #                     self.Position[0] = next_move[0] 
            #                     self.Position[2] = next_move[1]
                                
            #             if self.contadorSubida == 10:
            #                 self.ZigzagDir = [1, 1]
                            
            #                 # self.angulo += 90
            #                 for i in range(5):
            #                     self.angulo += 18
            #                     next_move = (x, z +  self.Direction[2])
            #                     self.Position[0] = next_move[0] 
            #                     self.Position[2] = next_move[1] 
            #                 self.contadorSubida = 0

            #Primer carro
            if self.id == 0:
                #Primeros movimientos
                if x < 200 and self.ZigzagDir[0] == 1:
                    next_move = (x + self.Direction[0], z)
                elif x == 200 and self.ZigzagDir[0] == 1:
                    if (z == 0 - self.Direction[2]):
                        return
                    else:
                        next_move = (x, z + self.Direction[2])
                        self.contadorSubida += 1
                        if self.contadorSubida == 1:
                            # self.angulo += 90
                            for i in range(5):
                                self.angulo += 18
                        if self.contadorSubida == 10:  
                            self.ZigzagDir = [-1, 1]
                            # self.angulo += 90
                            for i in range(5):
                                self.angulo += 18
                            self.contadorSubida = 0
                #Segundos movimientos
                elif x > 15 and self.ZigzagDir[0] == -1:
                    next_move = (x - self.Direction[0], z)
                elif x == 15 and self.ZigzagDir[0] == -1:
                    if (z == 0 - self.Direction[2]):
                        return
                    else:
                        next_move = (x, z +  self.Direction[2])
                        self.contadorSubida += 1
                        if self.contadorSubida == 1:
                            # self.angulo += 90
                            for i in range(5):
                                self.angulo += 18
                        if self.contadorSubida == 10:
                            self.ZigzagDir = [1, 1]
                            # self.angulo += 90
                            for i in range(5):
                                self.angulo += 18
                            self.contadorSubida = 0
                self.Position[0] = next_move[0] 
                self.Position[2] = next_move[1] 

            #Segundo Carro
            elif self.id == 1:  
                #Primeros movimientos
                if x < -15 and self.ZigzagDir[0] == 1:
                    next_move = (x + self.Direction[0], z)
                elif x == -15 and self.ZigzagDir[0] == 1:
                    if (z == 0 - self.Direction[2]):
                        return
                    else:
                        next_move = (x, z + self.Direction[2])
                        self.contadorSubida += 1
                        if self.contadorSubida == 1:
                            # self.angulo += 90
                            for i in range(5):
                                self.angulo += 18
                        if self.contadorSubida == 10:  
                            self.ZigzagDir = [-1, 1]
                            # self.angulo += 90
                            for i in range(5):
                                self.angulo += 18
                            self.contadorSubida = 0
                #Segundos movimientos
                elif x > -200 and self.ZigzagDir[0] == -1:
                    next_move = (x - self.Direction[0], z)
                elif x == -200 and self.ZigzagDir[0] == -1:
                    if (z == 0 - self.Direction[2]):
                        return
                    else:
                        next_move = (x, z + self.Direction[2])
                        self.contadorSubida += 1
                        if self.contadorSubida == 1:
                            # self.angulo += 90
                            for i in range(5):
                                self.angulo += 18
                        if self.contadorSubida == 10:  
                            self.ZigzagDir = [1, 1]
                            # self.angulo += 90
                            for i in range(5):
                                self.angulo += 18
                            self.contadorSubida = 0
                self.Position[0] = next_move[0]
                self.Position[2] = next_move[1]
            
            #Tercer carro
            elif self.id == 2:
                #Primeros movimientos
                if x > 15 and self.ZigzagDir[0] == 1:
                    next_move = (x - self.Direction[0], z)
                elif x == 15 and self.ZigzagDir[0] == 1:
                    if (z == 0 - self.Direction[2]):
                        return
                    else:
                        next_move = (x, z - self.Direction[2])
                        self.contadorSubida += 1
                        if self.contadorSubida == 1:
                            # self.angulo += 90
                            for i in range(5):
                                self.angulo += 18
                        if self.contadorSubida == 10:  
                            self.ZigzagDir = [-1, 1]
                            # self.angulo += 90
                            for i in range(5):
                                self.angulo += 18
                            self.contadorSubida = 0
                #Segundos movimientos
                elif x < 200 and self.ZigzagDir[0] == -1:
                    next_move = (x + self.Direction[0], z)
                elif x == 200 and self.ZigzagDir[0] == -1:
                    if (z == 0 - self.Direction[2]):
                        return
                    else:
                        next_move = (x, z - self.Direction[2])
                        self.contadorSubida += 1
                        if self.contadorSubida == 1:
                            # self.angulo += 90
                            for i in range(5):
                                self.angulo += 18
                        if self.contadorSubida == 10:
                            self.ZigzagDir = [1, 1]
                            # self.angulo += 90
                            for i in range(5):
                                self.angulo += 18
                            self.contadorSubida = 0
                self.Position[0] = next_move[0] 
                self.Position[2] = next_move[1] 
            
            #Cuarto carro
            elif self.id == 3:
                #Primeros movimientos
                if x < -15 and self.ZigzagDir[0] == 1:
                    next_move = (x + self.Direction[0], z)
                elif x == -15 and self.ZigzagDir[0] == 1:
                    if (z == 0 - self.Direction[2]):
                        return
                    else:
                        next_move = (x, z - self.Direction[2])
                        self.contadorSubida += 1
                        if self.contadorSubida == 1:
                            # self.angulo += 90
                            for i in range(5):
                                self.angulo += 18
                        if self.contadorSubida == 10:  
                            self.ZigzagDir = [-1, 1]
                            # self.angulo += 90
                            for i in range(5):
                                self.angulo += 18
                            self.contadorSubida = 0
                #Segundos movimientos
                elif x > -200 and self.ZigzagDir[0] == -1:
                    next_move = (x - self.Direction[0], z)
                elif x == -200 and self.ZigzagDir[0] == -1:
                    if (z == 0 - self.Direction[2]):
                        return
                    else:
                        next_move = (x, z - self.Direction[2])
                        self.contadorSubida += 1
                        if self.contadorSubida == 1:
                            # self.angulo -= 90
                            for i in range(5):
                                self.angulo -= 18
                                # pygame.display.flip()
                                # pygame.time.wait(10)
                        if self.contadorSubida == 10:
                            self.ZigzagDir = [1, 1]
                            # self.angulo -= 90
                            for i in range(5):
                                self.angulo -= 18
                            self.contadorSubida = 0
                self.Position[0] = next_move[0] 
                self.Position[2] = next_move[1] 
            else:
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
        
        elif self.condition == self.CARGADO:            
            centro = (0,0)
            mejor_movimiento = None
            mejor_distancia = float('inf')  # Inicializar con un valor muy grande
            posiblemovs = [
                (x + self.Direction[0], z),
                (x + self.Direction[0], z + self.Direction[2]),
                (x, z + self.Direction[2]),
                (x - self.Direction[0], z + self.Direction[2]),
                (x - self.Direction[0], z),
                (x - self.Direction[0], z - self.Direction[2]),
                (x, z - self.Direction[2]),
                (x + self.Direction[0], z - self.Direction[2])
            ]
            for movim in posiblemovs:
                distancia = distancia_entre_puntos(movim, centro)
                if distancia < mejor_distancia:
                    mejor_distancia = distancia
                    mejor_movimiento = movim
                    
            next_move = mejor_movimiento
            self.Position[0] = next_move[0]
            self.Position[2] = next_move[1]
            #Sospecho que es aquí donde se eleva la basura a la plataforma (CONFIRMAR)
            self.basura.update((self.Position[0],self.AlturaPlataforma,self.Position[2] + 7.0))
            if next_move == centro:
                self.basura.centrar()
                self.condition = self.REGRESANDO
                self.AlturaPlataforma -= 1.0


        elif self.condition == self.REGRESANDO:
            mejor_movimiento = None
            mejor_distancia = float('inf')  # Inicializar con un valor muy grande
            posiblemovs = [
                (x + self.Direction[0], z),
                (x + self.Direction[0], z + self.Direction[2]),
                (x, z + self.Direction[2]),
                (x - self.Direction[0], z + self.Direction[2]),
                (x - self.Direction[0], z),
                (x - self.Direction[0], z - self.Direction[2]),
                (x, z - self.Direction[2]),
                (x + self.Direction[0], z - self.Direction[2])
            ]
            for movim in posiblemovs:
                distancia = distancia_entre_puntos(movim, self.basuraPos)
                if distancia < mejor_distancia:
                    mejor_distancia = distancia
                    mejor_movimiento = movim
            next_move = mejor_movimiento
            self.Position[0] = next_move[0]
            self.Position[2] = next_move[1]
            if next_move == self.basuraPos:
                self.condition = self.BUSCANDO
                
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

    def drawCar(self,textura,id, id2, id3, id4, id5):
        
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(5,5,5)
        glRotatef(self.angulo, 0, 1, 0)
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
        glDisable(GL_TEXTURE_2D)
        
        # Dibujar cilindro a la derecha
        glPushMatrix()
        glColor3f(0.0,0.0,0.0)
        glTranslatef(1.0, 0.0, 0.0)  
        glRotatef(90,0,1,0)
        self.cilindro.draw()
        glPopMatrix()
        
        # Dibujar cilindro a la izquierda
        glPushMatrix()
        glTranslatef(-1.5, 0.0, 0.0)  
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
        #plataforma
        glPushMatrix()
        glTranslatef(0.0, self.AlturaPlataforma, 2.0)
        glBindTexture(GL_TEXTURE_2D, textura[id])
        self.drawFace(-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, -1.0)
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
        glPopMatrix()
    
    def buscaColision(self,basuras):
        for basura in basuras:  
            dx = self.Position[0] - basura.Position[0]
            dz = self.Position[2] - basura.Position[2]
            distancia = math.sqrt(dx*dx + dz*dz)
            if distancia < self.radio + basura.radio and basura.condition == basura.TIRADA:
                self.condition = self.CARGADO
                self.basuraPos = (self.Position[0], self.Position[2])
                basura.condition = basura.RECOLECTADA
                self.basura = basura
                self.AlturaPlataforma += 1.0