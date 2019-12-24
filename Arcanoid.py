import sys, pygame, time
pygame.init()

FPS = 30
SIZE = WIDTH, HEIGHT = 640, 480
speed = [1, 1]
BLACK = 0, 0, 0

screen = pygame.display.set_mode(SIZE)

class Ball:
    def __init__(self):
        self.img = pygame.image.load("intro_ball.gif")
        self.rect = self.img.get_rect()
        self.n = 0

    def change(self):
        self.n += 1
        xy = self.rect.center
        if self.n == 3:
            self.img = pygame.image.load("intro_ball.gif")
            self.rect = self.img.get_rect()
            self.rect.center = xy
            self.n = 0
        if self.n == 1:
            self.img = pygame.image.load("intro_ball_middle.gif")
            self.rect = self.img.get_rect()
            self.rect.center = xy
        if self.n == 2:
            self.img = pygame.image.load("intro_ball_small.gif")
            self.rect = self.img.get_rect()
            self.rect.center = xy

ball = Ball()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit('See you next time!')

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                speed[0] += 1
            if event.key == pygame.K_LEFT:
                speed[0] -= 1
            if event.key == pygame.K_UP:
                speed[1] -= 1
            if event.key == pygame.K_DOWN:
                speed[1] += 1
            if event.key == pygame.K_SPACE:
                ball.change()

    ball.rect = ball.rect.move(speed)
    if ball.rect.left < 0 or ball.rect.right > WIDTH:
        speed[0] = -speed[0]
    if ball.rect.top < 0 or ball.rect.bottom > HEIGHT:
        speed[1] = -speed[1]

    screen.fill(BLACK)
    screen.blit(ball.img, ball.rect)
    pygame.display.flip()
    pygame.time.Clock().tick(FPS)
