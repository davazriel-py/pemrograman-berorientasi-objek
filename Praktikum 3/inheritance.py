import pygame
import sys

pygame.init()

WIDHT = 600
HEIGHT = 400

screen = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption("Game kejar maling")

white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
black = (0, 0, 0)


class Character:

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = 0.5
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Polisi(Character):

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        if self.x < 0:
            self.x = 0
        if self.x > WIDHT - self.width:
            self.x = WIDHT - self.width
        if self.y < 0:
            self.y = 0
        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height



class Maling(Character):

    def move(self, keys):
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
        if self.x > WIDHT - self.width:
            self.x = WIDHT - self.width
        if self.y < 0:
            self.y = 0
        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height


polisi = Polisi(100, 200, blue)
maling = Maling(400, 200, red)

running = True

game_over = False

def reset_game():
    global polisi, maling, game_over
    polisi = Polisi(100, 200, blue)
    maling = Maling(400, 200, red)
    game_over = False

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()

    keys = pygame.key.get_pressed()

    if not game_over:
        polisi.move(keys)
        maling.move(keys)

    if polisi.get_rect().colliderect(maling.get_rect()):
        game_over = True

    screen.fill(white)
    
    polisi.draw(screen)
    maling.draw(screen)

    if game_over:
        font = pygame.font.SysFont(None, 48)
        text = font.render("POLISI MENANG!", True, black)
        screen.blit(text, (180, 160))

        font2 = pygame.font.SysFont(None, 30)
        text2 = font2.render("Tekan R untuk restart", True, black)
        screen.blit(text2, (200, 210))

    pygame.display.update()

pygame.quit()
sys.exit()