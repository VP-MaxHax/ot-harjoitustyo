import unittest
import pygame
from profile_select import Profile

class TestProfile(unittest.TestCase):
    def setUp(self):
        screen = pygame.display.set_mode((800, 600))
        self.profile = Profile(screen)

    def test_class_loads_up_correctly(self):
        screen = pygame.display.set_mode((800, 600))
        profile = Profile(screen, True)
        profile.mainloop()
        self.assertEqual(self.profile.selected_profile, None)

    def test_selecting_profile_works(self):
        self.profile.simulate_key_press(pygame.K_RETURN)
        selected_profile = self.profile.mainloop()
        self.assertEqual(selected_profile, "gamer1")

    def test_changing_profile_with_arrows_works(self):
        self.profile.simulate_key_press(pygame.K_DOWN)
        self.profile.simulate_key_press(pygame.K_RETURN)
        selected_profile = self.profile.mainloop()
        self.assertEqual(selected_profile, "gamer2")

    def test_selecting_third_profile_works(self):
        self.profile.simulate_key_press(pygame.K_DOWN)
        self.profile.simulate_key_press(pygame.K_DOWN)
        self.profile.simulate_key_press(pygame.K_RETURN)
        selected_profile = self.profile.mainloop()
        self.assertEqual(selected_profile, "gamer3")

    def test_selector_loops_correctly_when_going_up_from_top(self):
        self.profile.simulate_key_press(pygame.K_UP)
        self.profile.simulate_key_press(pygame.K_RETURN)
        selected_profile = self.profile.mainloop()
        self.assertEqual(selected_profile, "gamer3")

    def test_selector_loops_correctly_when_going_down_from_bottom(self):
        self.profile.simulate_key_press(pygame.K_DOWN)
        self.profile.simulate_key_press(pygame.K_DOWN)
        self.profile.simulate_key_press(pygame.K_DOWN)
        self.profile.simulate_key_press(pygame.K_RETURN)
        selected_profile = self.profile.mainloop()
        self.assertEqual(selected_profile, "gamer1")