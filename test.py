#  Pygame template - skeleton for a new pygame project
import pygame
import random


WIDTH = 800 # width of our game window
HEIGHT = 600 # height of our game window
FPS = 30 # 30 frames per second


# Colors(R,G,B),define color
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)


class Player(pygame.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        # this line is required to properly create the sprite
        pygame.sprite.Sprite.__init__(self)
        # create a plain rectangle for the sprite image
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        # find the rectangle that encloses the image
        self.rect = self.image.get_rect()
        # center the sprite on the screen
        self.rect.center = (WIDTH/2, HEIGHT/2)

    def update(self, *args):
        # any code here will happen every time the game loop updates
        self.rect.x += 5
        if self.rect.left > WIDTH:
            self.rect.right = 0



# initialize pygame and create windw
pygame.init()  # 启动pygame并初始化
pygame.mixer.init()  # 声音初始化
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 游戏屏幕，按照在配置常量中设置的大小创建
pygame.display.set_caption("Sprite Example")
clock = pygame.time.Clock()  # 创建一个时钟以便于确保游戏能以指定的FPS运行


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

player2 = Player()

pygame.sprite.spritecollide()
# Game Loop
running = True


while running:
    # keep loop running at the right speed
    clock.tick(FPS)

    # Process input(events)    # 这是游戏主循环，通过变量running控制，如果需要
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False


    # Update                   # 游戏结束的话直接将running设为False即可
    all_sprites.update()


    # Render(draw)             # 现在还没有确定具体的代码，先用一些基本代码填充，后续再补充
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # *after* drawing everything,flip the display
    pygame.display.flip()



pygame.quit()