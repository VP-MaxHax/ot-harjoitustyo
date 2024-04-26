import sys
import math
import pygame
from entities import Player, Vampire, Pickup
from upgrades import Upgrades
from meta_upgrades import Meta

# All of gameloop is done with help of Chat-GPT


class Game:
    def __init__(self, player_profile, screen):
        # Initialize Pygame
        pygame.init()
        # Set up the screen
        self.width, self.height = 800, 600
        self.screen = screen
        pygame.display.set_caption("Vampire Survivor")
        # Define colors
        self.white = (255, 255, 255)
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.vampires = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.pickups = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        # Create player
        self.player = Player()
        self.upgrade = Upgrades(self.player)
        self.all_sprites.add(self.player)
        self.players.add(self.player)
        self.meta = Meta(self.upgrade, player_profile)
        self.meta.apply_meta_upgrades()
        # Timer for vampire spawning
        self.spawn_vampire_event = pygame.USEREVENT + 1
        self.spawn_interval = 3000  # initial spawn interval in milliseconds
        pygame.time.set_timer(self.spawn_vampire_event, self.spawn_interval)
        self.score = None
        self.lvlup = None

    def draw(self):
        self.screen.fill(self.white)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.score, (300, 0))
        self.screen.blit(self.lvlup, (50, 0))
        pygame.display.flip()
        pygame.time.Clock().tick(30)

    def draw_levelup(self):
        waiting_for_key = True
        choices = self.upgrade.pick_options()
        choice1 = self.upgrade_choices(choices[0])
        choice2 = self.upgrade_choices(choices[1])
        choice3 = self.upgrade_choices(choices[2])
        while waiting_for_key:
            self.screen.fill(self.white)
            self.all_sprites.draw(self.screen)
            pygame.draw.rect(self.screen, (0, 0, 0), (50, 150, 200, 350))
            pygame.draw.rect(self.screen, (0, 0, 0), (300, 150, 200, 350))
            pygame.draw.rect(self.screen, (0, 0, 0), (550, 150, 200, 350))
            self.draw_levelup_choices(choice1, choice2, choice3)
            pygame.display.flip()
            pygame.time.Clock().tick(30)
            waiting_for_key = self.level_up_check_event(choices)

    def level_up_check_event(self, choices, test=False, keypress=None):
        waiting_for_key = True
        if test is True:
            pygame.event.post(keypress)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                if test is True:
                    return "Returned only in testing"
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.upgrade.chosen_upgrade(choices[0])
                    waiting_for_key = False
                elif event.key == pygame.K_2:
                    self.upgrade.chosen_upgrade(choices[1])
                    waiting_for_key = False
                elif event.key == pygame.K_3:
                    self.upgrade.chosen_upgrade(choices[2])
                    waiting_for_key = False
        return waiting_for_key

    def draw_levelup_choices(self, choice1, choice2, choice3):
        font = pygame.font.SysFont("Arial", 40)
        slot1 = font.render("Press 1", True, (255, 0, 0))
        slot2 = font.render("Press 2", True, (255, 0, 0))
        slot3 = font.render("Press 3", True, (255, 0, 0))
        upgrade_text = font.render("Upgrade", True, (255, 0, 0))
        self.screen.blit(self.score, (300, 0))
        self.screen.blit(self.lvlup, (50, 0))
        self.screen.blit(upgrade_text, (70, 150))
        self.screen.blit(choice1, (85, 250))
        self.screen.blit(slot1, (75, 400))
        self.screen.blit(upgrade_text, (320, 150))
        self.screen.blit(choice2, (335, 250))
        self.screen.blit(slot2, (325, 400))
        self.screen.blit(upgrade_text, (570, 150))
        self.screen.blit(choice3, (585, 250))
        self.screen.blit(slot3, (575, 400))

    def upgrade_choices(self, choice):
        font = pygame.font.SysFont("Arial", 24)
        match choice:
            case 1:
                upgrade = font.render("Firerate", True, (255, 0, 0))
            case 2:
                upgrade = font.render("Mov speed", True, (255, 0, 0))
            case 3:
                upgrade = font.render("Blt speed", True, (255, 0, 0))
            case 4:
                upgrade = font.render("Pickup range", True, (255, 0, 0))
            case 5:
                upgrade = font.render("Xp rate", True, (255, 0, 0))
            case 6:
                upgrade = font.render("Blt pierce", True, (255, 0, 0))
            case 7:
                upgrade = font.render("Blt size", True, (255, 0, 0))
        return upgrade

    def find_closest_vampire(self):
        closest_distance = float('inf')
        closest_vampire = None
        for vampire in self.vampires:
            distance = math.sqrt((vampire.rect.centerx - self.player.rect.centerx) ** 2 +
                                 (vampire.rect.centery - self.player.rect.centery) ** 2)
            if distance < closest_distance:
                closest_distance = distance
                closest_vampire = vampire
        return closest_vampire

    # Main game loop
    def run(self):
        running = True
        levelup = False
        while running:
            if not self.handle_events():
                break
            self.update_sprites()
            if not self.check_collisions():
                pygame.time.set_timer(self.spawn_vampire_event, 0)
                if self.spawn_interval <= 10:
                    self.winner()
                else:
                    self.gameover()
                return
            self.update_score_display()
            self.handle_levelup(levelup)
        pygame.quit()
        sys.exit()

    # Handle events
    def handle_events(self):
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == self.spawn_vampire_event:
                self.spawn_vampire()
        return running

    # Spawn vampire
    def spawn_vampire(self):
        vampire = Vampire(self.player)
        self.all_sprites.add(vampire)
        self.vampires.add(vampire)
        self.spawn_interval = max(
            int(2000-(math.sqrt(pygame.time.get_ticks())*5))//1, 5)
        pygame.time.set_timer(self.spawn_vampire_event, self.spawn_interval)

    def winner(self):
        choice = self.draw_metaupgrade_choices()
        self.meta.update_data(choice)


    def draw_metaupgrade_choices(self):
        choice = None
        metadata = self.meta.meta_status
        while choice is None:
            self.screen.fill(self.white)
            self.all_sprites.draw(self.screen)
            font = pygame.font.SysFont("Arial", 40)
            self.screen.blit(font.render("Congratulations!", True, (0, 0, 0)), (300, 100))
            font = pygame.font.SysFont("Arial", 24)
            self.screen.blit(font.render("You got to the endgame and now you can choose a meta upgrade and return to menu.",
                                        True, (0, 0, 0)), (50, 200))
            self.screen.blit(font.render("Maximum level of meta uprages is 9",
                                        True, (0, 00, 0)), (200, 300))
            pygame.draw.rect(self.screen, (0, 0, 0), (25, 400, 105, 180))
            pygame.draw.rect(self.screen, (0, 0, 0), (135, 400, 105, 180))
            pygame.draw.rect(self.screen, (0, 0, 0), (245, 400, 105, 180))
            pygame.draw.rect(self.screen, (0, 0, 0), (355, 400, 105, 180))
            pygame.draw.rect(self.screen, (0, 0, 0), (465, 400, 105, 180))
            pygame.draw.rect(self.screen, (0, 0, 0), (575, 400, 105, 180))
            pygame.draw.rect(self.screen, (0, 0, 0), (685, 400, 105, 180))
            self.screen.blit(font.render("Press 1", True, (255, 255, 0)), (30, 410))
            self.screen.blit(font.render("Upgrade:", True, (255, 255, 0)), (30, 430))
            self.screen.blit(font.render("Firerate", True, (255, 255, 0)), (30, 460))
            self.screen.blit(font.render("Current lvl:", True, (255, 255, 0)), (30, 490))
            self.screen.blit(font.render(f"{metadata[0]}", True, (255, 255, 0)), (30, 520))
            self.screen.blit(font.render("Press 2", True, (255, 255, 0)), (140, 410))
            self.screen.blit(font.render("Upgrade:", True, (255, 255, 0)), (140, 430))
            self.screen.blit(font.render("Mv Speed", True, (255, 255, 0)), (140, 460))
            self.screen.blit(font.render("Current lvl:", True, (255, 255, 0)), (140, 490))
            self.screen.blit(font.render(f"{metadata[1]}", True, (255, 255, 0)), (140, 520))
            self.screen.blit(font.render("Press 3", True, (255, 255, 0)), (250, 410))
            self.screen.blit(font.render("Upgrade:", True, (255, 255, 0)), (250, 430))
            self.screen.blit(font.render("Blt Speed", True, (255, 255, 0)), (250, 460))
            self.screen.blit(font.render("Current lvl:", True, (255, 255, 0)), (250, 490))
            self.screen.blit(font.render(f"{metadata[2]}", True, (255, 255, 0)), (250, 520))
            self.screen.blit(font.render("Press 4", True, (255, 255, 0)), (360, 410))
            self.screen.blit(font.render("Upgrade:", True, (255, 255, 0)), (360, 430))
            self.screen.blit(font.render("Pickup Rng", True, (255, 255, 0)), (360, 460))
            self.screen.blit(font.render("Current lvl:", True, (255, 255, 0)), (360, 490))
            self.screen.blit(font.render(f"{metadata[3]}", True, (255, 255, 0)), (360, 520))
            self.screen.blit(font.render("Press 5", True, (255, 255, 0)), (470, 410))
            self.screen.blit(font.render("Upgrade:", True, (255, 255, 0)), (470, 430))
            self.screen.blit(font.render("Exp Rate", True, (255, 255, 0)), (470, 460))
            self.screen.blit(font.render("Current lvl:", True, (255, 255, 0)), (470, 490))
            self.screen.blit(font.render(f"{metadata[4]}", True, (255, 255, 0)), (470, 520))
            self.screen.blit(font.render("Press 6", True, (255, 255, 0)), (580, 410))
            self.screen.blit(font.render("Upgrade:", True, (255, 255, 0)), (580, 430))
            self.screen.blit(font.render("Blt Pierce", True, (255, 255, 0)), (580, 460))
            self.screen.blit(font.render("Current lvl:", True, (255, 255, 0)), (580, 490))
            self.screen.blit(font.render(f"{metadata[5]}", True, (255, 255, 0)), (580, 520))
            self.screen.blit(font.render("Press 7", True, (255, 255, 0)), (690, 410))
            self.screen.blit(font.render("Upgrade:", True, (255, 255, 0)), (690, 430))
            self.screen.blit(font.render("Blt Size", True, (255, 255, 0)), (690, 460))
            self.screen.blit(font.render("Current lvl:", True, (255, 255, 0)), (690, 490))
            self.screen.blit(font.render(f"{metadata[6]}", True, (255, 255, 0)), (690, 520))
            choice = self.check_meta_event()
            pygame.display.flip()
            pygame.time.Clock().tick(30)
        return choice

    def check_meta_event(self):
        choice = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    choice = 1
                elif event.key == pygame.K_2:
                    choice = 2
                elif event.key == pygame.K_3:
                    choice = 3
                elif event.key == pygame.K_4:
                    choice = 4
                elif event.key == pygame.K_5:
                    choice = 5
                elif event.key == pygame.K_6:
                    choice = 6
                elif event.key == pygame.K_7:
                    choice = 7
        return choice


    def gameover(self, test=False):
        font = pygame.font.SysFont("Arial", 40)
        self.screen.blit(font.render("You died!", True, (255, 0, 0)), (300, 100))
        self.screen.blit(font.render("Press ENTER to go back to main menu.",
                                      True, (255, 0, 0)), (100, 500))
        gameover = True
        if test is True:
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
            pygame.event.post(event)
        while gameover:
            for event in pygame.event.get():
                gameover = self.check_gameover_events(event)
            pygame.display.flip()
            pygame.time.Clock().tick(30)
        return "GameOver"

    def check_gameover_events(self, event, test=False):
        if event.type == pygame.QUIT:
            pygame.quit()
            if test is True:
                return "Returned only in testing"
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return False
        return True

    # Update sprites
    def update_sprites(self):
        self.all_sprites.update()
        vamp = self.find_closest_vampire()
        bullet, shot = self.player.shoot(vamp)
        if shot:
            self.all_sprites.add(bullet)
            self.bullets.add(bullet)

    # Check collisions
    def check_collisions(self):
        hits = pygame.sprite.spritecollide(self.player, self.vampires, False)
        if hits:
            return False
        hits_bullet = pygame.sprite.groupcollide(
            self.bullets, self.vampires, False, False)
        hits_vampire = pygame.sprite.groupcollide(
            self.vampires, self.bullets, True, False)
        for vampire_hit in hits_vampire:
            self.handle_vampire_hit(vampire_hit)
        for bullet in hits_bullet:
            self.handle_bullet_hit(bullet)
        self.handle_pickup_collisions()
        return True

    # Handle pickup collisions
    def handle_pickup_collisions(self):
        for sprite in self.pickups:
            if sprite.collision_box.colliderect(self.player.rect):
                self.player.stats.score += self.player.stats.exprate
                sprite.kill()  # Remove collided sprite from group

    # Handle bullet hit
    def handle_bullet_hit(self, bullet):
        bullet.pierce -= 1
        if bullet.pierce == 0:
            bullet.kill()

    # Handle vampire hit
    def handle_vampire_hit(self, vampire_hit):
        self.vampires.remove(vampire_hit)
        self.all_sprites.remove(vampire_hit)
        if self.spawn_interval > 10:
            # Spawn pickup where vampire died
            pickup = Pickup(vampire_hit.rect.centerx,
                            vampire_hit.rect.centery,
                            self.player.stats.pickupradius)
            self.all_sprites.add(pickup)
            self.pickups.add(pickup)

    # Update score display
    def update_score_display(self):
        font = pygame.font.SysFont("Arial", 40)
        self.score = font.render(
            f"Score {self.player.stats.score:07}", True, (255, 0, 0))
        self.lvlup = font.render(
            f"Next level {self.player.stats.nxt_lvl}", True, (255, 0, 0))

    # Handle level up
    def handle_levelup(self, levelup):
        if self.player.stats.score >= self.player.stats.nxt_lvl:
            self.player.stats.pts_for_lvlup += 1
            self.player.stats.nxt_lvl = self.player.stats.score + \
                self.player.stats.pts_for_lvlup
            levelup = True
        if levelup:
            self.draw_levelup()
            levelup = False
        else:
            self.draw()
