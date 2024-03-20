# Define upgrades    
class Upgrades:
    def __init__(self, player):
        self.upg = []
        self.player = player

    def firerate_upg(self):
        self.player.shoot_delay = int(self.player.shoot_delay*0.9)

    def speed_upg(self):
        self.player.mv_speed += 1

    def bult_spd_upg(self):
        self.player.bullet_speed += 1

    def pickup_upg(self):
        self.player.pickupradius += 50
        self.player.pickuparea = self.player.Surface((self.player.pickupradius, self.player.pickupradius))

    def exprate_upg(self):
        self.player.exprate += 1

    def blt_prs_upg(self):
        self.player.pierce += 1

    def blt_sz_upg(self):
        self.player.bullet_size += 2