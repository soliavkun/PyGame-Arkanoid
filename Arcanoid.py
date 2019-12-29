import sys, pygame
from random import randrange

FPS = 30
SIZE = WIDTH, HEIGHT = 720, 480
Wall_width = 10
Field_w = WIDTH - Wall_width*2
Field_h = HEIGHT - Wall_width
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
BRIKS_PERCENTAGE=0.5
SPEED = -8,-6

class Ball(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.image = pygame.image.load("intro_ball_small.gif")
        self.mask = pygame.mask.from_surface(
            pygame.image.load("intro_ball_mask.gif"))
        self.rect = self.image.get_rect()
        self.rect.move(SPEED)
        self.moving=False
        self.name = 'MAIN_BALL'
        self.n = 0
        self.rect.centerx=pos_x
        self.rect.bottom=pos_y
        self.vectorx=SPEED[0]
        self.vectory=SPEED[1]

    def update(self,objects):
        self.rect.x+=self.vectorx
        self.rect.y+=self.vectory
        '''
        walls=pygame.sprite.spritecollide(self, walls, False)
        paddles=pygame.sprite.spritecollide(self, paddle, False)
        if walls:
            if walls[0].name=='RIGHT_WALL' or walls[0].name=='LEFT_WALL':
                self.vectorx*=-1
            if walls[0].name=='TOP_WALL':
                self.vectory*=-1
        '''
        result=pygame.sprite.spritecollide(self, objects, False)
        if result:
            if result[0].name=='RIGHT_WALL' or result[0].name=='LEFT_WALL':
                self.vectorx*=-1
            if result[0].name=='TOP_WALL' or result[0].name=='PADDLE':
                self.vectory*=-1
            #print(walls[0].name)
        #for wall in walls:
        #    print(dir(wall))
        
        

    def set_position(self,pos_x):
        if self.moving==False:
            self.rect.centerx=pos_x
   
                

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
    
    def __init__(self, color, width, height,name):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.name=name

class Blocks(pygame.sprite.Sprite):
    count=0
    base_name='Block'
    def __init__(self, color, width, height, hardness=1):
        super().__init__()
        self.count=count+1
        self.name=base_name+str(self.count)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.hardness = hardness

    def hit(self):
        hardness -= 1
        if hardness == 0:
            self.kill()
            
class Paddle(pygame.sprite.Sprite):
    def __init__(self,width,height,color=RED,name='PADDLE'):
        super().__init__()
        self.name=name
        self.width=width
        self.height=height
        self.image=pygame.Surface([self.width,self.height])
        self.image.fill(color)
        self.moving=False
        self.rect=self.image.get_rect()
        self.rect.left=WIDTH/2-self.width
        self.rect.bottom=HEIGHT-30
    
    def size(self,size=[]):
        self.width=size[0]
        self.height=size[1]
        self.rect.size=size
        
    def get_size(self):
        print(self.rect.size)
        
    def set_position(self,x):

        left_border=0+Wall_width+self.width/2
        right_border=WIDTH-Wall_width-self.width/2
        if x<left_border:
            x=self.width/2
        if x>right_border:
            x=WIDTH-self.width/2
        self.rect.centerx=x
        
class App():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)


    def make_walls(self):
        self.walls_list = pygame.sprite.Group()
        l_wall = Wall(WHITE, Wall_width, HEIGHT,'LEFT_WALL')
        l_wall.rect.x = 0
        l_wall.rect.y = 0
        r_wall = Wall(WHITE, Wall_width, HEIGHT,'RIGHT_WALL')
        r_wall.rect.x = WIDTH - Wall_width
        r_wall.rect.y = 0
        t_wall = Wall(WHITE, WIDTH, Wall_width,'TOP_WALL')
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
                            print(field_size[0],'-->',field_size[1])
                            block_w = int(((WIDTH-Wall_width*2))//int(field_size[0]))-2
                            #block_w = Field_w//(int(field_size[1])+1)
                            block_h = int((HEIGHT*BRIKS_PERCENTAGE)//int(field_size[1]))-2
                            #block_h = (Field_h//(int(field_size[1])+1))/2
                            block = Blocks(WHITE, block_w, block_h, line[k])
                            block.rect.x = k*(block_w+2) + Wall_width + 1
                            block.rect.y = i*(block_h+2) + Wall_width + 2
                            print(block.name)
                            self.blocks_list.add(block)
                        
    
    def make_ball(self,pos_x,pos_y):
        self.main_ball = Ball(pos_x,pos_y)
        
    def make_paddle(self,width=80,height=25):
        self.paddle=Paddle(width,height)

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
        

    def main_loop(self):
        self.make_blocks()
        self.make_walls()
        self.make_paddle(100,30)
        pos_x=self.paddle.rect.centerx
        pos_y=self.paddle.rect.top
        self.make_ball(pos_x,pos_y)
        self.all_sprites = pygame.sprite.Group(self.paddle,
                                               self.walls_list,
                                               self.blocks_list,
                                               self.main_ball,
                                               )
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.main_ball.moving=True
                       
                        
                '''
                if self.main_ball.rect.left < Wall_width:
                    self.main_ball.rect.left = Wall_width
                elif self.main_ball.rect.right > WIDTH - Wall_width:
                    self.main_ball.rect.right = WIDTH - Wall_width
                if self.main_ball.rect.top < Wall_width:
                    self.main_ball.rect.top = Wall_width
                elif self.main_ball.rect.bottom > HEIGHT:
                    self.main_ball.rect.bottom = HEIGHT
                '''


            self.paddle.set_position(pygame.mouse.get_pos()[0])
            collide_group=pygame.sprite.Group(self.walls_list,self.paddle)
            if self.main_ball.moving:
                self.main_ball.update(collide_group)
            else:
                self.main_ball.set_position(self.paddle.rect.centerx)  
                    
            for block in self.blocks_list:
                if pygame.sprite.collide_mask(self.paddle, block):
                    block.kill()
                #pygame.sprite.spritecollide(main_ball, balls_list, True)

            
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)


if __name__ == '__main__':
    app = App()
    app.main_loop()
    
