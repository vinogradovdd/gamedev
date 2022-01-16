import pygame
from config import *
import math
import random

vec = pygame.math.Vector2
from random import randint, uniform


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.bullets = 10
        self.collide_x = False
        self.collide_y = False

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.collide_x = False
        self.collide_y = False
        self.movement()
        self.animate()
        self.collide_enemy()
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_d]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change = PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_w]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_s]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False

    def collide_blocks(self, direction):

        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:

                self.collide_x = True
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                self.collide_y = True
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED

    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]
        if self.facing == "down":
            self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


class Rabbit(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.peacefull
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width / 2, self.height / 2])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.pos = vec(self.rect.x, self.rect.y)
        self.vel = vec(RABBIT_SPEED, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.target = vec(randint(0, WIN_WIDTH), randint(0, WIN_HEIGHT))
        self.last_target = 0

    def flee(self, target):
        steer = vec(0, 0)
        self.desired = vec(0, 0)
        dist = self.pos - target
        if FLEE_RADIUS_RABBIT > dist.length() > 0:
            self.desired = dist.normalize() * RABBIT_SPEED
            steer = self.desired - self.vel
            if steer.length() > MAX_FORCE_RABBIT:
                steer.scale_to_length(MAX_FORCE_RABBIT)
        return steer

    def seek(self, target):
        self.desired = (target - self.pos).normalize() * RABBIT_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE_RABBIT:
            steer.scale_to_length(MAX_FORCE_RABBIT)
        return steer

    def wander(self):
        now = pygame.time.get_ticks()
        if now - self.last_target > 500:
            self.last_target = now
            self.target = vec(randint(0, WIN_WIDTH), randint(0, WIN_HEIGHT))
        return self.seek(self.target)

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits:
            self.vel = -self.acc
        hits_e = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits_e:
            self.kill()

    def update(self):
        self.acc = self.wander()
        self.vel += self.acc
        for sprite in self.game.peacefull:
            if (self.pos - sprite.rect.center).length() < FLEE_RADIUS_RABBIT:
                self.acc += self.flee(sprite.rect.center)
        for sprite in self.game.enemies:
            if (self.pos - sprite.rect.center).length() < FLEE_RADIUS_RABBIT:
                self.acc += self.flee(sprite.rect.center)
        if self.vel.length() > RABBIT_SPEED:
            self.vel.scale_to_length(RABBIT_SPEED)
        self.collide()
        self.pos += self.vel
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            if not self.game.player.collide_x:
                self.pos.x += PLAYER_SPEED
        if keys[pygame.K_d]:
            if not self.game.player.collide_x:
                self.pos.x -= PLAYER_SPEED
        if keys[pygame.K_w]:
            if not self.game.player.collide_y:
                self.pos.y += PLAYER_SPEED
        if keys[pygame.K_s]:
            if not self.game.player.collide_y:
                self.pos.y -= PLAYER_SPEED
        self.rect.center = self.pos


class Doe(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tag, group_tag, lead=None):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.peacefull
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE
        self.tag = tag
        self.group_tag = group_tag
        self.image = pygame.Surface([self.width / 2, self.height / 2])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.lead = lead
        self.pos = vec(self.rect.x, self.rect.y)
        self.vel = vec(DOE_SPEED, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.target = vec(randint(0, WIN_WIDTH), randint(0, WIN_HEIGHT))
        self.last_target = 0

    def flee(self, target):
        steer = vec(0, 0)
        self.desired = vec(0, 0)
        dist = self.pos - target
        if 0 < dist.length() < FLEE_RADIUS_DOE:
            self.desired = dist.normalize() * DOE_SPEED
            steer = self.desired - self.vel
            if steer.length() > MAX_FORCE_DOE:
                steer.scale_to_length(MAX_FORCE_DOE)
        return steer

    def seek(self, target):
        self.desired = (target - self.pos).normalize() * DOE_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE_DOE:
            steer.scale_to_length(MAX_FORCE_DOE)
        return steer

    def wander(self):
        now = pygame.time.get_ticks()
        if now - self.last_target > 500:
            self.last_target = now
            self.target = vec(randint(0, WIN_WIDTH), randint(0, WIN_HEIGHT))
        return self.seek(self.target)

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits:
            self.vel = -self.acc
        hits_e = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits_e:
            self.kill()

    def update(self):
        if self.tag == 'lead':
            self.acc = self.wander()
            self.vel += self.acc
            for sprite in self.game.enemies:
                if (self.pos - sprite.rect.center).length() < FLEE_RADIUS_RABBIT:
                    self.acc += self.flee(sprite.rect.center)
        if self.tag == 'member':
            self.acc = self.seek(self.lead.rect.center)
            self.vel += self.acc
        if self.vel.length() > RABBIT_SPEED:
            self.vel.scale_to_length(RABBIT_SPEED)
        self.collide()
        self.pos += self.vel
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            if not self.game.player.collide_x:
                self.pos.x += PLAYER_SPEED
        if keys[pygame.K_d]:
            if not self.game.player.collide_x:
                self.pos.x -= PLAYER_SPEED
        if keys[pygame.K_w]:
            if not self.game.player.collide_y:
                self.pos.y += PLAYER_SPEED
        if keys[pygame.K_s]:
            if not self.game.player.collide_y:
                self.pos.y -= PLAYER_SPEED
        self.rect.center = self.pos


class Wolf(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width / 2, self.height / 2])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.nearest = 10000
        self.nearest_sprite = None
        self.pos = vec(self.rect.x, self.rect.y)
        self.vel = vec(WOLF_SPEED, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.target = vec(randint(0, WIN_WIDTH), randint(0, WIN_HEIGHT))
        self.last_target = 0

    def wander(self):
        now = pygame.time.get_ticks()
        if now - self.last_target > 500:
            self.last_target = now
            self.target = vec(randint(0, WIN_WIDTH), randint(0, WIN_HEIGHT))
        return self.seek(self.target)

    def seek(self, target):
        self.desired = (target - self.pos).normalize() * WOLF_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE_WOLF:
            steer.scale_to_length(MAX_FORCE_WOLF)
        return steer

    def collide(self):
        hits_e = pygame.sprite.spritecollide(self, self.game.peacefull, True)

    def update(self):
        self.acc = self.wander()
        self.vel += self.acc
        self.nearest = 10000
        self.nearest_sprite = None
        for sprite in self.game.peacefull:
            if (self.pos - sprite.rect.center).length() < self.nearest:
                self.nearest = (self.pos - sprite.rect.center).length()
                self.nearest_sprite = sprite
            if 0 < self.nearest < 10000 and self.nearest_sprite is not None:
                self.acc = self.seek(self.nearest_sprite.rect.center)
                self.vel = self.acc
        if self.vel.length() > WOLF_SPEED:
            self.vel.scale_to_length(WOLF_SPEED)
        self.collide()
        self.pos += self.vel

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if not self.game.player.collide_x:
                self.pos.x += PLAYER_SPEED
        if keys[pygame.K_d]:
            if not self.game.player.collide_x:
                self.pos.x -= PLAYER_SPEED
        if keys[pygame.K_w]:
            if not self.game.player.collide_y:
                self.pos.y += PLAYER_SPEED
        if keys[pygame.K_s]:
            if not self.game.player.collide_y:
                self.pos.y -= PLAYER_SPEED
        self.rect.center = self.pos


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('Arina.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False


class Attack(pygame.sprite.Sprite):

    def __init__(self, game, x, y, mouse_x, mouse_y, angle):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.movement_loop = 0
        self.angle = angle

        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.max_distance = 45
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0
        self.image = pygame.Surface([5, 5])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.collide()
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        self.x_change -= BULLET_SPEED * math.cos(self.angle)
        self.y_change -= BULLET_SPEED * math.sin(self.angle)
        self.movement_loop += 1
        if self.movement_loop >= self.max_distance:
            self.kill()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)
        hits_p = pygame.sprite.spritecollide(self, self.game.peacefull, True)
        hits_blocks = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits_blocks:
            self.kill()
