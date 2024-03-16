#Створи власний Шутер!
import random
from pygame import *

window = display.set_mode((700, 500))

bg = image.load("galaxy.jpg")
bg = transform.scale(bg, (700, 500))

game = True
clock = time.Clock()

mixer.init()
space = mixer.Sound("space.ogg")
space.play()

class Hero(sprite.Sprite):
    def __init__ (self, x, y, width, height, speed, img_name="rocket.png"):
        super().__init__()

        self.image = image.load(img_name)
        self.image = transform.scale(self.image, (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
        
class Player(Hero):
    def move (self):
        keys = key.get_pressed()
        if keys [K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys [K_d] and self.rect.x < 700:
            self.rect.x += self.speed

class Enemy (Hero):
    def move(self):
        self.rect.y += self.speed
        if self.rect.y > 560:
            self.rect.x = random.randint(100, 565)
            self.rect.y = -100
        

rocket = Player(350,400,50,100,5)
enemy1 = Enemy (350, -100, 150, 50, 3, "ufo.png")

while game:
    window.blit(bg, (0,0))

    for e in event.get():
        if e.type == QUIT:
            game = False

    enemy1.reset()
    enemy1.move()
    rocket.reset()
    rocket.move()
    clock.tick(60)
    display.update()
