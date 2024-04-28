import sys
import math
import pygame
from entities import Player, Vampire, Pickup
from upgrades import Upgrades
from meta_upgrades import Meta

# All of gameloop is done with help of Chat-GPT


class Game:
    """Class that runs the game logic
    """
    def __init__(self, player_profile, screen):
        """Class constructor, handles shared data ove logic

        Args:
            player_profile (str): player profile name
            screen (pygame.display.set_mode): pygame screen spesifications
        """
        # Initialize Pygame
        pygame.init()
        # Set up the screen
        self.width, self.height = 800, 600
        self.screen = screen
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
        self.spawn_vampire_event, self.spawn_interval = self.setup_vampire_spawn()
        pygame.time.set_timer(self.spawn_vampire_event, self.spawn_interval)
        self.ticks = 0
        self.score = None
        self.lvlup = None

    def setup_vampire_spawn(self):
        """Prepares vampire spawn timer

        Returns:
            tuple: (pygame event to spawn a vampire, base interval for that event)
        """
        self.spawn_vampire_event = pygame.USEREVENT + 1
        self.spawn_interval = 3000  # initial spawn interval in milliseconds
        return self.spawn_vampire_event, self.spawn_interval

    def draw(self):
        """Called on to draw the screen and objects on main gameplay loop
        """
        self.screen.fill(self.white)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.score, (300, 0))
        self.screen.blit(self.lvlup, (50, 0))
        pygame.display.flip()
        pygame.time.Clock().tick(30)

    def draw_levelup(self):
        """Called on levelup event to show upgrade choices
        """
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
        """Used to check choice of upgrade, also quits game if quit event is called

        Args:
            choices (list): list of three choices for an upgrade
            test (bool, optional): Used on testing to activate test functionality. 
            Defaults to False.
            
            keypress (pygame.event, optional): used on testing to simulate events. 
            Defaults to None.

        Returns:
            _type_: _description_
        """
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
        """Used to draw levelup choices

        Args:
            choice1 (pygame text object): text object to reflect one of the upgrade choices
            choice2 (pygame text object): text object to reflect one of the upgrade choices
            choice3 (pygame text object): text object to reflect one of the upgrade choices
        """
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
        """Used on levelup event to draw correct upgrade choices

        Args:
            choice (int): integer reflecting an upgrade choice

        Returns:
            pygame text object: text object to reflect an upgrade choice
        """
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
        """Finds the vampire that is closest to the player and return it

        Returns:
            Vampire(): vampire class object
        """
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
        """Main logic of the gameplay loop
        """
        running = True
        levelup = False
        while running:
            self.ticks += 1
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
        """Checks if there is any event happening on this tick

        Returns:
            bool: returns is the game ment to be still running
        """
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == self.spawn_vampire_event:
                self.spawn_vampire()
        return running

    # Spawn vampire
    def spawn_vampire(self):
        """Called on to spawn a vampire on vampire_spawn_event
        """
        vampire = Vampire(self.player)
        self.all_sprites.add(vampire)
        self.vampires.add(vampire)
        self.spawn_interval = max(
            int(2000-(self.ticks//3)), 5)
        pygame.time.set_timer(self.spawn_vampire_event, self.spawn_interval)

    def winner(self):
        """Called on if player got to endgame and won the game. Calls meta upgrade logic.
        """
        choice = self.draw_metaupgrade_choices()
        self.meta.update_data(choice)


    def draw_metaupgrade_choices(self):
        """Draws metaupgrade screen and waits for players pick for upgrade

        Returns:
            int: integer reflecting players choice of upgrade
        """
        choice = None
        while choice is None:
            self.screen.fill(self.white)
            self.all_sprites.draw(self.screen)
            font = pygame.font.SysFont("Arial", 40)
            self.screen.blit(font.render("Congratulations!", True, (0, 0, 0)), (300, 100))
            font = pygame.font.SysFont("Arial", 24)
            self.screen.blit(font.render(\
            "You got to the endgame and now you can choose a meta upgrade and return to menu.",
                                        True, (0, 0, 0)), (50, 200))
            self.screen.blit(font.render("Maximum level of meta uprages is 9",
                                        True, (0, 00, 0)), (200, 300))
            self.draw_meta_upgrades()
            choice = self.check_meta_event()
            pygame.display.flip()
            pygame.time.Clock().tick(30)
        return choice

    def draw_meta_upgrades(self):
        """Draws the meta upgrade boxes and text into them
        """
        x_pos = 25
        metadata = self.meta.meta_status
        upgrade_choices = ["Firerate", "M Speed", "Blt Speed",\
                            "Pickup Rng", "Exp Rate", "Blt Pierce", "Blt Size"]
        font = pygame.font.SysFont("Arial", 18)
        for i in range(7):
            pygame.draw.rect(self.screen, (0, 0, 0), (x_pos, 400, 105, 180))
            self.screen.blit(font.render(f"Press {i+1}",
                                          True, (255, 255, 0)), (x_pos+5, 410))
            self.screen.blit(font.render("Upgrade:",
                                          True, (255, 255, 0)), (x_pos+5, 430))
            self.screen.blit(font.render(f"{upgrade_choices[i]}",
                                          True, (255, 255, 0)), (x_pos+5, 460))
            self.screen.blit(font.render("Current lvl:",
                                          True, (255, 255, 0)), (x_pos+5, 490))
            self.screen.blit(font.render(f"{metadata[i]}",
                                          True, (255, 255, 0)), (x_pos+5, 520))
            x_pos += 110

    def check_meta_event(self):
        """Handles players meta upgrade pick in form of keypress

        Returns:
            int: integer reflecting players choice of upgrade
        """
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
        """Game over event if player dies before endgame

        Args:
            test (bool, optional): used on testing to activate test functionality. 
            Defaults to False.

        Returns:
            str: used in testing to return a value
        """
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
        """Check keypresses and quit events in gameover state

        Args:
            event (pygame.event): pygame game event
            test (bool, optional): used on testing to activate test functionality. 
            Defaults to False.

        Returns:
            _type_: _description_
        """
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
        """Updates all sprites on the screen. 
        Also checks if its time to shoot and does so if it is."""
        self.all_sprites.update()
        vamp = self.find_closest_vampire()
        bullet, shot = self.player.shoot(vamp)
        if shot:
            self.all_sprites.add(bullet)
            self.bullets.add(bullet)

    # Check collisions
    def check_collisions(self):
        """Checks sprite collisions. Collisions include:
        player-vampire, bullet-vampire, player-pickup

        Returns:
            bool: if collition between player-vampire signal False to game still runnign.
        """
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
        """Handles details of player-pickup collision
        """
        for sprite in self.pickups:
            if sprite.collision_box.colliderect(self.player.rect):
                self.player.stats.score += self.player.stats.exprate
                sprite.kill()  # Remove collided sprite from group

    # Handle bullet hit
    def handle_bullet_hit(self, bullet):
        """Checks if bullet has still pierce charges left. Removes bullet if not.

        Args:
            bullet (Bullet()): bullet class object
        """
        bullet.pierce -= 1
        if bullet.pierce == 0:
            bullet.kill()

    # Handle vampire hit
    def handle_vampire_hit(self, vampire_hit):
        """Handles removing vampire when hit by bullet. Also spawn pickup on same spot

        Args:
            vampire_hit (Vampire()): vampire class object
        """
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
        """Updates score (exp) on top of screen
        """
        font = pygame.font.SysFont("Arial", 40)
        self.score = font.render(
            f"Score {self.player.stats.score:07}", True, (255, 0, 0))
        self.lvlup = font.render(
            f"Next level {self.player.stats.nxt_lvl}", True, (255, 0, 0))

    # Handle level up
    def handle_levelup(self, levelup):
        """Levelup event trigger and main logic.

        Args:
            levelup (bool): determines has levelup happened
        """
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
