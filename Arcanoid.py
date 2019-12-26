import sys, pygame
from random import randrange

FPS = 30
SIZE = WIDTH, HEIGHT = 640, 480
Wall_width = 10
Field_w = WIDTH - Wall_width*2
Field_h = HEIGHT - Wall_width
speed = [1, 1]
BLACK = 0, 0, 0
WHITE = 255, 255, 255

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

class Wall(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

class Blocks(pygame.sprite.Sprite):
    def __init__(self, color, width, height, hardness=1):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.hardness = hardness

    def hit(self):
        hardness -= 1
        if hardness == 0:
            self.kill()
            

class App():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)

    def make_walls(self):
        self.walls_list = pygame.sprite.Group()
        l_wall = Wall(WHITE, Wall_width, HEIGHT)
        l_wall.rect.x = 0
        l_wall.rect.y = 0
        r_wall = Wall(WHITE, Wall_width, HEIGHT)
        r_wall.rect.x = WIDTH - Wall_width
        r_wall.rect.y = 0
        t_wall = Wall(WHITE, WIDTH, Wall_width)
        t_wall.rect.x = Wall_width
        t_wall.rect.y = 0

        self.walls_list.add(l_wall, r_wall, t_wall)

    def make_blocks(self):
        self.blocks_list = pygame.sprite.Group()
        with open ('INPUT') as inp:
            line = inp.readline()
            if 'level' in line:
                self.level = line
                line = inp.readline()
                field_size = line.split(' ')
                for i in range(int(field_size[0])):
                    line = inp.readline()
                    for k in range(int(field_size[1])):                   
                        if line[k].isdigit():
                            block_w = Field_w//(int(field_size[1])+1)
                            block_h = (Field_h//(int(field_size[1])+1))/2
                            block = Blocks(WHITE, block_w, block_h, line[k])
                            block.rect.x = k*(block_w+2) + Wall_width + 2
                            block.rect.y = i*(block_h+2) + Wall_width + 2
                            self.blocks_list.add(block)
                        
    
    def make_ball(self):
        self.main_ball = Ball()

    def terminate(self):
        pygame.display.quit()
        pygame.quit()
        sys.exit('See you next time!')


    def make_balls(self):
        self.balls_list = pygame.sprite.Group()
        for i in range(1, 17):
            ball = Ball()
            ball.change()
            ball.name += '_' + str(i)
            ball.rect.x = randrange(WIDTH - ball.rect.width)
            ball.rect.y = randrange(HEIGHT - ball.rect.height)
            self.balls_list.add(ball)
        self.all_sprites = pygame.sprite.Group(self.balls_list,
                                               self.main_ball,
                                               self.walls_list,
                                               self.blocks_list)

    def main_loop(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.main_ball.change()

                self.main_ball.rect.center = pygame.mouse.get_pos()
                if self.main_ball.rect.left < Wall_width:
                    self.main_ball.rect.left = Wall_width
                elif self.main_ball.rect.right > WIDTH - Wall_width:
                    self.main_ball.rect.right = WIDTH - Wall_width
                if self.main_ball.rect.top < Wall_width:
                    self.main_ball.rect.top = Wall_width
                elif self.main_ball.rect.bottom > HEIGHT:
                    self.main_ball.rect.bottom = HEIGHT
                
                for ball in self.balls_list:
                    if pygame.sprite.collide_mask(self.main_ball, ball):
                        print(ball.name)
                        ball.kill()
                #pygame.sprite.spritecollide(main_ball, balls_list, True)

            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)


if __name__ == '__main__':
    app = App()
    app.make_blocks()
    app.make_walls()
    app.make_ball()
    app.make_balls()
    app.main_loop()
    
