import pygame
import sys

pygame.init()

width = 800
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game PBO")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.width = 50
        self.height = 50

        self.speed = 5
        self.color = black

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed

        if self.x < 0:
            self.x = 0
        if self.x > width - self.width:
            self.x = width - self.width
        if self.y < 0:
            self.y = 0
        if self.y > height - self.height:
            self.y = height - self.height
        
        if keys[pygame.K_q]:
            self.speed -= 0.01
        if keys[pygame.K_e]:
            self.speed += 0.01
        if self.speed < 0.5:
            self.speed = 0.5
        if self.speed > 10:
            self.speed = 10

    def size(self, keys):
        if keys[pygame.K_p]:
            self.width += 0.5
            self.height += 0.5
        if keys[pygame.K_o]:
            self.width -= 0.5
            self.height -= 0.5
        if self.width < 20:
            self.width = 20
        if self.height < 20:
            self.height = 20
        if self.width > 400:
            self.width = 400
        if self.height > 400:
            self.height = 400

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
player = Player (375, 275)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player.color = red
            if event.key == pygame.K_g:
                player.color = green
            if event.key == pygame.K_b:
                player.color = blue
            if event.key == pygame.K_n:
                player.color = black

    keys = pygame.key.get_pressed()
    player.move(keys)
    player.size(keys)

    screen.fill(white)
    player.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()