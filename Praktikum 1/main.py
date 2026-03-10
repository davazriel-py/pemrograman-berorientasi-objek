import pygame
import sys

pygame.init()

WIDHT = 600
HEIGHT = 400

screen = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption("Game pertama")

netral = (0, 0, 0)
merah = (255, 0, 0)
hijau = (0, 255, 0)
biru = (0, 0, 255)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                netral = merah
            if event.key == pygame.K_g:
                netral = hijau
            if event.key == pygame.K_b:
                netral = biru
            if event.key == pygame.K_n:
                netral = (0, 0, 0)


    screen.fill(netral)
    pygame.display.flip()

pygame.quit()
sys.exit()