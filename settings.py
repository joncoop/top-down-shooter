import pygame

# Window settings
WIDTH = 960
HEIGHT = 660
TITLE = "Laser Tag!"
FPS = 60

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 150, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# Music
START_MUSIC = None
MAIN_THEME = 'assets/sounds/theme.ogg'
END_MUSIC = None

# Sound effects
LASER_SOUND = 'assets/sounds/laser.ogg'

# Fonts
TITLE_FONT = 'assets/fonts/kenvector_future.ttf'
BASE_FONT = None

# Tiles
TILES = {'wall_ul': 'assets/images/tiles/tile_398.png',
         'wall_ur': 'assets/images/tiles/tile_398.png' }

# Players
P1_IMAGES = { 'normal': 'assets/images/characters/woman_normal.png',
              'gun_out': 'assets/images/characters/woman_gun.png' }

P1_CONTROLS = { 'up': pygame.K_w,
                'down': pygame.K_s,
                'left': pygame.K_a,
                'right': pygame.K_d,
                'toggle_gun': pygame.K_q,
                'shoot': pygame.K_SPACE }

PLAYER_NORMAL_SPEED = 4
PLAYER_MAX_SPEED = 7

# Lasers
LASER_IMAGE = 'assets/images/projectiles/laser_red.png'
LASER_SPEED = 10

# Items


# Other settings
START_KEY = pygame.K_SPACE
TOGGLE_MUTE = pygame.K_m


