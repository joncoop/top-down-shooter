# Imports
import pygame
import sys
from settings import *
from sprites import *
        
# Helper functions
''' Sound utilitites '''
def play_music(track, loops=-1):
    if not mute:
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(loops)

def pause_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()

def unpause_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.unpause()

def stop_music(fadeout=0.0):
    pygame.mixer.music.fadeout(fadeout)

def play_sound(sound):
    if not mute:
        sound.play()
        
''' Image utilities '''
def load_image(img):
    return pygame.image.load(img).convert_alpha()

# Stages
START = 0
PLAYING = 1
PAUSED = 2
END = 3
    
class Game:
    def __init__(self):
        pygame.init()
        
        self.window = pygame.display.set_mode([WIDTH, HEIGHT])
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(TITLE)

        self.load_assets()
        self.new()
        
    def load_assets(self):
        self.p1_images = { 'normal': load_image(P1_IMAGES['normal']),
                           'gun_out': load_image(P1_IMAGES['gun_out']) }

        self.projectile_images = { 'laser_red': load_image(LASER_IMAGE) }

        self.tile_images = { 'wall_ul': load_image(TILES['wall_ul']) }
                     
        self.item_images = {}
                       
        self.music = { 'start': START_MUSIC,
                       'main': MAIN_THEME,
                       'end': END_MUSIC }
                       
        self.sound_effects = { 'laser': pygame.mixer.Sound(LASER_SOUND) }

        self.fonts = { 'sm': pygame.font.Font(BASE_FONT, 36),
                       'md': pygame.font.Font(BASE_FONT, 48),
                       'lg': pygame.font.Font(BASE_FONT, 64),
                       'title': pygame.font.Font(TITLE_FONT, 96) }

    def new(self):
        self.players = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()

        self.p1 = Player(300, 300, 1, self.p1_images, self)
        self.players.add(self.p1)

        o1 = Obstacle(400, 500, self.tile_images['wall_ul'])
        o2 = Obstacle(200, 100, self.tile_images['wall_ul'])
        o3 = Obstacle(500, 300, self.tile_images['wall_ul'])
        self.obstacles.add(o1, o2, o3)
    
        self.stage = START
        self.running = True
        self.mute = True
        self.draw_grid = False
    
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.window, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.window, LIGHTGREY, (0, y), (WIDTH, y))

    def intro_screen(self):
        f = self.fonts['title']
        title = f.render(TITLE, 1, BLACK)
        title_rect = title.get_rect()
        title_rect.centerx = WIDTH / 2
        title_rect.centery = 265

        f = self.fonts['sm']
        sub_title = f.render("Press space to start", 1, BLACK)
        sub_title_rect = sub_title.get_rect()
        sub_title_rect.centerx = WIDTH / 2
        sub_title_rect.centery = 325

        self.window.blit(title, title_rect)
        self.window.blit(sub_title, sub_title_rect)
    
    def end_screen(self):
        f = self.fonts['lg']
        title = f.render("Game Over", 1, BLACK)
        title_rect = title.get_rect()
        title_rect.centerx = WIDTH / 2
        title_rect.centery = 275

        f = self.fonts['sm']
        sub_title = f.render("Press space to restart", 1, BLACK)
        sub_title_rect = sub_title.get_rect()
        sub_title_rect.centerx = WIDTH / 2
        sub_title_rect.centery = 325

        self.window.blit(title, title_rect)
        self.window.blit(sub_title, sub_title_rect)

    def show_stats(self):
        score_txt = fonts['sm'].render(str(score), 1, BLACK)
        score_rect = score_txt.get_rect()
        score_rect.centerx = WIDTH / 2
        score_rect.centery = 30

        self.window.blit(score_txt, score_rect)

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.stage == START:
                    if event.key == START_KEY:
                        self.stage = PLAYING

                elif self.stage == PLAYING:
                    if event.key == P1_CONTROLS['toggle_gun']:
                        self.p1.gun_out = not self.p1.gun_out
                    elif event.key == P1_CONTROLS['shoot']:
                        self.p1.shoot()
                    elif event.key == TOGGLE_MUTE:
                        self.mute = not self.mute
                
                elif event.stage == END:
                    if event.key == START_KEY:
                        self.stage = START

        pressed = pygame.key.get_pressed()
            
        if pressed[P1_CONTROLS['up']]:
            self.p1.direction = 0
            self.p1.moving = True
        elif pressed[P1_CONTROLS['right']]:
            self.p1.direction = 1
            self.p1.moving = True
        elif pressed[P1_CONTROLS['down']]:
            self.p1.direction = 2
            self.p1.moving = True
        elif pressed[P1_CONTROLS['left']]:
            self.p1.direction = 3
            self.p1.moving = True
        else:
            self.p1.moving = False
            
    def update(self):
        self.players.update()
        self.lasers.update()
        
    def render(self):
        self.window.fill(GRAY)

        if self.stage == START:
            self.intro_screen()
            
        elif self.stage == PLAYING:
            self.players.draw(self.window)
            for p in self.players:
                pygame.draw.rect(self.window, BLACK, p.rect, 1)
            self.obstacles.draw(self.window)
            self.lasers.draw(self.window)
            
        elif self.stage == END:
            self.end_screen()
        
    def quit(self):
        pygame.quit()
        sys.exit()
        
    def run(self):
        while self.running:
            self.process_input()
            self.update()
            self.render()
            
            pygame.display.update()
            self.clock.tick(FPS)

# Go!
if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()
    g.quit()

