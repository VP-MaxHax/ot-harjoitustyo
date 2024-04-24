import unittest
from upgrades import Upgrades
from entities import Player, Vampire, Bullet, Pickup
from gameloop import Game
import pygame

class TestGameloop(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.upgrade = Upgrades(self.player)
        self.game = Game()

    def test_spawn_a_vampire(self):
        self.game.spawn_vampire()
        self.assertEqual(len(self.game.vampires), 1)

    def test_spawn_many_vampires(self):
        for _ in range(5):
            self.game.spawn_vampire()
        self.assertEqual(len(self.game.vampires), 5)

    def test_event_to_spawn_a_vampire(self):
        spawn_vampire_event = pygame.USEREVENT + 1
        event = pygame.event.Event(spawn_vampire_event)
        pygame.event.post(event)
        self.game.handle_events()
        self.assertEqual(len(self.game.vampires), 1)

    def test_event_to_quit_the_game(self):
        event = pygame.event.Event(pygame.QUIT)
        pygame.event.post(event)
        running = self.game.handle_events()
        self.assertEqual(running, False)

    def test_gameover_events_to_quit_the_game(self):
        event = pygame.event.Event(pygame.QUIT)
        running = self.game.check_gameover_events(event, True)
        self.assertEqual(running, "Returned only in testing")

    def test_gameover_events_to_continue_to_menu(self):
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
        running = self.game.check_gameover_events(event)
        self.assertEqual(running, False)

    def test_gameover_events_to_stay_on_gameover_screen(self):
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_KP_ENTER)
        running = self.game.check_gameover_events(event)
        self.assertEqual(running, True)

    def test_gameover_handler_continues_to_mainmenu_after_keypress(self):
        running = self.game.gameover(True)
        self.assertEqual(running, "GameOver")

    def test_upgarde_choises_are_returned_correctly_firerate(self):
        value = self.game.upgrade_choices(1)
        font = pygame.font.SysFont("Arial", 24)
        self.assertEqual(pygame.image.tostring(value, 'RGBA'),
                         pygame.image.tostring(font.render("Firerate", True, (255, 0, 0)), 'RGBA'))

    def test_upgarde_choises_are_returned_correctly_mov_speed(self):
        value = self.game.upgrade_choices(2)
        font = pygame.font.SysFont("Arial", 24)
        self.assertEqual(pygame.image.tostring(value, 'RGBA'),
                         pygame.image.tostring(font.render("Mov speed", True, (255, 0, 0)), 'RGBA'))
        
    def test_upgarde_choises_are_returned_correctly_blt_speed(self):
        value = self.game.upgrade_choices(3)
        font = pygame.font.SysFont("Arial", 24)
        self.assertEqual(pygame.image.tostring(value, 'RGBA'),
                         pygame.image.tostring(font.render("Blt speed", True, (255, 0, 0)), 'RGBA'))

    def test_upgarde_choises_are_returned_correctly_pickup_range(self):
        value = self.game.upgrade_choices(4)
        font = pygame.font.SysFont("Arial", 24)
        self.assertEqual(pygame.image.tostring(value, 'RGBA'),
                         pygame.image.tostring(font.render("Pickup range", True, (255, 0, 0)), 'RGBA'))

    def test_upgarde_choises_are_returned_correctly_xp_rate(self):
        value = self.game.upgrade_choices(5)
        font = pygame.font.SysFont("Arial", 24)
        self.assertEqual(pygame.image.tostring(value, 'RGBA'),
                         pygame.image.tostring(font.render("Xp rate", True, (255, 0, 0)), 'RGBA'))

    def test_upgarde_choises_are_returned_correctly_blt_pierce(self):
        value = self.game.upgrade_choices(6)
        font = pygame.font.SysFont("Arial", 24)
        self.assertEqual(pygame.image.tostring(value, 'RGBA'),
                         pygame.image.tostring(font.render("Blt pierce", True, (255, 0, 0)), 'RGBA'))    

    def test_upgarde_choises_are_returned_correctly_blt_size(self):
        value = self.game.upgrade_choices(7)
        font = pygame.font.SysFont("Arial", 24)
        self.assertEqual(pygame.image.tostring(value, 'RGBA'),
                         pygame.image.tostring(font.render("Blt size", True, (255, 0, 0)), 'RGBA')) 
        
    def test_wait_for_lvlup_confirmation_no_event(self):
        value = self.game.level_up_check_event([1,2,3])
        self.assertEqual(value, True)
        
    def test_wait_for_lvlup_confirmation_k1_event(self):
        value = self.game.level_up_check_event([1,2,3], True, pygame.event.Event(pygame.KEYDOWN, key=pygame.K_1))
        self.assertEqual(value, False)

    def test_wait_for_lvlup_confirmation_k2_event(self):
        value = self.game.level_up_check_event([1,2,3], True, pygame.event.Event(pygame.KEYDOWN, key=pygame.K_2))
        self.assertEqual(value, False)

    def test_wait_for_lvlup_confirmation_k3_event(self):
        value = self.game.level_up_check_event([1,2,3], True, pygame.event.Event(pygame.KEYDOWN, key=pygame.K_3))
        self.assertEqual(value, False)

    def test_wait_for_lvlup_confirmation_k4_event(self):
        value = self.game.level_up_check_event([1,2,3], True, pygame.event.Event(pygame.KEYDOWN, key=pygame.K_4))
        self.assertEqual(value, True)

    def test_wait_for_lvlup_confirmation_quit_event(self):
        value = self.game.level_up_check_event([1,2,3], True, pygame.event.Event(pygame.QUIT))
        self.assertEqual(value, "Returned only in testing")

    def test_choose_closest_vampire_from_two(self):
        vampire1 = Vampire(self.player)
        vampire1.rect.x = 100
        vampire1.rect.y = 300
        self.game.vampires.add(vampire1)
        vampire2 = Vampire(self.player)
        vampire2.rect.x = 200
        vampire2.rect.y = 300
        self.game.vampires.add(vampire2)
        closest = self.game.find_closest_vampire()
        self.assertEqual((closest.rect.x, closest.rect.y), (200,300))

    def test_choose_closest_vampire_from_many(self):
        vampire1 = Vampire(self.player)
        vampire1.rect.x = 600
        vampire1.rect.y = 300
        self.game.vampires.add(vampire1)
        vampire2 = Vampire(self.player)
        vampire2.rect.x = 200
        vampire2.rect.y = 300
        self.game.vampires.add(vampire2)
        vampire3 = Vampire(self.player)
        vampire3.rect.x = 400
        vampire3.rect.y = 125
        self.game.vampires.add(vampire3)
        vampire4 = Vampire(self.player)
        vampire4.rect.x = 400
        vampire4.rect.y = 600
        self.game.vampires.add(vampire4)
        closest = self.game.find_closest_vampire()
        self.assertEqual((closest.rect.x, closest.rect.y), (400,125))