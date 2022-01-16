import pygame
from sprites import *
from config import *
import sys
import socket


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('Arina.ttf', 32)
        self.s = socket.socket()
        self.host = 'localhost'
        self.port = 12345
        self.running = True
        self.conn = None
        self.addr = None
        self.enemy = None
        self.win = False
        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.intro_background = pygame.image.load('img/introbackground.png')
        self.go_background = pygame.image.load('img/gameover.png')
        self.win_background = pygame.image.load('img/introbackground.png')

    def getEnemyInfo(self):
        received = self.conn.recv(1024)
        result = received.decode('utf-8').split('\n')
        coord_x = int(result[0])
        coord_y = int(result[1])
        health = int(result[2])
        damage = int(result[3])
        return coord_x, coord_y, health, damage

    def sendMyCoords(self):
        str_coord = str(self.player.x_change) + '\n' + str(self.player.y_change) + '\n' + str(self.enemy.health) + '\n' + str(self.enemy.damage)
        self.conn.sendall(str_coord.encode('utf-8'))
        if self.enemy.health <= 0:
            self.win = True
            self.playing = False

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "S":
                    Bullet_package(self, j, i)
                if column == "H":
                    Health_package(self, j, i)
                if column == "E":
                    self.enemy = Enemy(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)

    def new(self):

        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.boosts_bullets = pygame.sprite.LayeredUpdates()
        self.boosts_health = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.player.bullets > 0:
                        Attack(self, self.player.rect.x, self.player.rect.y, mouse_x, mouse_x,
                               math.atan2(self.player.rect.y - mouse_y,
                                          self.player.rect.x - mouse_x))
                        self.player.bullets -= 1

    def update(self):

        self.all_sprites.update()
        if self.player.health <= 0:
            self.playing = False
        strng = 'Bullets: ' + str(self.player.bullets) + '/10'
        text = self.font.render(strng, True, WHITE)
        text_rect = text.get_rect(center=(60, 20))
        self.screen.blit(text, text_rect)

        strng = 'My Health: ' + str(self.player.health) + '/100'
        text = self.font.render(strng, True, WHITE)
        text_rect = text.get_rect(center=(50, 50))
        self.screen.blit(text, text_rect)

        strng = 'Enemy Health: ' + str(self.enemy.health) + '/100'
        text = self.font.render(strng, True, WHITE)
        text_rect = text.get_rect(center=(100, 80))
        self.screen.blit(text, text_rect)

        pygame.display.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        text = self.font.render('Game Over', True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))
        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.blit(self.go_background, (0, 0))
            self.screen.blit(text, text_rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def game_winner(self):
        text = self.font.render('You Win!', True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))
        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.blit(self.win_background, (0, 0))
            self.screen.blit(text, text_rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        intro = True
        play_button = Button(275, 180, 100, 50, WHITE, BLACK, 'Play', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


g = Game()
g.s.bind((g.host, g.port))
g.s.listen(5)
g.conn, g.addr = g.s.accept()
print('Got connection from ', g.addr[0], '(', g.addr[1], ')')
str_tilemap = ""
for row in tilemap:
    str_tilemap += row + "\n"
g.conn.sendall(str_tilemap.encode('utf-8'))
g.intro_screen()
g.new()
while g.running:
    g.main()
    if g.win == False:
        g.game_over()
    else:
        g.game_winner()

pygame.quit()
sys.exit()
