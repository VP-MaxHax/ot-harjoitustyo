import sys
import pygame
from gameloop import Game

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Vampire Survivor")
white = (255, 255, 255)
black = (0, 0, 0)
game = Game()
RUNNING = True
while RUNNING:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F2:
                game.run()
        screen.fill(black)
        font = pygame.font.SysFont("Arial", 100)
        screen.blit(font.render("Vampire Survivor",
                    True, (255, 0, 0)), (50, 100))
        font = pygame.font.SysFont("Arial", 30)
        screen.blit(font.render("Press F2 to start game",
                    True, (255, 0, 0)), (285, 400))
        pygame.display.flip()
        pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()
