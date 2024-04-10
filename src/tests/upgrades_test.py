import unittest
from upgrades import Upgrades
from entities import Player


class TestUpgrades(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.upgrade = Upgrades(self.player)

    def test_firerate_upgrade_working_correctly(self):
        self.upgrade.firerate_upg()
        self.assertEqual(self.player.stats.shoot_delay, 900)

    def test_speed_upgrade_working_correctly(self):
        self.upgrade.speed_upg()
        self.assertEqual(self.player.stats.mv_speed, 6)

    def test_bullet_speed_upgrade_working_correctly(self):
        self.upgrade.bult_spd_upg()
        self.assertEqual(self.player.stats.bullet_speed, 8)

    def test_pickup_range_upgrade_working_correctly(self):
        self.upgrade.pickup_upg()
        self.assertEqual(self.player.stats.pickupradius, 70)

    def test_exprate_upgrade_working_correctly(self):
        self.upgrade.exprate_upg()
        self.assertEqual(self.player.stats.exprate, 2)

    def test_bullet_pierce_upgrade_working_correctly(self):
        self.upgrade.blt_prs_upg()
        self.assertEqual(self.player.stats.pierce, 2)

    def test_bullet_size_upgrade_working_correctly(self):
        self.upgrade.blt_sz_upg()
        self.assertEqual(self.player.stats.bullet_size, 12)

    def test_upgrade_options_list_correct_length(self):
        options = self.upgrade.pick_options()
        self.assertEqual(len(options), 3)

    def test_upgrade_options_list_in_correct_range(self):
        in_range = True
        i = 0
        while i < 100 and in_range:
            options = self.upgrade.pick_options()
            for j in options:
                if j not in [1, 2, 3, 4, 5, 6, 7]:
                    in_range = False
            i += 1
        self.assertEqual(in_range, True)

    def test_firerate_chosen_working_correctly(self):
        self.upgrade.chosen_upgrade(1)
        self.assertEqual(self.player.stats.shoot_delay, 900)

    def test_speed_chosen_working_correctly(self):
        self.upgrade.chosen_upgrade(2)
        self.assertEqual(self.player.stats.mv_speed, 6)

    def test_bullet_speed_chosen_working_correctly(self):
        self.upgrade.chosen_upgrade(3)
        self.assertEqual(self.player.stats.bullet_speed, 8)

    def test_pickup_range_chosen_working_correctly(self):
        self.upgrade.chosen_upgrade(4)
        self.assertEqual(self.player.stats.pickupradius, 70)

    def test_exprate_chosen_working_correctly(self):
        self.upgrade.chosen_upgrade(5)
        self.assertEqual(self.player.stats.exprate, 2)

    def test_bullet_pierce_chosen_working_correctly(self):
        self.upgrade.chosen_upgrade(6)
        self.assertEqual(self.player.stats.pierce, 2)

    def test_bullet_size_chosen_working_correctly(self):
        self.upgrade.chosen_upgrade(7)
        self.assertEqual(self.player.stats.bullet_size, 12)

    def test_default_case_returning_correct_value(self):
        value = self.upgrade.chosen_upgrade("defaultcase")
        self.assertEqual(value, False)
        