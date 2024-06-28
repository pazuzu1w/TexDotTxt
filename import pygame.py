import pygame
import sys
import random

# --- Constants ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
MENU_OPTION_HEIGHT = 50
MUSIC_VOLUME_INCREMENT = 0.1
MAX_BULLET_HOLES = 10  # Maximum number of bullet holes per view

# --- Weapon and Ammo Types ---
WEAPONS = {
    "Colt Single Action Army": {
        "ammo_type": ".45 Colt",
        "damage": 50,
        "accuracy": 0.8,
        "range": 100
    },
    "Winchester Model 1873": {
        "ammo_type": ".44-40 Winchester",
        "damage": 60,
        "accuracy": 0.9,
        "range": 200
    },
    "Remington Model 1875": {
        "ammo_type": ".44 Remington",
        "damage": 55,
        "accuracy": 0.85,
        "range": 120
    },
    "Derringer": {
        "ammo_type": ".41 Rimfire",
        "damage": 30,
        "accuracy": 0.6,
        "range": 50
    },
    "Sharps Rifle": {
        "ammo_type": ".50-70 Government",
        "damage": 80,
        "accuracy": 0.95,
        "range": 300
    }
}

AMMO_TYPES = {
    ".45 Colt": {"penetration": 2},
    ".44-40 Winchester": {"penetration": 3},
    ".44 Remington": {"penetration": 2},
    ".41 Rimfire": {"penetration": 1},
    ".50-70 Government": {"penetration": 4}
}

# --- Classes ---
def initialize_shootable_objects(self):
    # Example shootable objects for each view
    return [
        [ShootableObject(100, 200, 50, 50, "bottle", False),
         ShootableObject(300, 400, 100, 100, "window", True)],
        [ShootableObject(200, 300, 75, 75, "picture", False)],
        [ShootableObject(400, 200, 60, 60, "lamp", False)],
        [ShootableObject(150, 350, 80, 80, "mirror", True)]
    ]


class ShootableObject:
    def __init__(self, x, y, width, height, object_type, durability):
        self.rect = pygame.Rect(x, y, width, height)
        self.object_type = object_type
        self.durability = durability
        self.destroyed = False

    def hit(self, damage, penetration):
        self.durability -= damage * (penetration / 2)
        if self.durability <= 0:
            self.destroyed = True
            return True
        return False

class Gun:
    def __init__(self, gun_type):
        self.gun_type = gun_type
        self.ammo_type = WEAPONS[gun_type]["ammo_type"]
        self.damage = WEAPONS[gun_type]["damage"]
        self.accuracy = WEAPONS[gun_type]["accuracy"]
        self.range = WEAPONS[gun_type]["range"]


class ShootableObject:
    def __init__(self, x, y, width, height, object_type, bulletproof):
        self.rect = pygame.Rect(x, y, width, height)
        self.object_type = object_type
        self.bulletproof = bulletproof
        self.destroyed = False

    def hit(self, ammo_type):
        if not self.bulletproof or ammo_type == "armor_piercing":
            self.destroyed = True
            return True
        return False

class Player:
    def __init__(self):
        self.weapon_drawn = False
        self.hand_cursor = pygame.image.load('hand_cursor.png')
        self.crosshair_cursor = pygame.image.load('crosshair_cursor.png')
        self.current_gun = Gun("Colt Single Action Army")  # Default gun
        self.ammo = {ammo_type: 20 for ammo_type in AMMO_TYPES}  # Start with 20 rounds of each type

    def toggle_weapon(self):
        self.weapon_drawn = not self.weapon_drawn

    def get_cursor(self):
        return self.crosshair_cursor if self.weapon_drawn else self.hand_cursor

    def change_gun(self, gun_type):
        if gun_type in WEAPONS:
            self.current_gun = Gun(gun_type)

    def shoot(self):
        if self.ammo[self.current_gun.ammo_type] > 0:
            self.ammo[self.current_gun.ammo_type] -= 1
            return True
        return False

