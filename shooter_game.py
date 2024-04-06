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
# space.play()2

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


class Bullet(Hero):
    def move(self):
        self.rect.y -= self.speed
        if (self.rect.y < 0):
            self.kill()


class Player(Hero):
    def move (self):
        keys = key.get_pressed()
        if keys [K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys [K_d] and self.rect.x < 700:
            self.rect.x += self.speed
        
    

    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.y, 10, 10, 10, 'bullet.png')
        bullets.add(bullet)

bullets = sprite.Group()

class Enemy (Hero):
    def move(self):
        self.rect.y += self.speed
        global counter
        if self.rect.y > 560:
            counter += 1
            self.rect.x = random.randint(50, 565)
            self.speed = random.randint(1,4)
            self.rect.y = -100

class Asteroid(Hero):   
    def move(self): 
        self.rect.y += self.speed
        self.rect.x += self.speed
        if self.rect.y > 560 or self.rect.x > 750:
            self.rect.x = random.randint(-200, 200)
            self.rect.y = -random.randint(50, 150)


rocket = Player(350,400,35,85,5)

# Створення НЛО
enemys = sprite.Group()
for i in range(5):
    enemy1 = Enemy (random.randint(50, 565), -100, 70, 30, random.randint(1,4), "ufo.png")
    enemys.add(enemy1)

# Створення астероїдів    
asteroids = sprite.Group()
for i in range(5):
    asteroid = Asteroid(random.randint(-200, 200), -random.randint(50, 150), 30, 30, random.randint(1,3), "asteroid.png")
    asteroids.add(asteroid)


font.init()
font1 = font.Font(None, 40)
font_win = font.Font(None, 60)

finish = False
lifes = 3
counter = 0
killed = 0

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
            if e.key == K_r:
                lifes = 3
                killed = 0
                counter = 0
                finish = False

                for i in enemys:
                    i.rect.y = -random.randint(50, 200)
                    i.rect.x = random.randint(50, 565)

                for i in asteroids:
                    i.rect.y = -random.randint(50, 200)
                    i.rect.x = random.randint(-200, 200)



    window.blit(bg, (0,0)) 

    if finish != True:
        window.blit(font1.render(f"Лічилник: {counter}",True, (255,255,255), (0,0,0)), (0,0))
        window.blit(font1.render(f"Життя: {lifes}",True, (255,255,255), (0,0,0)), (0,50))
        window.blit(font1.render(f"Збито: {killed}",True, (255,255,255), (0,0,0)), (0,100))
        for i in enemys:
            i.reset()
            i.move()

        for b in bullets:
            b.reset()
            b.move()

        for a in asteroids:
            a.reset()
            a.move()

        if counter >= 5:
            finish = True

    
        list_collides = sprite.spritecollide(rocket, enemys, False)
        for collide in list_collides:
            if collide:
                lifes -= 1

                if lifes == 0:
                    finish = True

                for i in enemys:
                    i.rect.y = -random.randint(50, 200)
                    i.rect.x = random.randint(50, 565)


        list_collides = sprite.spritecollide(rocket, asteroids, True)
        for collide in list_collides:
            if collide:
                lifes -= 1
                if lifes == 0:
                    finish = True
                asteroid = Asteroid(random.randint(-200, 200), -random.randint(50, 150), 30, 30, random.randint(1,3), "asteroid.png")
                asteroids.add(asteroid)
                

        list_collides = sprite.groupcollide(enemys, bullets, True, True)
        for collide in list_collides:
            if collide:
                killed += 1
                if killed == 100:
                    finish = True

                enemy1 = Enemy (random.randint(50, 565), -100, 70, 30, random.randint(1,4), "ufo.png")
                enemys.add(enemy1)


        rocket.reset()
        rocket.move()

    if finish == True:
        if killed == 100:
            window.blit(font_win.render("YOU WIN", True, (0,255,0)), (250, 240))

        if lifes == 0 or counter == 5:
            window.blit(font_win.render("YOU LOSE", True, (255,0,0)), (250, 240))

        window.blit(font1.render("For restart press R",True, (255,255,255)), (230, 300))


    clock.tick(60)
    display.update()
