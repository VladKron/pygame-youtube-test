#https://www.youtube.com/playlist?list=PLzMcBGfZo4-lp3jAExUCewBfMx3UZFkh5

# Импортировать библиотеку под названием 'pygame'
import pygame

class Player():    # Player
    def __init__(self, x, y, w, h):
        #sprite
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vel = 5  # скорость
        self.jumpСount = 10
        self.walkCount = 0

        # флажки
        self.jump = False
        self.left = False
        self.right = False
        self.standing = True
    def draw(self, win):
        if self.walkCount + 1 >= FPS:  #обнуление шагомера
            self.walkCount = 0
        if not(self.standing): # если человечек не стоит
            if self.left:  
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y)) # делим на 3, т.к. у нас 9 картинок при 27 FPS
                self.walkCount += 1                          
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        else:                  # если человечек стоит
            if self.left and self.right:
                win.blit(char, (self.x, self.y))
                self.walkCount = 0
            elif self.left:
                win.blit(walkLeft[0], (self.x, self.y))     
            else:
                win.blit(walkRight[0], (self.x, self.y))

            #self.walkCount = 0


class Bullet():
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing       
        self.vel = 8 * facing
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
    
        

pygame.init()  # запуск время игры
# pygame.time.get_ticks()  # время с начала игры

win_x = 500
win_y = 500
walkRight = [pygame.image.load('data\R1.png'), pygame.image.load('data\R2.png'), pygame.image.load('data\R3.png'), pygame.image.load('data\R4.png'), pygame.image.load('data\R5.png'), pygame.image.load('data\R6.png'), pygame.image.load('data\R7.png'), pygame.image.load('data\R8.png'), pygame.image.load('data\R9.png')]
walkLeft = [pygame.image.load('data\L1.png'), pygame.image.load('data\L2.png'), pygame.image.load('data\L3.png'), pygame.image.load('data\L4.png'), pygame.image.load('data\L5.png'), pygame.image.load('data\L6.png'), pygame.image.load('data\L7.png'), pygame.image.load('data\L8.png'), pygame.image.load('data\L9.png')]
char = pygame.image.load('data\standing.png')
bg = pygame.image.load('data\\bg.jpg')
FPS = 27
bulletNum = 10   # максимальное кол. пуль на экране
run = True

win = pygame.display.set_mode((win_x, win_y))
pygame.display.set_caption('AYE 777')
clock = pygame.time.Clock()  # создавать часы 

p = Player(300, 410, 64, 64)
bullets =[]

def redrawWin():
    win.blit(bg, (0, 0))
    p.draw(win)
    for b in bullets:
        b.draw(win)
    
    pygame.display.update()

while run:
    clock.tick(FPS) # Игра будет работать со скоростью не более FPS кадров в секунду
    #pygame.time.delay(100)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # проверяем вылетела ли пуля за границу окна
    for b in bullets:
        if b.x < win_x and b.x > 0:
            b.x += b.vel
        else:
            bullets.pop(bullets.index(b)) # удаляем из списка пулю с индексом текущей пули

    # проверяем клавиши ЛЕВО, ПРАВО и выставляем флажки    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if p.left:
            facing = -1
        else:
            facing = 1    
        if len(bullets) < bulletNum: # сколько пуль можно выпустить
            bullets.append(Bullet(p.x + p.w//2,p.y + p.h//2,6,(23,54,245),facing))
    if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
        p.standing = True
        p.left = True
        p.right = True
        #p.left = False
        #p.right = False
    elif keys[pygame.K_LEFT] and p.x > 0:
        p.x -= p.vel
        p.left = True
        p.standing = False
        p.right = False
    elif keys[pygame.K_RIGHT] and p.x + p.w < win_x:
        p.x += p.vel
        p.left = False
        p.right = True
        p.standing = False
    else:
        #p.left = False
        #p.right = False
        #p.walkCount = 0
        p.standing = True
        
    # проверяем клавиши ПРОБЕЛ и выставляем флажки    
    if not(p.jump):
        if keys[pygame.K_UP]:
            p.jump = True
            #p.left = False
            #p.right = False
            p.walkCount = 0
    else:
        if p.jumpСount >= -10:
            neg = 1
            if p.jumpСount < 0: # чтобы лететь в обратную сторону
                neg = -1
            p.y -= int((p.jumpСount ** 2) * 0.5 * neg) # ускорение
            p.jumpСount -= 1
        else:
            p.jump = False
            p.jumpСount = 10
    redrawWin()
pygame.quit()
