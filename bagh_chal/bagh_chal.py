import sys, pygame
from pygame import Rect

black = (0, 0, 0)
# The call to pygame.init() initializes each of these modules.
pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Bagh-Chal")
goat = pygame.image.load("./images/goat.png")
goatrect = goat.get_rect()
# rect = Rect(200, 200, 100, 100)
# rect1 = rect.get_rect()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill(black)

    screen.blit(goat, goatrect)
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(200, 200, 100, 100))

    pygame.display.flip()
