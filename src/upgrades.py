import random

# Define upgrades    
class Upgrades:
    def __init__(self, player):
        self.upg = []
        self.options = [1,2,3,4,5,6,7]
        self.player = player

    def firerate_upg(self):
        self.player.shoot_delay = int(self.player.shoot_delay*0.9)

    def speed_upg(self):
        self.player.mv_speed += 1

    def bult_spd_upg(self):
        self.player.bullet_speed += 3

    def pickup_upg(self):
        self.player.pickupradius += 50

    def exprate_upg(self):
        self.player.exprate += 1

    def blt_prs_upg(self):
        self.player.pierce += 1

    def blt_sz_upg(self):
        self.player.bullet_size += 2

    def pick_options(self):
        picked_options = random.sample(self.options, 3)
        return picked_options
    
    def chosen_upgrade(self, chosen):
        match chosen:
            case 1:
                self.firerate_upg()
            
            case 2:
                self.speed_upg()

            case 3:
                self.bult_spd_upg()

            case 4:
                self.pickup_upg()

            case 5:
                self.exprate_upg()

            case 6:
                self.blt_prs_upg()

            case 7:
                self.blt_sz_upg()
