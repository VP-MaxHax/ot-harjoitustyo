import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vampire Survivor")

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
        self.pierce = 2
        self.bullet_size = 100


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

    def shoot(self):
        # Shoot towards the closest vampire
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            closest_vampire = self.find_closest_vampire()
            if closest_vampire:
                dx = closest_vampire.rect.centerx - self.rect.centerx
                dy = closest_vampire.rect.centery - self.rect.centery
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance != 0:
                    bullet = Bullet(self.rect.centerx, self.rect.centery, dx / distance, dy / distance, player.bullet_speed, player.bullet_size)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

    def find_closest_vampire(self):
        closest_distance = float('inf')
        closest_vampire = None
        for vampire in vampires:
            distance = math.sqrt((vampire.rect.centerx - self.rect.centerx) ** 2 +
                                 (vampire.rect.centery - self.rect.centery) ** 2)
            if distance < closest_distance:
                closest_distance = distance
                closest_vampire = vampire
        return closest_vampire

# Define upgrades    
class Upgrades:
    def __init__(self):
        self.upg = []

    def firerate_upg(self):
        player.shoot_delay = int(player.shoot_delay*0.9)

    def speed_upg(self):
        player.mv_speed += 1

    def bult_spd_upg(self):
        player.bullet_speed += 1

    def pickup_upg(self):
        player.pickupradius += 50
        player.pickuparea = pygame.Surface((player.pickupradius, player.pickupradius))

    def exprate_upg(self):
        player.exprate += 1

    def blt_prs_upg(self):
        player.pierce += 1

    def blt_sz_upg(self):
        player.bullet_size += 2
    

# Define the vampire class
class Vampire(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.player = player
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
        #print(self.player.rect.centerx, self.player.rect.centery)
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        # Normalize the movement vector
        if distance != 0:
            dx /= distance
            dy /= distance

        
        # Set the speed of the vampire
        speed = 1  # Adjust this value as needed
        
        # Move the vampire towards the player
        print(dx, dy)
        self.rect.x += dx * speed
        self.rect.y += dy * speed
        #print(self.rect.x, self.rect.y)

# Define the bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, bullet_speed, bullet_size):
        super().__init__()
        self.image = pygame.Surface((bullet_size, bullet_size))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.bullet_speed = bullet_speed
        self.speedx = self.bullet_speed * dx
        self.speedy = self.bullet_speed * dy
        self.pierce = player.pierce

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Kill the bullet if it goes off the screen
        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
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

    # Draw
def draw():
    screen.fill(WHITE)
    all_sprites.draw(screen)
    screen.blit(score, (300, 0))
    screen.blit(lvlup, (50, 0))
    # Levelup choices
    if levelup == True:
        pygame.draw.rect(screen, (0, 0, 0), (50, 150, 200, 350)) 
        pygame.draw.rect(screen, (0, 0, 0), (300, 150, 200, 350)) 
        pygame.draw.rect(screen, (0, 0, 0), (550, 150, 200, 350)) 
    pygame.display.flip()
    # Cap the frame rate
    pygame.time.Clock().tick(30)

# Create sprite groups
all_sprites = pygame.sprite.Group()
vampires = pygame.sprite.Group()
bullets = pygame.sprite.Group()
pickups = pygame.sprite.Group()
players = pygame.sprite.Group()

# Create player
player = Player()
upgrade = Upgrades()
all_sprites.add(player)
players.add(player)

# Timer for vampire spawning
SPAWN_VAMPIRE_EVENT = pygame.USEREVENT + 1
spawn_interval = 3000  # initial spawn interval in milliseconds
pygame.time.set_timer(SPAWN_VAMPIRE_EVENT, spawn_interval)

# Main game loop
running = True
levelup = False
while running:
    #print((2000-(math.sqrt(pygame.time.get_ticks())*5))//1)
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_VAMPIRE_EVENT:
            vampire = Vampire(player)
            all_sprites.add(vampire)
            vampires.add(vampire)
            #spawn_interval = int(2000-(math.sqrt(pygame.time.get_ticks())*5))//1
            spawn_interval = 999999
            pygame.time.set_timer(SPAWN_VAMPIRE_EVENT, spawn_interval)

    # Update
    all_sprites.update()
    player.shoot()

    # Check for collisions between player and vampires
    hits = pygame.sprite.spritecollide(player, vampires, False)
    if hits:
        running = False
    
    # Check for collisions between player and vampires
    hits_bullet = pygame.sprite.groupcollide(bullets, vampires, False, False)
    hits_vampire = pygame.sprite.groupcollide(vampires, bullets, True, False)
    #print(hits_vampire)
    #print(hits_bullet)
    for vampire_hit in hits_vampire:
        vampires.remove(vampire_hit)
        all_sprites.remove(vampire_hit)
        # Spawn pickup where vampire died
        pickup = Pickup(vampire_hit.rect.centerx, vampire_hit.rect.centery, player.pickupradius)
        all_sprites.add(pickup)
        pickups.add(pickup)
    for bullet in hits_bullet:
        bullet.pierce -= 1
        if bullet.pierce == 0:
            bullet.kill()

    

    # Check collisions between player and pickup
    for sprite in pickups:
        if sprite.collision_box.colliderect(player.rect):
            player.score += player.exprate
            sprite.kill()  # Remove collided sprite from group

    #Init score display
    font = pygame.font.SysFont("Arial", 40)
    score = font.render(f"Score {player.score:07}", True, (255, 0, 0))
    lvlup = font.render(f"Next level {player.nxt_lvl}", True, (255, 0, 0))

    if player.score == player.nxt_lvl:
        player.pts_for_lvlup += 1
        player.nxt_lvl = player.score + player.pts_for_lvlup
        levelup = True

    draw()

    if levelup == True:
        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        print("1")
                        upgrade.firerate_upg()
                        print(player.shoot_delay)
                        waiting_for_key = False
                    elif event.key == pygame.K_2:
                        print("2")
                        waiting_for_key = False
                    elif event.key == pygame.K_3:
                        print("3")
                        waiting_for_key = False
            draw()
        levelup = False

# Quit Pygame
pygame.quit()
sys.exit()
