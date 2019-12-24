import sys, pygame
from random import randrange

FPS = 30
SIZE = WIDTH, HEIGHT = 640, 480
speed = [1, 1]
BLACK = 0, 0, 0

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("intro_ball.gif")
        self.mask = pygame.mask.from_surface(
            pygame.image.load("intro_ball_mask.gif"))
        self.rect = self.image.get_rect()
        self.name = 'Ball'
        self.n = 0

    def change(self):
        self.n += 1
        xy = self.rect.center
        if self.n == 3:
            self.image = pygame.image.load("intro_ball.gif")
            self.mask = pygame.mask.from_surface(
                pygame.image.load("intro_ball_mask.gif"))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.center = xy
            self.n = 0
        if self.n == 1:
            self.image = pygame.image.load("intro_ball_middle.gif")
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.center = xy
        if self.n == 2:
            self.image = pygame.image.load("intro_ball_small.gif")
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.center = xy


class App():

    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SIZE)

    def make_ball(self):
        main_ball = Ball()

    def terminate(self):
        pygame.display.quit()
        pygame.quit()
        sys.exit('See you next time!')

    def main_loop(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        main_ball.change()

                main_ball.rect.center = pygame.mouse.get_pos()
                if main_ball.rect.left < 0:
                    main_ball.rect.left = 0
                elif main_ball.rect.right > WIDTH:
                    main_ball.rect.right = WIDTH
                if main_ball.rect.top < 0:
                    main_ball.rect.top = 0
                elif main_ball.rect.bottom > HEIGHT:
                    main_ball.rect.bottom = HEIGHT
                
                for ball in balls_list:
                    if pygame.sprite.collide_mask(main_ball, ball):
                        print(ball.name)
                        ball.kill()
                #pygame.sprite.spritecollide(main_ball, balls_list, True)

            screen.fill(BLACK)
            all_sprites.draw(screen)
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)

balls_list = pygame.sprite.Group()

for i in range(1, 17):
    ball = Ball()
    ball.change()
    ball.change()
    ball.name += '_' + str(i)
    ball.rect.x = randrange(WIDTH - ball.rect.width)
    ball.rect.y = randrange(HEIGHT - ball.rect.height)
    
    balls_list.add(ball)

all_sprites = pygame.sprite.Group(balls_list, main_ball)


if __name__ == '__main__':
    app = App()
    app.main_loop()
    
