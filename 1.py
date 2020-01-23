import sys, pygame, time
pygame.init()

size = width, height = 600, 600
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

class Ball(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.image = pygame.image.load("intro_ball_small.gif")
        #self.mask = pygame.mask.from_surface(pygame.image.load("intro_ball_mask.gif"))
        self.rect = self.image.get_rect()
        #self.rect.move(SPEED)
        #self.moving=False
        self.vectorx=speed[0]
        self.vectory=speed[1]
        self.rect.centerx=pos_x
        self.rect.bottom=pos_y

    def update(self):
        self.rect.y+=self.vectory
            
ball=Ball(300,300)
ball_image=ball.image
ballrect=ball.rect
all_sprites=pygame.sprite.Group(ball)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]
    
    screen.fill(black)
    
    #screen.blit(ball_image, ballrect)
    time.sleep(0.5)
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
