import sys
import pygame

# For ChatGPT usage report, read ChatGPT_kaytto_raportti.md

class Profile:
    """Class to handle profile selecting interface
    """
    def __init__(self, window, test=False):
        """Class constructor whitch gets pygame screen as a variable

        Args:
            window (pygame.display.set_mode): pygame screen spesifications
        """
        pygame.init()
        self.screen = window
        self.colors = self.color_init()
        self.profiles = ["gamer1", "gamer2", "gamer3"]
        self.selected_profile_index = 0
        self.font = pygame.font.SysFont(None, 40)
        self.selected_profile = None
        self.test = test

    def color_init(self):
        """Initalises all colors used by the program

        Returns:
            Dict: [color]:(tuple of color codes for pygame)
        """
        colors = {}
        colors["white"] = (255, 255, 255)
        colors["black"] = (0, 0, 0)
        colors["red"] = (255, 0, 0)
        colors["green"] = (0, 255, 0)
        return colors

    def key_event_handler(self, event):
        """Checks if event includes commands to move or confirm profile selector

        Args:
            event (pygame.KEYDOWN): keypress from user
        """
        if event.key == pygame.K_UP:
            self.selected_profile_index =\
                  (self.selected_profile_index - 1) % len(self.profiles)
        elif event.key == pygame.K_DOWN:
            self.selected_profile_index =\
                  (self.selected_profile_index + 1) % len(self.profiles)
        elif event.key == pygame.K_RETURN:
            self.selected_profile = self.profiles[self.selected_profile_index]

    def simulate_key_press(self, key):
        """Used in testing to inject keypresses to pygame event log.

        Args:
            key (pygame.K_"key"): pygame key code
        """
        event = pygame.event.Event(pygame.KEYDOWN, key=key)
        pygame.event.post(event)

    def mainloop(self):
        """Main loop of profile selector which draws the screen 
        and return chosen profile to mainmenu.

        Returns:
            str: selected profile name
        """
        running = True
        self.selected_profile = None
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.key_event_handler(event)
            self.screen.fill(self.colors["black"])
            if self.selected_profile is not None:
                return self.selected_profile

            # Display profile options
            for i, selected in enumerate(self.profiles):
                text_color = self.colors["green"] if i == self.selected_profile_index\
                      else self.colors["red"]
                text_surface = self.font.render(selected, True, text_color)
                text_rect = text_surface.get_rect(center=(800 // 2, 100 + i * 50))
                self.screen.blit(text_surface, text_rect)

            # Update the display
            pygame.display.flip()

            if self.test is True:
                return None

        # Quit Pygame
        pygame.quit()
        sys.exit()
