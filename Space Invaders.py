import pygame
import random
import time
pygame.init()
pygame.display.set_caption("space invaders!")
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
gameover = False
xpos = 400
ypos = 750
moveLeft = False
moveRight = False
timer = 0;
shoot = False
collide = False
numHits = 0
lives = 3

class Alien:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = True
        self.direction = 1
    def draw(self):
        if self.isAlive == True:
            pygame.draw.rect(screen, (250, 250, 250), (self.xpos, self.ypos, 40, 40))
    def move(self, timer):
        if timer % 600 == 0:
            self.ypos += 100 #move down
            self.direction *=-1
            return 0
        if timer % 150 == 0:
            self.xpos+=20*self.direction #move right
        return timer
    
    
    def collide(self, BulletX, BulletY):
        if self.isAlive:
            if (BulletX > self.xpos and BulletX < self.xpos + 40
                and BulletY < self.ypos + 40 and BulletY > self.ypos):
                            print("hit!")
                            self.isAlive = False
                            return False
        return True
    
class Wall:
    def __init__(self, xpos, ypos, numHits):
        self.xpos = xpos
        self.ypos = ypos
        self.numHits = 0
    
    def draw(self):
        if self.numHits ==0:
            pygame.draw.rect(screen, (250, 250, 20), (self.xpos, self.ypos, 30, 30))
        if self.numHits ==1:
            pygame.draw.rect(screen, (150, 150, 10), (self.xpos, self.ypos, 30, 30))    
        if self.numHits ==2:
            pygame.draw.rect(screen, (50, 50, 0), (self.xpos, self.ypos, 30, 30))
            
    def collide(self, BulletX, BulletY):
        if self.numHits < 3:
            if (BulletX > self.xpos and BulletX < self.xpos + 40
                and BulletY < self.ypos + 40 and BulletY > self.ypos):
                            print("hit!")
                            self.numHits += 1
                            return numHits
        return True
#==============================================================================
class Missile:
    def __init__(self):
        self.xpos = -10
        self.ypos = -10
        self.isAlive = False
        
    def move(self):
        if self.isAlive == True:
            self.ypos+=5
        if self.ypos >800:
            self.isAlive = False
            self.xpos = -100
            self.ypos = -100
            
    def draw(self):
        if self.isAlive == True:
            pygame.draw.rect(screen, (250, 250, 250), (self.xpos, self.ypos, 3, 20))
            
missile = []
for i in range (10):
    missile.append(Missile())
#==============================================================================
class Bullet:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = False
        
    def move(self, xpos, ypos):
        if self.isAlive == True:
            self.ypos-=5
        if self.ypos < 0:
            self.isAlive = False
            self.xpos = xpos
            self.ypos = ypos
            
    def draw(self):
        if self.isAlive == True:
            pygame.draw.rect(screen, (250, 250, 250), (self.xpos, self.ypos, 3, 20))
        
    
            
        
bullet = Bullet(xpos+28, ypos)


armada = []
for i in range (4):
    for j in range (9):
        armada.append(Alien(j*80+50, i*80+50))

walls = []
for k in range (4):
    for i in range (2):
        for j in range (3):
            walls.append(Wall(j*30+200*k+50, i*30+600, 0))
        
while not gameover: #game loop----------------------------------------------------
    clock.tick(60)#FPS
    timer += 1       
    #Input Section----------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveLeft = True
            if event.key == pygame.K_RIGHT:
                moveRight = True
            if event.key == pygame.K_SPACE:
                shoot = True
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moveLeft = False
            if event.key == pygame.K_RIGHT:
                moveRight = False
            if event.key == pygame.K_SPACE:
                shoot = False
    #Physics section--------------------------------------------------------------
    
    if moveLeft == True:
        vx = -3
    elif moveRight == True:
        vx = 3
    else:
        vx = 0
        
    xpos += vx
    
    for i in range (len(armada)):
        timer = armada[i].move(timer)
        
    if shoot == True:
        bullet.isAlive = True
        
    for i in range (len(missile)):
        missile[i].move()
        
    chance = random.randrange(100)
    if chance < 2:
        print("Missle Drop!")
        pick = random.randrange(len(armada))
        if armada[pick].isAlive == True:
            for i in range(len(missile)):
                if missile[i].isAlive == False:
                    missile[i].isAlive = True
                    missile[i].xpos = armada[pick].xpos+5
                    missile[i].ypos = armada[pick].ypos
                    break
                
    for i in range(len(walls)):
        for j in range(len(missile)):
            if missile[j].isAlive == True:
                if walls[i].collide(missile[j].xpos, missile[j].ypos) == False:
                    missile[j].isAlive = False
                    break
        
    if bullet.isAlive == True:
        bullet.move(xpos+28, ypos)
        if bullet.isAlive == True:
            for i in range (len(armada)):
                bullet.isAlive = armada[i].collide(bullet.xpos, bullet.ypos)
                if bullet.isAlive == False:
                    print()
                    break
                
    else:
        bullet.xpos = xpos + 28
        bullet.ypos = ypos
    
    if bullet.isAlive == True:
        for i in range (len(walls)):
            bullet.isAlive = walls[i].collide(bullet.xpos, bullet.ypos)
            if bullet.isAlive == False:
                break
                
    for i in range (len(missile)):
        if missile[i].isAlive:
            if missile[i].xpos > xpos:
                if missile[i].xpos < xpos + 40:
                    if missile[i].ypos < ypos + 40:
                        if missile[i].ypos > ypos:
                            missile[i].ypos = 900
                            missile[i].xpos = 5
                            lives -= 1
                            time.sleep (1)
                            xpos = 400
                            print("Player Hit!")
                            break
    
    #Render section---------------------------------------------------------------
        
    screen.fill((0,0,0))
    
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = my_font.render('LIVES:', False, (255, 255, 0))
    text_surface2 = my_font.render(str(int(lives)), 1, (255, 0, 0))
    screen.blit(text_surface, (0,0))
    screen.blit(text_surface2, (120,0))
    
    
    pygame.draw.rect(screen, (0, 200, 50), (xpos, 750, 60, 20))
    pygame.draw.rect(screen, (0, 200, 50), (xpos+5, 745, 50, 20))
    pygame.draw.rect(screen, (0, 200, 50), (xpos+25, 736, 10, 20))
    pygame.draw.rect(screen, (0, 200, 50), (xpos+28, 732, 4, 20))
    
    for i in range (len(armada)):
        armada[i].draw()
        
    for i in range (len(walls)):
        walls[i].draw()
        
    for i in range (len(missile)):
        missile[i].draw()
        
    bullet.draw()
    pygame.display.flip()
    
    screen.blit(text_surface, (0,0))
    
    #End game loop----------------------------------------------------------------
    
    if lives < 0:
        gameover = True

pygame.quit() 
