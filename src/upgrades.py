import random

# Define upgrades


class Upgrades:
    """Class that handles handing out upgrade choices and applying player upgrades
    """
    def __init__(self, player):
        """Class constructor that gets player class variable to apply upgrades to

        Args:
            player (Player()): Player class object
        """
        self.upg = []
        self.options = [1, 2, 3, 4, 5, 6, 7]
        self.player = player

    def firerate_upg(self):
        """Applies firerate upgrade to player object
        """
        self.player.stats.shoot_delay = int(self.player.stats.shoot_delay*0.9)

    def speed_upg(self):
        """Applies movement speed upgrade to player object
        """
        self.player.stats.mv_speed += 1

    def bult_spd_upg(self):
        """Applies bullet speed upgrade to player object
        """
        self.player.stats.bullet_speed += 3

    def pickup_upg(self):
        """Applies pickup radius upgrade to player object
        """
        self.player.stats.pickupradius += 50

    def exprate_upg(self):
        """Applies experience gain rate upgrade to player object
        """
        self.player.stats.exprate += 1

    def blt_prs_upg(self):
        """Applies bullet pierce upgrade to player object
        """
        self.player.stats.pierce += 1

    def blt_sz_upg(self):
        """Applies bullet size upgrade to player object
        """
        self.player.stats.bullet_size += 2

    def pick_options(self):
        """Picks 3 random elements from self.options and passes them forward

        Returns:
            list: 3 elements that reflect different upgrades
        """
        picked_options = random.sample(self.options, 3)
        return picked_options

    def chosen_upgrade(self, chosen):
        """Upgrades players stat basec on the 'chosen' variable

        Args:
            chosen (int): number reflecting an upgrade

        Returns:
            bool: bool value for tests to see if something was changed
        """
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
