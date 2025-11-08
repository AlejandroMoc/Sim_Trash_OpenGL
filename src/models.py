import math
import random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def dist_between_points(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

class Wheel:
    def __init__(self, radio, altura, slices=30, stacks=30):
        self.radio = radio
        self.altura = altura
        self.slices = slices
        self.stacks = stacks

    def draw(self):
        glPushMatrix()
        glColor3f(0.0, 0.0, 0.0)

        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluQuadricTexture(quadric, GL_TRUE)

        # Lateral side
        gluCylinder(quadric, self.radio, self.radio, self.altura, self.slices, self.stacks)

        # Covers of the wheel
        glPushMatrix()
        glTranslatef(0.0, 0.0, self.altura)
        gluDisk(quadric, 0.0, self.radio, self.slices, 1)
        glPopMatrix()

        glPushMatrix()
        glRotatef(180, 1.0, 0.0, 0.0)
        gluDisk(quadric, 0.0, self.radio, self.slices, 1)
        glPopMatrix()

        gluDeleteQuadric(quadric)
        glPopMatrix()

class TrashBlock:
    STATE_COLLECTED = 0
    STATE_ON_GROUND = 1

    def __init__(self, dim):
        self.angulo = 0
        self.radio = 7.0
        self.Position = [0.0, 5.0, 0.0]
        # The coordinates of the cube's vertices are initialized
        self.vertexCoords = [
                   1,1,1,   1,1,-1,   1,-1,-1,   1,-1,1,
                  -1,1,1,  -1,1,-1,  -1,-1,-1,  -1,-1,1 ]

        # Vertex colors
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
        # Random position
        self.Position[0] = random.randint(-self.DimBoard, self.DimBoard)
        self.Position[2] = random.randint(-self.DimBoard, self.DimBoard)
        self.condition = self.STATE_ON_GROUND

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

    # Here change this
    def draw(self, textura, id):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(5,5,5)
        glColor3f(1.0, 1.0, 1.0)
        # Enable textures
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

    # To use textures like in this
    def drawTrash(self,textura,id):

        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(4,4,4)
        glRotatef(self.angulo, 0, 1, 0)
        glColor3f(1.0, 1.0, 1.0)

        # Enable textures
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
        self.Position[1] = pos[1] + 12.0
        self.Position[2] = pos[2]

    def centrar(self):
        self.Position[0] = 0.0
        self.Position[1] = 5.0
        self.Position[2] = 0.0

class TrashCar:
    STATE_SEARCHING = 0
    STATE_CARRYING = 1
    STATE_RETURNING = 2
    STATE_RAISING = 3
    STATE_LOWERING = 4

    def __init__(self, dim, vel, pos, id):
        self.id = id
        self.condition = self.STATE_SEARCHING
        self.radio = 7.0
        self.Position = [0.0, 7.0, 0.0]
        self.Direction = [0.0, 7.0, 0.0]
        self.cilindro = Wheel(radio=0.5, altura=0.5)

        self.DimBoard = dim

        # Last trash found
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

        self.contadorPlataforma = 0

        self.angulo = 0
        self.ultimoAngulo = self.angulo

        if self.id == 0:
            self.angulo = 90

        elif self.id == 1:
            self.angulo = 90

        elif self.id == 2:
            self.angulo = -90

        elif self.id == 3:
            self.angulo = 90

        else:
            self.angulo = 0

        self.AlturaPlataforma = -1.9

    def update(self):
        x,z = self.Position[0],self.Position[2]
        if self.condition == self.STATE_SEARCHING:

            # First TrashCar (+x,-z)
            if self.id == 0:
                # First movements
                if x < 200 and self.ZigzagDir[0] == 1:
                    next_move = (x + self.Direction[0], z)
                elif x <= 200 and self.ZigzagDir[0] == 1:
                    if (z == 0 - self.Direction[2]):
                        return
                    else:
                        next_move = (x, z + self.Direction[2])
                        self.contadorSubida += 1
                        if self.contadorSubida == 1:
                            self.angulo -= 90
                        if self.contadorSubida == 10:
                            self.ZigzagDir = [-1, 1]
                            self.angulo -= 90
                            self.contadorSubida = 0
                # Second movements
                elif x > 10 and self.ZigzagDir[0] == -1:
                    next_move = (x - self.Direction[0], z)
                elif x <= 10 and self.ZigzagDir[0] == -1:
                    if (z == 0 - self.Direction[2]):
                        return
                    else:
                        next_move = (x, z +  self.Direction[2])
                        self.contadorSubida += 1
                        if self.contadorSubida == 1:
                            self.angulo += 90
                        if self.contadorSubida == 10:
                            self.ZigzagDir = [1, 1]
                            self.angulo += 90
                            self.contadorSubida = 0
                self.Position[0] = next_move[0]
                self.Position[2] = next_move[1]

            # Second TrashCar (-x, -z)
            elif self.id == 1:
                # First movements
                if x < -10 and self.ZigzagDir[0] == 1:
                    next_move = (x + self.Direction[0], z)
                elif x == -10 and self.ZigzagDir[0] == 1:
                    if (z == 0 - self.Direction[2]):
                        return
                    else:
                        next_move = (x, z + self.Direction[2])
                        self.contadorSubida += 1
                        if self.contadorSubida == 1:
                            self.angulo -= 90
                        if self.contadorSubida == 10:
                            self.ZigzagDir = [-1, 1]
                            self.angulo -= 90
                            self.contadorSubida = 0
                # Second movements
                elif x > -200 and self.ZigzagDir[0] == -1:
                    next_move = (x - self.Direction[0], z)
                elif x == -200 and self.ZigzagDir[0] == -1:
                    if (z == 0 - self.Direction[2]):
                        return
                    else:
                        next_move = (x, z + self.Direction[2])
                        self.contadorSubida += 1
                        if self.contadorSubida == 1:
                            self.angulo += 90
                        if self.contadorSubida == 10:
                            self.ZigzagDir = [1, 1]
                            self.angulo += 90
                            self.contadorSubida = 0
                self.Position[0] = next_move[0]
                self.Position[2] = next_move[1]

            # Third TrashCar (+x, +z)
            elif self.id == 2:
                # First movements
                if x > 10 and self.ZigzagDir[0] == 1:
                    next_move = (x - self.Direction[0], z)
                elif x == 10 and self.ZigzagDir[0] == 1:
                    if (z == 0 - self.Direction[2]):
                        return
                    else:
                        next_move = (x, z - self.Direction[2])
                        self.contadorSubida += 1
                        if self.contadorSubida == 1:
                            self.angulo -= 90
                        if self.contadorSubida == 10:
                            self.ZigzagDir = [-1, 1]
                            self.angulo -= 90
                            self.contadorSubida = 0
                # Second movements
                elif x < 200 and self.ZigzagDir[0] == -1:
                    next_move = (x + self.Direction[0], z)
                elif x == 200 and self.ZigzagDir[0] == -1:
                    if (z == 0 - self.Direction[2]):
                        return
                    else:
                        next_move = (x, z - self.Direction[2])
                        self.contadorSubida += 1
                        if self.contadorSubida == 1:
                            self.angulo += 90
                        if self.contadorSubida == 10:
                            self.ZigzagDir = [1, 1]
                            self.angulo += 90
                            self.contadorSubida = 0
                self.Position[0] = next_move[0]
                self.Position[2] = next_move[1]

            # Fourth TrashCar (-x, +z)
            elif self.id == 3:
                # First movements
                if x < -10 and self.ZigzagDir[0] == 1:
                    next_move = (x + self.Direction[0], z)
                elif x == -10 and self.ZigzagDir[0] == 1:
                    if (z == 0 - self.Direction[2]):
                        return
                    else:
                        next_move = (x, z - self.Direction[2])
                        self.contadorSubida += 1
                        if self.contadorSubida == 1:
                            self.angulo += 90
                        if self.contadorSubida == 10:
                            self.ZigzagDir = [-1, 1]
                            self.angulo += 90
                            self.contadorSubida = 0
                # Second movements
                elif x > -200 and self.ZigzagDir[0] == -1:
                    next_move = (x - self.Direction[0], z)
                elif x == -200 and self.ZigzagDir[0] == -1:
                    if (z == 0 - self.Direction[2]):
                        return
                    else:
                        next_move = (x, z - self.Direction[2])
                        self.contadorSubida += 1
                        if self.contadorSubida == 1:
                            self.angulo -= 90
                        if self.contadorSubida == 10:
                            self.ZigzagDir = [1, 1]
                            self.angulo -= 90
                            self.contadorSubida = 0
                self.Position[0] = next_move[0]
                self.Position[2] = next_move[1]

            else:
                new_x = self.Position[0] + self.Direction[0]
                new_z = self.Position[2] + self.Direction[2]

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
            self.ultimoAngulo = self.angulo

        elif self.condition == self.STATE_RAISING:
            if self.contadorPlataforma < 40:
                self.contadorPlataforma += 1
                self.AlturaPlataforma += 0.025
                self.basura.update((self.basura.Position[0],self.AlturaPlataforma - 1.0,self.basura.Position[2]))
            else:
                self.condition = self.STATE_CARRYING

        elif self.condition == self.STATE_LOWERING:
            if self.contadorPlataforma > 0:
                self.contadorPlataforma -= 1
                self.AlturaPlataforma -= 0.025
                self.basura.update((self.Position[0],self.AlturaPlataforma,self.Position[2]))
            else:
                self.condition = self.STATE_RETURNING
                self.contadorPlataforma = 0
                self.basura.centrar()

        elif self.condition == self.STATE_CARRYING:
            # Determine the direction to move towards to achieve (0, 0)
            if self.Position[2] > 0:
                next_move = (self.Position[0], self.Position[2] - self.Direction[2])
                self.angulo = 180
            elif self.Position[2] < 0:
                self.angulo = 0
                next_move = (self.Position[0], self.Position[2] + self.Direction[2])
            elif self.Position[0] > 0:
                next_move = (self.Position[0] - self.Direction[0], self.Position[2])
                self.angulo = -90
            elif self.Position[0] < 0:
                next_move = (self.Position[0] + self.Direction[0], self.Position[2])
                self.angulo = 90

            dx = next_move[0] - self.Position[0]
            dz = next_move[1] - self.Position[2]

            if dx != 0:
                dx /= abs(dx)
                dx *= 5
            if dz != 0:
                dz /= abs(dz)
                dz *= 5

            # Update self.Position
            self.Position[0] = next_move[0]
            self.Position[2] = next_move[1]
            # Change agent state to raise the trash
            self.basura.update((self.Position[0] + dx,self.AlturaPlataforma,self.Position[2] + dz))
            if next_move == (0,0):
                self.condition = self.STATE_LOWERING

        # elif self.condition == self.STATE_CARRYING:
        #     center = (0,0)
        #     best_move = None
        #     best_distance = float('inf')  # Initialize with a very large value
        #     possible_moves = [
        #         (x + self.Direction[0], z),
        #         (x + self.Direction[0], z + self.Direction[2]),
        #         (x, z + self.Direction[2]),
        #         (x - self.Direction[0], z + self.Direction[2]),
        #         (x - self.Direction[0], z),
        #         (x - self.Direction[0], z - self.Direction[2]),
        #         (x, z - self.Direction[2]),
        #         (x + self.Direction[0], z - self.Direction[2])
        #     ]
        #     for move in possible_moves:
        #         distance = dist_between_points(move, center)
        #         if distance < best_distance:
        #             best_distance = distance
        #             best_move = move

        #     next_move = best_move
        #     # Determine the movement direction based on next_move and self.Position
        #     dx = next_move[0] - self.Position[0]
        #     dz = next_move[1] - self.Position[2]

        #     if dx != 0:
        #         dx /= abs(dx)
        #         dx *= 5
        #     if dz != 0:
        #         dz /= abs(dz)
        #         dz *= 5

        #     # Update self.Position
        #     self.Position[0] = next_move[0]
        #     self.Position[2] = next_move[1]
        #     # Change the agent's state to raise the trash
        #     self.basura.update((self.Position[0] + dx,self.AlturaPlataforma,self.Position[2] + dz))
        #     if next_move == center:
        #         self.condition = self.STATE_LOWERING


        # elif self.condition == self.STATE_RETURNING:
        #     best_move = None
        #     best_distance = float('inf')  # Initialize with a very large value
        #     possible_moves = [
        #         (x + self.Direction[0], z),
        #         (x + self.Direction[0], z + self.Direction[2]),
        #         (x, z + self.Direction[2]),
        #         (x - self.Direction[0], z + self.Direction[2]),
        #         (x - self.Direction[0], z),
        #         (x - self.Direction[0], z - self.Direction[2]),
        #         (x, z - self.Direction[2]),
        #         (x + self.Direction[0], z - self.Direction[2])
        #     ]
        #     for move in possible_moves:
        #         distance = dist_between_points(move, self.basuraPos)
        #         if distance < best_distance:
        #             best_distance = distance
        #             best_move = move
        #     next_move = best_move
        #     self.Position[0] = next_move[0]
        #     self.Position[2] = next_move[1]
        #     if next_move == self.basuraPos:
        #         self.condition = self.STATE_SEARCHING
        #         self.angulo = self.ultimoAngulo

        elif self.condition == self.STATE_RETURNING:
            # Determine the direction to move towards to achieve (0, 0)
            if self.Position[2] > self.basuraPos[1]:
                next_move = (self.Position[0], self.Position[2] - self.Direction[2])
                self.angulo = 180
            elif self.Position[2] < self.basuraPos[1]:
                self.angulo = 0
                next_move = (self.Position[0], self.Position[2] + self.Direction[2])
            elif self.Position[0] > self.basuraPos[0]:
                next_move = (self.Position[0] - self.Direction[0], self.Position[2])
                self.angulo = -90
            elif self.Position[0] < self.basuraPos[0]:
                next_move = (self.Position[0] + self.Direction[0], self.Position[2])
                self.angulo = 90
            self.Position[0] = next_move[0]
            self.Position[2] = next_move[1]
            if next_move == self.basuraPos:
                self.condition = self.STATE_SEARCHING
                self.angulo = self.ultimoAngulo


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

        # If the state is STATE_CARRYING:
        # Calculate the angle to point towards the origin (0,0,0)
        # angleToOrigin = math.atan2(-self.Position[2], -self.Position[0]) * 180 / math.pi

        # Apply a rotation so that the front points towards the origin
        # glRotatef(angleToOrigin, 0, 1, 0)

        glRotatef(self.angulo, 0, 1, 0)
        glColor3f(1.0, 1.0, 1.0)
        # Enable textures
        glEnable(GL_TEXTURE_2D)
        # Front
        glBindTexture(GL_TEXTURE_2D, textura[id2])
        self.drawFace(-1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0)
        # Right
        glBindTexture(GL_TEXTURE_2D, textura[id5])
        self.drawFace(1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0)
        # Back
        glBindTexture(GL_TEXTURE_2D, textura[id3])
        self.drawFace(1.0, 1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0)
        # Left
        glBindTexture(GL_TEXTURE_2D, textura[id5])
        self.drawFace(-1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0)
        # Up
        glBindTexture(GL_TEXTURE_2D, textura[id4])
        self.drawFace(-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, -1.0)
        glDisable(GL_TEXTURE_2D)

        # Draw cylinder to the right
        glPushMatrix()
        glColor3f(0.0,0.0,0.0)
        glTranslatef(1.0, -0.85, 0.0)
        glRotatef(90,0,1,0)
        self.cilindro.draw()
        glPopMatrix()

        # Draw cylinder to the left
        glPushMatrix()
        glTranslatef(-1.5, -0.85, 0.0)
        glRotatef(90,0,1,0)
        self.cilindro.draw()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.0, 1.5, -0.5)
        glScaled(0.5,0.5,0.5)
        glColor3f(1.0, 1.0, 1.0)


        glEnable(GL_TEXTURE_2D)
        # Front
        glBindTexture(GL_TEXTURE_2D, textura[id4])
        self.drawFace(-1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0)
        # Right
        glBindTexture(GL_TEXTURE_2D, textura[id4])
        self.drawFace(1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0)
        # Back
        glBindTexture(GL_TEXTURE_2D, textura[id4])
        self.drawFace(1.0, 1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0)
        # Left
        glBindTexture(GL_TEXTURE_2D, textura[id4])
        self.drawFace(-1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0)
        # Up
        glBindTexture(GL_TEXTURE_2D, textura[id4])
        self.drawFace(-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, -1.0)
        glPopMatrix()
        # Platform
        glPushMatrix()
        glTranslatef(0.0, self.AlturaPlataforma, 2.0)
        glBindTexture(GL_TEXTURE_2D, textura[id])
        self.drawFace(-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, -1.0)
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
        glPopMatrix()

    def search_collision(self,basuras):
        for basura in basuras:
            dx = self.Position[0] - basura.Position[0]
            dz = self.Position[2] - basura.Position[2]
            distancia = math.sqrt(dx*dx + dz*dz)
            if distancia < self.radio + basura.radio and basura.condition == basura.STATE_ON_GROUND:
                self.condition = self.STATE_RAISING
                self.basuraPos = (self.Position[0], self.Position[2])
                basura.condition = basura.STATE_COLLECTED
                self.basura = basura
