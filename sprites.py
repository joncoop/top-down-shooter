import pygame
from settings import *

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, direction, images, game):
        super().__init__()

        self.images = images
        self.direction = direction
        self.moving = False
        self.gun_out = False      
        self.set_image()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vy = 0
        self.vx = 0
        self.game = game
        
    def set_image(self):
        if self.gun_out:
            img = self.images['gun_out']
        else:
            img = self.images['normal']

        if self.direction == 0:
            self.image = pygame.transform.rotate(img, 90)
        elif self.direction == 1:
            self.image = pygame.transform.rotate(img, 0)
        elif self.direction == 2:
            self.image = pygame.transform.rotate(img, 270)
        elif self.direction == 3:
            self.image = pygame.transform.rotate(img, 180)

    def set_rect(self):
        x, y = self.rect.x, self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        
    def shoot(self):
        if self.gun_out:
            x = self.rect.centerx
            y = self.rect.centery
            d = self.direction
            img = self.game.projectile_images['laser_red']
            
            if d == 0:
                x += 7
                y -= 75
            elif d == 1:
                x += 30
                y += 6
            elif d == 2:
                x -= 12
                y += 28
            elif d == 3:
                x -= 73
                y -= 13
              
            laser = Laser(x, y, d, img, self.game)
            self.game.lasers.add(laser)
            #play_sound(sound_effects['laser'])
    
    def move(self):
        if self.moving:
            if self.gun_out:
                speed = PLAYER_NORMAL_SPEED
            else:
                speed = PLAYER_MAX_SPEED
                
            if self.direction == 0:
                self.vx = 0
                self.vy = -speed
            elif self.direction == 1:
                self.vx = speed
                self.vy = 0
            elif self.direction == 2:
                self.vx = 0
                self.vy = speed
            elif self.direction == 3:
                self.vx = -speed
                self.vy = 0
        else:
            self.vx = 0
            self.vy = 0

        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, self.game.obstacles, False)

        for obstacle in hit_list:
            if self.rect.centerx < obstacle.rect.centerx:
                self.rect.right = obstacle.rect.left
            elif self.rect.centerx > obstacle.rect.centerx:
                self.rect.left = obstacle.rect.right

        self.rect.y += self.vy
        hit_list = pygame.sprite.spritecollide(self, self.game.obstacles, False)

        for obstacle in hit_list:
            if self.rect.centery < obstacle.rect.centery:
                self.rect.bottom = obstacle.rect.top
            elif self.rect.centery > obstacle.rect.centery:
                self.rect.top = obstacle.rect.bottom
        
    def check_edges(self):
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, HEIGHT)
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)
    
    def update(self):
        self.set_image()
        self.set_rect()
        
        self.move()
        self.check_edges()
        

class Obstacle(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Laser(pygame.sprite.Sprite):

    def __init__(self, x, y, direction, image, game):
        super().__init__()

        self.image = image

        if direction == 0 or direction == 2:
            self.image = image
        else:
            self.image = pygame.transform.rotate(image, 90)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.speed = 12
        self.game = game

    def move(self):
        if self.direction == 0:
            self.rect.y -= LASER_SPEED
        elif self.direction == 1:
            self.rect.x += LASER_SPEED
        elif self.direction == 2:
            self.rect.y += LASER_SPEED
        elif self.direction == 3:
            self.rect.x -= LASER_SPEED

    def check_obstacles(self):
        hit_list = pygame.sprite.spritecollide(self, self.game.obstacles, False)

        if len(hit_list) > 0:
            self.kill()
            
    def check_edges(self):
        if (self.rect.bottom < 0 or self.rect.top > HEIGHT or
            self.rect.right < 0 or self.rect.left > WIDTH):
            self.kill()        
    
    def update(self):
        self.move()
        self.check_obstacles()
        self.check_edges()

