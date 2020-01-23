import sys, pygame
from random import randrange

FPS = 30
SIZE = WIDTH, HEIGHT = 720, 480
Wall_width = 10
Field_w = WIDTH - Wall_width*2
Field_h = HEIGHT - Wall_width
speed = [1, 1]
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
BRIKS_PERCENTAGE=0.5
SPEED = [2,2]

class Ball():
    def __init__(self,pos_x,pos_y):
        #super().__init__()
        self.image = pygame.image.load("intro_ball_small.gif")
        #self.mask = pygame.mask.from_surface(pygame.image.load("intro_ball_mask.gif"))
        self.rect = self.image.get_rect()
        #self.rect.move(SPEED)
        #self.moving=False
        self.rect.centerx=pos_x
        self.rect.bottom=pos_y

pygame.init()
screen = pygame.display.set_mode(SIZE)
ball=Ball(200,200)
ball.rect.move([10,10])
#all_sprites=pygame.sprite.Group(ball)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ballrect = ball.rect.move(SPEED)
    screen.fill(BLACK)
    #all_sprites.draw(screen)
    screen.blit(ball.image, ballrect)
    pygame.display.flip()
    #pygame.time.Clock().tick(FPS)
