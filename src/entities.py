import random
import math
import pygame

# For ChatGPT usage report, read ChatGPT_kaytto_raportti.md

WIDTH, HEIGHT = 800, 600

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define the player class
class Player(pygame.sprite.Sprite):
    """Class that handles players stats and other variables

    Args:
        pygame (pygame.sprite.Sprite): pygame sprite data
    """
    def __init__(self):
        """Constructor for player class object
        """
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.stats = PlayerStats()


    def update(self, keypress=None):
        """Player movement based on keys pressed

        Args:
            keypress (pygame.key, optional): 
            Used on testing to input movement command. 
            Defaults to None.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keypress == "left":
            self.rect.x -= self.stats.mv_speed
        if keys[pygame.K_RIGHT] or keypress == "right":
            self.rect.x += self.stats.mv_speed
        if keys[pygame.K_UP] or keypress == "up":
            self.rect.y -= self.stats.mv_speed
        if keys[pygame.K_DOWN] or keypress == "down":
            self.rect.y += self.stats.mv_speed

    def shoot(self, closest_vampire):
        """Triggers the player to shoot towards closest vampire when timer epires

        Args:
            closest_vampire (Vampire): vampire class object

        Returns:
            bullet()(if fired), bool: return bullet and info if bullet was fired
        """
        # Shoot towards the closest vampire
        now = pygame.time.get_ticks()
        if now - self.stats.last_shot > self.stats.shoot_delay:
            self.stats.last_shot = now
            if closest_vampire:
                dx = closest_vampire.rect.centerx - self.rect.centerx
                dy = closest_vampire.rect.centery - self.rect.centery
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance != 0:
                    bullet = Bullet(self.rect.centerx, self.rect.centery,\
                                     dx / distance, dy / distance, (self.stats.bullet_speed,\
                                          self.stats.bullet_size, self.stats.pierce))
                    return bullet, True
        return None, False

class PlayerStats:
    """Class that hold info of players stats
    """
    def __init__(self):
        self.shoot_delay = 1000  # milliseconds
        self.last_shot = pygame.time.get_ticks()
        self.score = 0
        self.pts_for_lvlup = 1
        self.nxt_lvl = 1
        self.mv_speed = 5
        self.bullet_speed = 5
        self.pickupradius = 20
        self.exprate = 1
        self.pierce = 1
        self.bullet_size = 10
        self.upgrades = (self.bullet_speed, self.bullet_size, self.pierce)

# Define the vampire class
class Vampire(pygame.sprite.Sprite):
    """Class that handles vampires variables

    Args:
        pygame (pygame.sprite.Sprite): pygame sprite data
    """
    def __init__(self, player):
        """Class constructor which holds vampire objects base info and stats

        Args:
            player (Player()): player object for vampire to get a target
        """
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.player = player
        self.speed = 1
        self.spawn_on_edge()

    def spawn_on_edge(self, side=None):
        """Spawns vampire on the edge of the screen

        Args:
            side (str, optional): 
            Used in testing to determine a spawn side for vampire. 
            Defaults to None.
        """
        if side is None:
            side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            self.rect.centerx = random.randint(0, WIDTH)
            self.rect.top = 0
        elif side == "bottom":
            self.rect.centerx = random.randint(0, WIDTH)
            self.rect.bottom = HEIGHT
        elif side == "left":
            self.rect.left = 0
            self.rect.centery = random.randint(0, HEIGHT)
        elif side == "right":
            self.rect.right = WIDTH
            self.rect.centery = random.randint(0, HEIGHT)

    def update(self):
        """Used to move vampire towards player every game tick
        """
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            dx /= distance
            dy /= distance
        # Move the vampire towards the player
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

# Define the bullet class
class Bullet(pygame.sprite.Sprite):
    """Class that handles bullet class variables

    Args:
        pygame (pygame.sprite.Sprite): pygame sprite data
    """
    def __init__(self, x, y, dx, dy, upgrades):
        """Class constructor which holds bullets objects base info and stats

        Args:
            x (int): current x axis location of the bullet
            y (int): current y axis location of the bullet
            dx (int): bullets movement speed in x axis
            dy (int): bullets movement speed in y axis
            upgrades (tuple): holds upgrade info for bullet 
            (bullet speed, bullet size, bullet pierce)
        """
        super().__init__()
        self.image = pygame.Surface((upgrades[1], upgrades[1]))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.bullet_speed = upgrades[0]
        self.speedx = self.bullet_speed * dx
        self.speedy = self.bullet_speed * dy
        self.pierce = upgrades[2]

    def update(self):
        """Updates bullets location on each tick. Also despawns bullet if it goes out of screen.
        """
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Kill the bullet if it goes off the screen
        if self.rect.bottom < 0 or self.rect.top > HEIGHT\
            or self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

# Define the pickup class
class Pickup(pygame.sprite.Sprite):
    """Class that handles pickup class variables

    Args:
        pygame (pygame.sprite.Sprite): pygame sprite data
    """
    def __init__(self, x, y, pickupradius):
        """Class constructor which holds bullets objects base info and stats

        Args:
            x (int): pickups location in x axis
            y (int): pickups location in y axis
            pickupradius (int): pickups radius based on players 'pickup radius' upgrade
        """
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center = (x, y))
        self.collision_box = pygame.Rect(x-(pickupradius // 2),
                                         y-(pickupradius // 2),
                                         pickupradius, pickupradius)
