import random
import math
import pygame

# All entities done with the help of Chat-GPT

WIDTH, HEIGHT = 800, 600

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define the player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
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


    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.mv_speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.mv_speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.mv_speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.mv_speed

    def shoot(self, closest_vampire):
        # Shoot towards the closest vampire
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if closest_vampire:
                dx = closest_vampire.rect.centerx - self.rect.centerx
                dy = closest_vampire.rect.centery - self.rect.centery
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance != 0:
                    bullet = Bullet(self.rect.centerx, self.rect.centery,\
                                     dx / distance, dy / distance, self.bullet_speed,\
                                          self.bullet_size, self.pierce)
                    return bullet, True
        return None, False
# Define the vampire class
class Vampire(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.player = player
        self.speed = 1
        self.spawn_on_edge()

    def spawn_on_edge(self):
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
    def __init__(self, x, y, dx, dy, bullet_speed, bullet_size, pierce):
        super().__init__()
        self.image = pygame.Surface((bullet_size, bullet_size))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.bullet_speed = bullet_speed
        self.speedx = self.bullet_speed * dx
        self.speedy = self.bullet_speed * dy
        self.pierce = pierce

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Kill the bullet if it goes off the screen
        if self.rect.bottom < 0 or self.rect.top > HEIGHT\
            or self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

# Define the pickup class
class Pickup(pygame.sprite.Sprite):
    def __init__(self, x, y, pickupradius):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center = (x, y))
        self.collision_box = pygame.Rect(x-(pickupradius // 2),
                                         y-(pickupradius // 2),
                                         pickupradius, pickupradius)
