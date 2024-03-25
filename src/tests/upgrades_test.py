from upgrades import Upgrades
from entities import Player
import unittest

class TestUpgrades(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.upgrade = Upgrades(self.player)

    def test_firerate_upgrade_working_correctly(self):
        self.upgrade.firerate_upg()
        self.assertEqual(self.player.shoot_delay, 900)

    def test_speed_upgrade_working_correctly(self):
        self.upgrade.speed_upg()
        self.assertEqual(self.player.mv_speed, 6)

    def test_bullet_speed_upgrade_working_correctly(self):
        self.upgrade.bult_spd_upg()
        self.assertEqual(self.player.bullet_speed, 8)

    def test_pickup_range_upgrade_working_correctly(self):
        self.upgrade.pickup_upg()
        self.assertEqual(self.player.pickupradius, 70)

    def test_exprate_upgrade_working_correctly(self):
        self.upgrade.exprate_upg()
        self.assertEqual(self.player.exprate, 2)

    def test_bullet_pierce_upgrade_working_correctly(self):
        self.upgrade.blt_prs_upg()
        self.assertEqual(self.player.pierce, 2)

    def test_bullet_size_upgrade_working_correctly(self):
        self.upgrade.blt_sz_upg()
        self.assertEqual(self.player.bullet_size, 12)