class Saloon:
    def __init__(self):
        self.views = [
            pygame.image.load('saloon_001.jpg'),
            pygame.image.load('saloon_001_right.jpg'),
            pygame.image.load('saloon_001_around.jpg'),
            pygame.image.load('saloon_001_left.jpg')
        ]
        self.current_view_index = 0
        self.bullet_holes = [[] for _ in range(len(self.views))]
        self.shootable_objects = self.initialize_shootable_objects()



    def add_bullet_hole(self, pos):
        if len(self.bullet_holes[self.current_view_index]) < MAX_BULLET_HOLES:
            self.bullet_holes[self.current_view_index].append(pos)



    def initialize_shootable_objects(self):
        # Example shootable objects for each view
        return [
            [ShootableObject(100, 200, 50, 50, "bottle", False),
             ShootableObject(300, 400, 100, 100, "window", True)],
            [ShootableObject(200, 300, 75, 75, "picture", False)],
            [ShootableObject(400, 200, 60, 60, "lamp", False)],
            [ShootableObject(150, 350, 80, 80, "mirror", True)]
        ]

    def get_current_view(self):
        return self.views[self.current_view_index]

    def get_current_shootable_objects(self):
        return self.shootable_objects[self.current_view_index]

    def change_view(self, direction):
        if direction == "left":
            self.current_view_index = (self.current_view_index - 1) % len(self.views)
        elif direction == "right":
            self.current_view_index = (self.current_view_index + 1) % len(self.views)
