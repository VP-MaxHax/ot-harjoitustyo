import unittest
import pygame
from upgrades import Upgrades
from entities import Player, Vampire
from gameloop import Game


class TestEntities(unittest.TestCase):
    def setUp(self):
        self.player = Player() # Player always start at the middle of the board (400, 300)
        self.upgrade = Upgrades(self.player)
        screen = pygame.display.set_mode((800, 600))
        self.game = Game("test", screen)

    def test_vampire_moves_correctly_towards_player_from_left(self):
        vampire = Vampire(self.player)
        vampire.rect.x = 100
        vampire.rect.y = 300
        for _ in range(10):
            vampire.update()
        self.assertEqual((vampire.rect.x, vampire.rect.y), (110, 300))

    def test_vampire_moves_correctly_towards_player_from_right(self):
        vampire = Vampire(self.player)
        vampire.rect.x = 500
        vampire.rect.y = 300
        for _ in range(10):
            vampire.update()
        self.assertEqual((vampire.rect.x, vampire.rect.y), (490, 300))

    def test_vampire_moves_correctly_towards_player_from_below(self):
        vampire = Vampire(self.player)
        vampire.rect.x = 400
        vampire.rect.y = 500
        for _ in range(10):
            vampire.update()
        self.assertEqual((vampire.rect.x, vampire.rect.y), (400, 490))

    def test_vampire_moves_correctly_towards_player_from_above(self):
        vampire = Vampire(self.player)
        vampire.rect.x = 400
        vampire.rect.y = 100
        for _ in range(10):
            vampire.update()
        self.assertEqual((vampire.rect.x, vampire.rect.y), (400, 110))

    def test_vampire_spawns_correctly_to_top_edge(self):
        vampire = Vampire(self.player)
        vampire.spawn_on_edge("top")
        self.assertEqual(vampire.rect.top, 0)

    def test_vampire_spawns_correctly_to_bottom_edge(self):
        vampire = Vampire(self.player)
        vampire.spawn_on_edge("bottom")
        self.assertEqual(vampire.rect.bottom, 600)

    def test_vampire_spawns_correctly_to_left_edge(self):
        vampire = Vampire(self.player)
        vampire.spawn_on_edge("left")
        self.assertEqual(vampire.rect.left, 0)

    def test_vampire_spawns_correctly_to_right_edge(self):
        vampire = Vampire(self.player)
        vampire.spawn_on_edge("right")
        self.assertEqual(vampire.rect.right, 800)

    def test_player_movement_left(self):
        for _ in range(10):
            self.player.update("left")
        self.assertEqual((self.player.rect.center), (350, 300))

    def test_player_movement_right(self):
        for _ in range(10):
            self.player.update("right")
        self.assertEqual((self.player.rect.center), (450, 300))

    def test_player_movement_down(self):
        for _ in range(10):
            self.player.update("down")
        self.assertEqual((self.player.rect.center), (400, 350))

    def test_player_movement_up(self):
        for _ in range(10):
            self.player.update("up")
        self.assertEqual((self.player.rect.center), (400, 250))
