import os.path

import pygame as pg
import sys
import pytweening

DISPLAY_SIZE = (1024, 512)
pytweening.linear(1.0)
pytweening.easeInQuad(1.0)
pytweening.easeInOutSine(1.0)
KANEKY = ['data/img/brawlers/Kaneky/Kagune1.png',
          'data/img/brawlers/Kaneky/Kagune2.png',
          'data/img/brawlers/Kaneky/Kagune3.png',
          'data/img/brawlers/Kaneky/Kagune4.png',
          'data/img/brawlers/Kaneky/Kagune3.png',
          'data/img/brawlers/Kaneky/Kagune2.png']

class SpriteSheet:

    def __init__(self, surface, width_frames, height_frames):
        self.surface = surface
        self.current_frame = None
        self.frame_size = (surface.get_width() // width_frames,
                           surface.get_height() // height_frames)
        self.wf = width_frames
        self.hf = height_frames

    def get_frame(self, index):
        x = index % self.wf * self.frame_size[0]
        y = index % self.hf * self.frame_size[1]
        return self.surface.subsurface(pg.Rect(x, y, self.frame_size[0], self.frame_size[1]))


class Player(pg.sprite.Sprite):
    image = pg.image.load('data/img/brawlers/Kaneky/Kagune1.png')

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = Player.image
        self.rect = self.image.get_rect().move(pos)
        self.vel = (0, 0)
        self.x = 1

    def step(self, dx, dy, level):
        self.rect = self.rect.move(dx * Tile.size, dy * Tile.size)
        for tile in pg.sprite.spritecollide(self, level.get_tiles(), False):
            if tile.type == 'wall':
                self.rect = self.rect.move(-dx * Tile.size, -dy * Tile.size)
                break

    def movement(self):
        self.rect = self.rect.move(self.vel)
        self.image = pg.image.load(KANEKY[self.x // 10])
        if self.x < 50:
            self.x += 1
        else:
            self.x -= 50

    def update(self, x, y):
        self.vel = (self.vel[0] + x, self.vel[1] + y)


class Tile(pg.sprite.Sprite):

    size = 64
    images = {
        'wall': pg.image.load('data/img/walls/cross_wall.png'),
        'empty': pg.image.load('data/img/floors/wooden_floor4.png')
    }

    def __init__(self, tile_type, tile_pos, *groups):
        super().__init__(*groups)
        self.image = Tile.images[tile_type]
        self.rect = self.image.get_rect().move(tile_pos[0] * Tile.size,
                                               tile_pos[1] * Tile.size)
        self.type = tile_type


class Level:

    def __init__(self, lvl_path):
        self.tile_group = pg.sprite.Group()
        # self.player_group = pg.sprite.Group()
        self.spawn = (0, 0)
        with open(lvl_path, mode='r') as level_file:
            for y, line in enumerate(level_file):
                line = line.strip()
                for x, sym in enumerate(line):
                    if sym == '.':
                        Tile('empty', (x, y), self.tile_group)
                    if sym == '#':
                        Tile('wall', (x, y), self.tile_group)
                    if sym == '@':
                        Tile('empty', (x, y), self.tile_group)
                        self.spawn = (x * Tile.size, y * Tile.size)
                        # player = Player((x * Tile.size, y * Tile.size), self.player_group)

    def get_tiles(self):
        return self.tile_group

    def spawn(self):
        return self.spawn
    # def get_player(self):
    #     return next(iter(self.player_group))

    def draw(self, surface):
        self.tile_group.draw(surface)
        # self.player_group.draw(surface)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - DISPLAY_SIZE[0] // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - DISPLAY_SIZE[1] // 2)


def terminate():
    pg.quit()
    sys.exit()


def start_screen(surface, size):
    fon = pg.transform.scale(pg.image.load('data/img/fon.jpg'), size)
    screen.blit(fon, (0, 0))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            elif event.type == pg.KEYDOWN or \
                    event.type == pg.MOUSEBUTTONDOWN:
                return
        pg.display.flip()
        clock.tick(60)


lvl_name = input()
if os.path.exists(f'data/levels/{lvl_name}.txt'):

    pg.init()
    pg.display.set_caption('Перемещение героя. Камера')
    screen = pg.display.set_mode(DISPLAY_SIZE)
    clock = pg.time.Clock()
    player_group = pg.sprite.Group()
    level = Level(f'data/levels/{lvl_name}.txt')
    player = Player(level.spawn, player_group)
    start_screen(screen, DISPLAY_SIZE)
    camera = Camera()
    running = True
    dt = clock.tick(120)

    while running:
        screen.fill('black')
        for sprite in level.tile_group:
            camera.apply(sprite)
        camera.apply(player)
        camera.update(player)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    player.update(0, round(-100 * dt / 1000))
                if event.key == pg.K_s:
                    player.update(0, round(100 * dt / 1000))
                if event.key == pg.K_a:
                    player.update(round(-100 * dt / 1000), 0)
                if event.key == pg.K_d:
                    player.update(round(100 * dt / 1000), 0)
            if event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    player.update(0, round(100 * dt / 1000))
                if event.key == pg.K_s:
                    player.update(0, round(-100 * dt / 1000))
                if event.key == pg.K_a:
                    player.update(round(100 * dt / 1000), 0)
                if event.key == pg.K_d:
                    player.update(round(-100 * dt / 1000), 0)
        player.movement()

        level.draw(screen)
        player_group.draw(screen)

        pg.display.flip()
    pg.quit()
else:
    print('Уровня с таким именем не существует')