class MusicPlayer:
    def __init__(self, music_file):
        pygame.mixer.init()
        self.music = pygame.mixer.music.load(music_file)
        self.volume = 0.5
        pygame.mixer.music.set_volume(self.volume)
        self.is_playing = False

    def play(self):
        if not self.is_playing:
            pygame.mixer.music.play(-1)  # Loop indefinitely
            self.is_playing = True

    def stop(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False

    def toggle(self):
        if self.is_playing:
            self.stop()
        else:
            self.play()

    def volume_up(self):
        self.volume = min(self.volume + MUSIC_VOLUME_INCREMENT, 1.0)
        pygame.mixer.music.set_volume(self.volume)

    def volume_down(self):
        self.volume = max(self.volume - MUSIC_VOLUME_INCREMENT, 0.0)
        pygame.mixer.music.set_volume(self.volume)


class Menu:
    def __init__(self, screen, font, options):
        self.screen = screen
        self.font = font
        self.options = options
        self.selected_option = 0
        self.y_offset = 300
        self.background = pygame.image.load('pause_sign.jpg')

    def draw(self, music_player):
        x = (SCREEN_WIDTH - current_view.get_width()) // 2
        y = (SCREEN_HEIGHT - current_view.get_height()) // 2
        self.screen.blit(self.background, (x, y))

        for i, option in enumerate(self.options):
            color = (230, 0, 0) if i == self.selected_option else (0, 0, 0)
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, self.y_offset + i * MENU_OPTION_HEIGHT))
            self.screen.blit(text_surface, text_rect)

        # Music Status Display
        music_status = "ON" if music_player.is_playing else "OFF"
        music_status_color = (0, 0, 0) if music_player.is_playing else (255, 0, 0)
        music_status_surface = self.font.render(f"Music: {music_status}", True, music_status_color)
        self.screen.blit(music_status_surface,
                         (SCREEN_WIDTH // 2 - 100, self.y_offset + len(self.options) * MENU_OPTION_HEIGHT + 50))

        # Volume Display
        volume_surface = self.font.render(f"Volume: {int(music_player.volume * 100)}%", True, (0, 0, 0))
        self.screen.blit(volume_surface,
                         (SCREEN_WIDTH // 2 - 100, self.y_offset + len(self.options) * MENU_OPTION_HEIGHT + 100))

    def handle_input(self, event, music_player):
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0:  # Resume
                        return False  # Indicate to close the menu
                    elif self.selected_option == 1:  # Quit
                        return "quit"  # Indicate to quit the game
                    elif self.selected_option == 2:  # Music: ON/OFF
                        music_player.toggle()
                    elif self.selected_option == 3:  # Volume Up
                        music_player.volume_up()
                    elif self.selected_option == 4:  # Volume Down
                        music_player.volume_down()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for i, option in enumerate(self.options):
                text_surface = self.font.render(option, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, self.y_offset + i * MENU_OPTION_HEIGHT))
                if text_rect.collidepoint(mouse_x, mouse_y):
                    self.selected_option = i
                    if self.selected_option == 0:  # Resume
                        return False
                    elif self.selected_option == 1:  # Quit
                        return "quit"
                    elif self.selected_option == 2:  # Music: ON/OFF
                        music_player.toggle()
                    elif self.selected_option == 3:  # Volume Up
                        music_player.volume_up()
                    elif self.selected_option == 4:  # Volume Down
                        music_player.volume_down()
        return True



class ShootingEffects:
    def __init__(self):
        pass
        self.bullet_hole = pygame.image.load('bullet_hole.png')
        self.ricochet_sound = pygame.mixer.Sound('ricochet.mp3')
        self.gunshot_sound = pygame.mixer.Sound('gunshot.mp3')
        self.break_sound = pygame.mixer.Sound('breaking_sound.mp3')

    def create_bullet_hole(self, screen, pos):
        screen.blit(self.bullet_hole, pos)

    def play_ricochet(self):
        self.ricochet_sound.play()

    def play_gunshot(self):
        self.gunshot_sound.play()

    def play_break(self):
        self.break_sound.play()


class Player:
    def __init__(self):
        self.weapon_drawn = False
        self.hand_cursor = pygame.image.load('hand_cursor.png')
        self.crosshair_cursor = pygame.image.load('crosshair_cursor.png')

    def toggle_weapon(self):
        self.weapon_drawn = not self.weapon_drawn

    def get_cursor(self):
        return self.crosshair_cursor if self.weapon_drawn else self.hand_cursor

#setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("TexDotText: Saloon Spin Cycle")
clock = pygame.time.Clock()
font = pygame.font.Font('Quentincaps-owxKz.ttf', 36)

saloon = Saloon()
music_player = MusicPlayer('saloon_music001.mp3')
menu = Menu(screen, font, ["Resume", "Quit", "Music: ON/OFF", "Volume Up", "Volume Down"])
player = Player()
shooting_effects = ShootingEffects()
music_player.play()

show_menu = False
pygame.mouse.set_visible(False)  # Hide the default cursor

# --- Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                show_menu = not show_menu
            elif not show_menu:
                if event.key == pygame.K_LEFT:
                    saloon.change_view("left")
                elif event.key == pygame.K_RIGHT:
                    saloon.change_view("right")
                elif event.key == pygame.K_SPACE:
                    player.toggle_weapon()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            if player.weapon_drawn and not show_menu:
                shooting_effects.play_gunshot()
                mouse_pos = pygame.mouse.get_pos()
                hit_object = None

                for obj in saloon.get_current_shootable_objects():
                    if obj.rect.collidepoint(mouse_pos):
                        hit_object = obj
                        break

                if hit_object:
                    if hit_object.hit(player.current_gun.ammo_type):
                        shooting_effects.play_break()
                    else:
                        shooting_effects.play_ricochet()
                else:
                    if random.random() < 0.3:  # 30% chance of ricochet for non-object hits
                        shooting_effects.play_ricochet()
                    saloon.add_bullet_hole(mouse_pos)

        if show_menu:
            result = menu.handle_input(event, music_player)
            if result == "quit":
                running = False
            show_menu = result if result is not None else show_menu

    # --- Rendering ---
    screen.fill((0, 0, 0))  # Clear the screen

    if show_menu:
        menu.draw(music_player)
    else:
        current_view = saloon.get_current_view()
        x = (SCREEN_WIDTH - current_view.get_width()) // 2
        y = (SCREEN_HEIGHT - current_view.get_height()) // 2
        screen.blit(current_view, (x, y))

        # Draw bullet holes
        for hole_pos in saloon.bullet_holes[saloon.current_view_index]:
            shooting_effects.create_bullet_hole(screen, hole_pos)

        # Draw shootable objects (placeholder rectangles)
        for obj in saloon.get_current_shootable_objects():
            if not obj.destroyed:
                pygame.draw.rect(screen, (255, 0, 0), obj.rect, 2)  # Red rectangle outline

    # Draw custom cursor
    cursor = player.get_cursor()
    cursor_pos = pygame.mouse.get_pos()
    screen.blit(cursor, cursor_pos)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()