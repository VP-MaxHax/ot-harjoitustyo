import unittest
import os
from upgrades import Upgrades
from entities import Player
from meta_upgrades import Meta

class TestMeta(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.upgrades = Upgrades(self.player)
        meta_setup = Meta(self.upgrades, "test")
        meta_setup.remove_test_profile()
        meta_setup.add_test_profile("0000000")
        self.meta = Meta(self.upgrades, "test")

    def test_meta_initialised_succesfully_with_correct_value(self):
        self.assertEqual(self.meta.meta_status, "0000000")

    def test_database_write_is_successfull(self):
        self.meta.update_data(3)
        data = self.meta.fetch_data()
        self.assertEqual(data, "0010000")

    def test_upgrades_dont_go_ove_9(self):
        for _ in range(15):
            self.meta.update_data(3)
        self.assertEqual(self.meta.meta_status, "0090000")

    def test_creating_new_database_works_correctly(self):
        if os.path.exists("test.db"):
            os.remove("test.db")
        testdb = Meta(self.upgrades, "test", "test.db")
        testg1 = Meta(self.upgrades, "gamer1", "test.db")
        testg2 = Meta(self.upgrades, "gamer2", "test.db")
        testg3 = Meta(self.upgrades, "gamer3", "test.db")
        self.assertEqual((testdb.meta_status, testg1.meta_status, testg2.meta_status, testg3.meta_status), ("0000000", "0000000", "0000000", "0000000"))
