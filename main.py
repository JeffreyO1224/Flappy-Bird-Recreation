import pygame
import random
import os
from os import path
#Colors:
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#Settings
pygame.init()
pygame.mixer.init() #Sounds

'''Screen Settings'''
width = 405
height = 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird") #FILL IN THE BLANK

'''Time Settings'''
clock = pygame.time.Clock()
fps = 60

'''Message Settings'''
score = 0
font_name = pygame.font.match_font("comicsansms")

#Images/ Sounds
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, "img")

#Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird   #If you have an image for the sprite, use this
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, height/2) #Centers the Rectangle
        self.last_jump = pygame.time.get_ticks()
        self.speed_y = 0

    def jump(self):
        keystate = pygame.key.get_pressed()
        self.speed_y = 7
        if keystate[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            self.speed_y = -7
    

        self.rect.y += self.speed_y

    def restart(self):
        self.rect.center = (width/2, height/2) #Centers the Rectangle

    def update(self):
        self.jump()

class Base_1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = base
        self.rect = self.image.get_rect()
        self.rect.bottom = height

    def boundary(self):
        if self.rect.right <= 0:
            self.rect.x = width

    def restart(self):
        pass

    def update(self):
        self.rect.x -= 5
        self.boundary()

class Base_2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = base
        self.rect = self.image.get_rect()
        self.rect.bottom = height
        self.rect.x = width

    def boundary(self):
        if self.rect.right <= 0:
            self.rect.x = width

    def restart(self):
        pass

    def update(self):
        self.rect.x -= 5
        self.boundary()
            

y = random.randrange(-150, 0)

class Pipe_1(pygame.sprite.Sprite):
    def __init__(self):
        global y
        pygame.sprite.Sprite.__init__(self)
        self.image = top_pipe
        self.rect = self.image.get_rect()
        self.rect.left = width
        self.rect.y = y
 
    def spawn_new_pipe(self):
        global y
        y = random.randrange(-250, 0)
        self.rect.y = y
        self.rect.x = width

    def boundary(self):
        if self.rect.right <= 0:
            self.spawn_new_pipe()

    def score(self):
        global score
        if self.rect.x in range(int((width/2)-2), int((width/2)+2)):
            score += 1
            int(score)

    def restart(self):
        self.rect.y = y
        self.rect.x = width
            

    def update(self):
        self.rect.x -= 5
        self.boundary()
        self.score()

class Pipe_2(pygame.sprite.Sprite):
    def __init__(self):
        global y
        pygame.sprite.Sprite.__init__(self)
        p = Pipe_1()
        self.image = bottom_pipe
        self.rect = self.image.get_rect()
        self.rect.left = width
        self.rect.top = y + 470

    def spawn_new_pipe(self):
        global y
        p = Pipe_1()
        self.rect.top = y + 500
        self.rect.x = width

    def boundary(self):
        if self.rect.right <= 0:
            self.spawn_new_pipe()

    def restart(self):
        self.rect.left = width
        self.rect.top = y + 470

    def update(self):
        self.rect.x -= 5
        self.boundary()
        
#Functions
def get_image(folder, file):
    img = pygame.image.load(path.join(folder, file))
    return img

def add_sprite(name):
    all_sprites.add(name)

def message(message, color, font_size, x, y):
    '''Display messages to the screen'''
    font = pygame.font.SysFont(font_name, font_size)
    text = font.render(message, True, color)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    screen.blit(text, text_rect)

#Images/ Sounds
'''Bird'''
bird = get_image(img_folder, "yellowbird0.png")
bird = pygame.transform.scale(bird, (50, 35))

'''Background'''
bg = get_image(img_folder, "background.png")
bg = pygame.transform.scale(bg, (405, 720))
bg_rect = bg.get_rect()

'''Pipe'''
top_pipe = get_image(img_folder, "top pipe.png")
bottom_pipe = get_image(img_folder, "bottom pipe.png")

'''Base'''
base = get_image(img_folder, "base.png")
base = pygame.transform.scale(base, (405, 135))

#Sprites
all_sprites = pygame.sprite.Group() #Group all Sprites
all_dangers = pygame.sprite.Group()
player = Player()
pipe_1 = Pipe_1()
pipe_2 = Pipe_2()
base_1 = Base_1()
base_2 = Base_2()
sprites = [player, pipe_1, pipe_2, base_1, base_2]
dangers = [pipe_1, pipe_2, base_1, base_2]
for i in sprites:
    add_sprite(i)

for i in dangers:
    all_dangers.add(i)

#Main
run = True
keystate = pygame.key.get_pressed()
while run:
    clock.tick(fps)
    screen.fill(white)
    message("Press Space to Start", black, 50, width/2, height/2)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                run = False
    
    pygame.display.update()

run = True
loop = True
restart = True

while loop:
    while run:
        
        #Keep Game at 60 FPS
        clock.tick(fps)

        #Check for Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #Check For Collision
        collision = pygame.sprite.spritecollide(player, all_dangers, False)
        for i in collision:
            restart = True
            while restart:
                clock.tick(fps)
                screen.fill(white)
                message("Game Over!", black, 50, width/2, height/2 - 60)
                message("Your score: " + str(score), black, 50, width/2, height/2 - 30)
                message("Press Enter to Restart!", black, 50, width/2, height/2)
                message("Press Escape to Exit!", black, 50, width/2, height/2 + 30)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            score = 0
                            player.restart()
                            pipe_1.spawn_new_pipe()
                            pipe_2.spawn_new_pipe()
                            restart = False
                        if event.key == pygame.K_ESCAPE:
                            loop = False
                            os._exit(0)
    
                pygame.display.update()
            #run = False
            #os._exit(0)
            

        #Update Sprites
        all_sprites.update()

        #Draw/ Render
        screen.fill(black)
        screen.blit(bg, bg_rect)
        all_sprites.draw(screen)
        message("Score: " + str(score), white, 24, 35, 10)
        
        #Update the Display
        pygame.display.update()


    
