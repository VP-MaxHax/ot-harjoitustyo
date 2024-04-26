import sys
import pygame
from gameloop import Game
from profile_select import Profile

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Vampire Survivor")
profile = Profile(screen)
SELECTED_PROFILE = "gamer1"
white = (255, 255, 255)
black = (0, 0, 0)
RUNNING = True
while RUNNING:
    # Handle events
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F2:
                game = Game(SELECTED_PROFILE, screen)
                game.run()
            if event.key == pygame.K_F3:
                SELECTED_PROFILE = profile.mainloop()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        screen.fill(black)
        font = pygame.font.SysFont("Arial", 100)
        screen.blit(font.render("Vampire Survivor",
                    True, (255, 0, 0)), (50, 100))
        font = pygame.font.SysFont("Arial", 30)
        screen.blit(font.render("Press F2 to start game",
                    True, (255, 0, 0)), (285, 300))
        screen.blit(font.render("Press F3 to select profile",
                    True, (255, 0, 0)), (285, 400))
        screen.blit(font.render(f"Now selected: {SELECTED_PROFILE}",
                    True, (255, 0, 0)), (285, 450))
        pygame.display.flip()
        pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()
