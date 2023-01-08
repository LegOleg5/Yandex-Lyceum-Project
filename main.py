import os.path
import random

import pygame as pg
import sys
import pytweening

DISPLAY_SIZE = (1240, 720)
pytweening.linear(1.0)
pytweening.easeInQuad(1.0)
pytweening.easeInOutSine(1.0)


class Bullet(pg.sprite.Sprite):

    def __init__(self, start_pos, target, *groups):
        super().__init__(*groups)
        self.start_pos = start_pos
        self.pos = start_pos
        self.target = target
        self.image = pg.image.load('data/img/mar.png')
        self.rect = self.image.get_rect().move(self.pos)
        self.damage = 10
        self.vel = (0, 0)

    def update(self, dt):
        for tile in pg.sprite.spritecollide(self, level.get_tiles(), False):
            if tile.type == 'wall':
                self.kill()
        if self.vel == (0, 0):
            self.vel = ((self.target[0] - self.start_pos[0]) / (500 * (dt / 1000)), (self.target[1] - self.start_pos[1]) / (500 * (dt / 1000)))
        self.pos = (self.pos[0] + self.vel[0], self.pos[0] + self.vel[1])
        self.rect.move(self.pos)


class Enemy(pg.sprite.Sprite):
    MORPHLING = ['data/img/heroes/Morphling/Morf1.png',
                 'data/img/heroes/Morphling/Morf2.png',
                 'data/img/heroes/Morphling/Morf3.png',
                 'data/img/heroes/Morphling/Morf4.png']

    SF = ['data/img/heroes/Sf/SF1.png',
          'data/img/heroes/Sf/SF2.png',
          'data/img/heroes/Sf/SF3.png',
          'data/img/heroes/Sf/SF4.png',
          'data/img/heroes/Sf/SF3.png',
          'data/img/heroes/Sf/SF2.png']

    def __init__(self, pos, type, *groups):
        super().__init__(*groups)
        if type == 'morph':
            # TODO
            self.image = pg.image.load('data/img/state_morphling.png')
            self.hp = 40
        elif type == 'jugger':
            # TODO
            self.hp = 70
        self.rect = self.image.get_rect().move(pos)
        self.vel = (0, 0)

    def update(self, dt):
        # TODO
        if self.hp <= 0:
            self.kill()


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
    KANEKY = ['data/img/heroes/Kaneky/Kagune1.png',
              'data/img/heroes/Kaneky/Kagune2.png',
              'data/img/heroes/Kaneky/Kagune3.png',
              'data/img/heroes/Kaneky/Kagune4.png',
              'data/img/heroes/Kaneky/Kagune3.png',
              'data/img/heroes/Kaneky/Kagune2.png']

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.pos = pos
        self.image = pg.image.load('data/img/heroes/Kaneky/Kagune1.png')
        self.rect = self.image.get_rect().move(pos)
        self.vel = (0, 0)
        self.frame = 1

    def movement(self, level):
        self.rect = self.rect.move(self.vel)
        for tile in pg.sprite.spritecollide(self, level.get_tiles(), False):
            if tile.type == 'wall':
                self.rect = self.rect.move(-self.vel[0], -self.vel[1])

        # animation
        self.image = pg.image.load(Player.KANEKY[self.frame // 10])
        if self.frame < 50:
            self.frame += 1
        else:
            self.frame -= 50

    def update_vel(self, x, y):
        self.vel = (self.vel[0] + x, self.vel[1] + y)


class Tile(pg.sprite.Sprite):
    WOODEN_FLOORS = ['data/img/floors/wooden_floor1.png',
                     'data/img/floors/wooden_floor2.png',
                     'data/img/floors/wooden_floor3.png',
                     'data/img/floors/wooden_floor4.png']

    STONE_FLOORS = ['data/img/floors/stone_floor1.png',
                    'data/img/floors/stone_floor2.png',
                    'data/img/floors/stone_floor3.png',
                    'data/img/floors/stone_floor4.png']

    COBBLE_FLOORS = ['data/img/floors/cobble_floor1.png',
                     'data/img/floors/cobble_floor2.png',
                     'data/img/floors/cobble_floor3.png',
                     'data/img/floors/cobble_floor4.png']

    size = 64
    images = {
        'wall': pg.image.load('data/img/walls/cross_wall.png'),
        'floor1': pg.image.load('data/img/floors/wooden_floor4.png'),
        'floor2': pg.image.load('data/img/floors/stone_floor4.png'),
        'floor3': pg.image.load('data/img/floors/cobble_floor4.png')
    }

    def __init__(self, tile_type, tile_pos, *groups):
        super().__init__(*groups)
        Tile.images['floor1'] = pg.image.load(Tile.WOODEN_FLOORS[random.randint(0, 3)])
        Tile.images['floor2'] = pg.image.load(Tile.STONE_FLOORS[random.randint(0, 3)])
        Tile.images['floor3'] = pg.image.load(Tile.COBBLE_FLOORS[random.randint(0, 3)])
        self.image = Tile.images[tile_type]
        self.rect = self.image.get_rect().move(tile_pos[0] * Tile.size,
                                               tile_pos[1] * Tile.size)
        self.type = tile_type


class Level:

    def __init__(self, lvl_path):
        self.tile_group = pg.sprite.Group()
        self.spawn = (0, 0)
        with open(lvl_path, mode='r') as level_file:
            for y, line in enumerate(level_file):
                line = line.strip()
                for x, sym in enumerate(line):
                    if sym == '.':
                        Tile('floor2', (x, y), self.tile_group)
                    if sym == ',':
                        Tile('floor3', (x, y), self.tile_group)
                    if sym == '!':
                        Tile('floor1', (x, y), self.tile_group)
                    if sym == '#':
                        Tile('wall', (x, y), self.tile_group)
                    if sym == '@':
                        Tile('floor1', (x, y), self.tile_group)
                        self.spawn = (x * Tile.size, y * Tile.size)

    def get_tiles(self):
        return self.tile_group

    def spawn(self):
        return self.spawn

    def draw(self, surface):
        self.tile_group.draw(surface)


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


def main_menu(surface, size):
    screen.blit(pg.image.load('data/img/Menu/Menu2.png'), (0, 0))

    class Button(pg.sprite.Sprite):
        change_char_img = pg.image.load('data/img/Menu/ButtonChange.png')
        start_game_img = pg.image.load('data/img/Menu/ButtonStart.png')

        def __init__(self, pos, type, *groups):
            super().__init__(*groups)
            self.type = type
            if self.type == 'start':
                self.image = Button.start_game_img
            elif self.type == 'change':
                self.image = Button.change_char_img
            self.rect = self.image.get_rect().move(pos)

        def update(self, pos):
            if self.rect.collidepoint(pos):
                if self.type == 'start':
                    terminate()
                else:
                    pass


    buttons_group = pg.sprite.Group()
    Button((215, 310), 'change', buttons_group)
    Button((215, 435), 'start', buttons_group)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            elif event.type == pg.KEYDOWN or \
                    event.type == pg.MOUSEBUTTONDOWN:
                return
        pg.display.flip()
        clock.tick(144)
        buttons_group.draw(screen)


lvl_name = input()
if os.path.exists(f'data/levels/{lvl_name}.txt'):

    pg.init()
    pg.display.set_caption('Перемещение героя. Камера')
    screen = pg.display.set_mode(DISPLAY_SIZE)
    clock = pg.time.Clock()
    player_group = pg.sprite.Group()
    level = Level(f'data/levels/{lvl_name}.txt')
    player = Player(level.spawn, player_group)
    bullets_group = pg.sprite.Group()
    main_menu(screen, DISPLAY_SIZE)
    camera = Camera()
    running = True

    while running:
        dt = clock.tick(144)
        screen.fill('black')
        for sprite in level.tile_group:
            camera.apply(sprite)
        for bullet in bullets_group:
            bullet.update(dt)
            camera.apply(bullet)
        camera.apply(player)
        camera.update(player)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                Bullet((DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1] / 2), event.pos, bullets_group)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    player.update_vel(0, round(-300 * dt / 1000))
                if event.key == pg.K_s:
                    player.update_vel(0, round(300 * dt / 1000))
                if event.key == pg.K_a:
                    player.update_vel(round(-300 * dt / 1000), 0)
                if event.key == pg.K_d:
                    player.update_vel(round(300 * dt / 1000), 0)
            if event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    player.update_vel(0, round(300 * dt / 1000))
                if event.key == pg.K_s:
                    player.update_vel(0, round(-300 * dt / 1000))
                if event.key == pg.K_a:
                    player.update_vel(round(300 * dt / 1000), 0)
                if event.key == pg.K_d:
                    player.update_vel(round(-300 * dt / 1000), 0)

        player.movement(level)
        level.draw(screen)
        player_group.draw(screen)
        bullets_group.update(dt)
        bullets_group.draw(screen)

        pg.display.flip()
    pg.quit()
else:
    print('Уровня с таким именем не существует')