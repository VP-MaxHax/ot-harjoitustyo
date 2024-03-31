import pygame
from entities import Player, Vampire, Bullet, Pickup
from upgrades import Upgrades
import sys
import math

# All of gameloop is done with help of Chat-GPT

def run():
    # Initialize Pygame
    pygame.init()

    # Set up the screen
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Vampire Survivor")

    # Define colors
    WHITE = (255, 255, 255)

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    vampires = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    pickups = pygame.sprite.Group()
    players = pygame.sprite.Group()

    # Create player
    player = Player()
    upgrade = Upgrades(player)
    all_sprites.add(player)
    players.add(player)

    # Timer for vampire spawning
    SPAWN_VAMPIRE_EVENT = pygame.USEREVENT + 1
    spawn_interval = 3000  # initial spawn interval in milliseconds
    pygame.time.set_timer(SPAWN_VAMPIRE_EVENT, spawn_interval)

    def draw():
        screen.fill(WHITE)
        all_sprites.draw(screen)
        screen.blit(score, (300, 0))
        screen.blit(lvlup, (50, 0))
        pygame.display.flip()
        pygame.time.Clock().tick(30)

    def draw_levelup():
        waiting_for_key = True
        choices = upgrade.pick_options()
        choice1 = upgrade_choices(choices[0])
        choice2 = upgrade_choices(choices[1])
        choice3 = upgrade_choices(choices[2])
        slot1 = font.render(f"Press 1", True, (255, 0, 0))
        slot2 = font.render(f"Press 2", True, (255, 0, 0))
        slot3 = font.render(f"Press 3", True, (255, 0, 0))
        upgrade_text = font.render(f"Upgrade", True, (255, 0, 0))
        while waiting_for_key:
            screen.fill(WHITE)
            all_sprites.draw(screen)
            screen.blit(score, (300, 0))
            screen.blit(lvlup, (50, 0))
            pygame.draw.rect(screen, (0, 0, 0), (50, 150, 200, 350))
            screen.blit(upgrade_text, (70, 150))
            screen.blit(choice1, (85, 250))
            screen.blit(slot1, (75, 400))
            pygame.draw.rect(screen, (0, 0, 0), (300, 150, 200, 350))
            screen.blit(upgrade_text, (320, 150))
            screen.blit(choice2, (335, 250))
            screen.blit(slot2, (325, 400))
            pygame.draw.rect(screen, (0, 0, 0), (550, 150, 200, 350))
            screen.blit(upgrade_text, (570, 150))
            screen.blit(choice3, (585, 250))
            screen.blit(slot3, (575, 400))
            pygame.display.flip()
            pygame.time.Clock().tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        print("1")
                        upgrade.chosen_upgrade(choices[0])
                        waiting_for_key = False
                    elif event.key == pygame.K_2:
                        print("2")
                        upgrade.chosen_upgrade(choices[1])
                        waiting_for_key = False
                    elif event.key == pygame.K_3:
                        print("3")
                        upgrade.chosen_upgrade(choices[2])
                        waiting_for_key = False

    def upgrade_choices(choice):
        font = pygame.font.SysFont("Arial", 24)
        match choice:
            case 1:
                return font.render(f"Firerate", True, (255, 0, 0))
            
            case 2:
                return font.render(f"Mov speed", True, (255, 0, 0))

            case 3:
                return font.render(f"Blt speed", True, (255, 0, 0))

            case 4:
                return font.render(f"Pickup range", True, (255, 0, 0))

            case 5:
                return font.render(f"Xp rate", True, (255, 0, 0))

            case 6:
                return font.render(f"Blt pierce", True, (255, 0, 0))

            case 7:
                return font.render(f"Blt size", True, (255, 0, 0))

    def find_closest_vampire():
        closest_distance = float('inf')
        closest_vampire = None
        for vampire in vampires:
            distance = math.sqrt((vampire.rect.centerx - player.rect.centerx) ** 2 +
                                (vampire.rect.centery - player.rect.centery) ** 2)
            if distance < closest_distance:
                closest_distance = distance
                closest_vampire = vampire
        return closest_vampire

    # Main game loop
    running = True
    levelup = False
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPAWN_VAMPIRE_EVENT:
                vampire = Vampire(player)
                all_sprites.add(vampire)
                vampires.add(vampire)
                spawn_interval = max(int(2000-(math.sqrt(pygame.time.get_ticks())*5))//1, 5)
                pygame.time.set_timer(SPAWN_VAMPIRE_EVENT, spawn_interval)

        # Update sprites
        all_sprites.update()
        vamp = find_closest_vampire()
        bullet, shot = player.shoot(vamp)
        if shot:
            all_sprites.add(bullet)
            bullets.add(bullet)
            shot = False

        # Check for collisions between player and vampires
        hits = pygame.sprite.spritecollide(player, vampires, False)
        if hits:
            running = False
        
        # Check for collisions between bullet and vampires
        hits_bullet = pygame.sprite.groupcollide(bullets, vampires, False, False)
        hits_vampire = pygame.sprite.groupcollide(vampires, bullets, True, False)
        for vampire_hit in hits_vampire:
            vampires.remove(vampire_hit)
            all_sprites.remove(vampire_hit)
            if spawn_interval > 10:
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

        if player.score >= player.nxt_lvl:
            player.pts_for_lvlup += 1
            player.nxt_lvl = player.score + player.pts_for_lvlup
            levelup = True

        if levelup == True:
            draw_levelup()
            levelup = False
        else:
            draw()

    # Quit Pygame
    pygame.quit()
    sys.exit()