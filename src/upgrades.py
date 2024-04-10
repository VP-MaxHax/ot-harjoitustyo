import random

# Define upgrades


class Upgrades:
    def __init__(self, player):
        self.upg = []
        self.options = [1, 2, 3, 4, 5, 6, 7]
        self.player = player

    def firerate_upg(self):
        self.player.stats.shoot_delay = int(self.player.stats.shoot_delay*0.9)

    def speed_upg(self):
        self.player.stats.mv_speed += 1

    def bult_spd_upg(self):
        self.player.stats.bullet_speed += 3

    def pickup_upg(self):
        self.player.stats.pickupradius += 50

    def exprate_upg(self):
        self.player.stats.exprate += 1

    def blt_prs_upg(self):
        self.player.stats.pierce += 1

    def blt_sz_upg(self):
        self.player.stats.bullet_size += 2

    def pick_options(self):
        picked_options = random.sample(self.options, 3)
        return picked_options

    def chosen_upgrade(self, chosen):
        match chosen:
            case 1:
                self.firerate_upg()
                change = True

            case 2:
                self.speed_upg()
                change = True

            case 3:
                self.bult_spd_upg()
                change = True

            case 4:
                self.pickup_upg()
                change = True

            case 5:
                self.exprate_upg()
                change = True

            case 6:
                self.blt_prs_upg()
                change = True

            case 7:
                self.blt_sz_upg()
                change = True

            case _:
                # Default case if chosen doesn't match any of the above cases
                # Handle the default behavior here or simply pass if not needed
                change = False
        return change
