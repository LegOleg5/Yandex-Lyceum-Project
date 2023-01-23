import random
import math
import pygame as pg
import sys
import pytweening

DISPLAY_SIZE = (1240, 720)
pytweening.linear(1.0)
pytweening.easeInQuad(1.0)
pytweening.easeInOutSine(1.0)

class Bullet(pg.sprite.Sprite):

    def __init__(self, start_pos, target, type, *groups):
        super().__init__(*groups)
        self.type = type
        if self.type == 'player':
            self.image = pg.image.load('data/img/attack1_kaneky.png')
            self.damage = 15
        if self.type == 'morph':
            self.image = pg.image.load('data/img/attack1_morfling.png')
            self.damage = 20
        self.start_pos = start_pos
        self.pos = start_pos
        self.target = target
        self.rect = self.image.get_rect().move(self.pos)
        self.vel = self.calc_vel()
        self.image = pg.transform.rotate(self.image, (-math.atan(self.target[0] - self.pos[0] / self.target[1] - self.pos[1]) * 180) / math.pi)

    def calc_vel(self):
        d = (self.target[0] - self.start_pos[0], self.target[1] - self.start_pos[1])
        len_d = math.sqrt(d[0] ** 2 + d[1] ** 2)
        dn = (d[0] / len_d, d[1] / len_d)
        if self.type == 'player':
            return dn[0] * 128 * 10, dn[1] * 128 * 10
        if self.type == 'morph':
            return dn[0] * 64 * 10, dn[1] * 64 * 10

    def update(self, dt):
        for tile in pg.sprite.spritecollide(self, level.get_tiles(), False):
            if tile.type == 'wall':
                self.kill()
        if self.type == 'player':
            for enemy in pg.sprite.spritecollide(self, enemies_group, False):
                enemy.get_damage(self.damage)
                self.kill()
        elif self.type == 'morph':
            if pg.sprite.spritecollide(self, player_group, False):
                player.get_damage(self.damage)
                self.kill()

        self.pos = (self.rect.x + self.vel[0] * dt, self.rect.y + self.vel[1] * dt)
        self.rect.x, self.rect.y = self.pos


class Enemy(pg.sprite.Sprite):
    MORPHLING = [pg.image.load('data/img/enemies/Morphling/Morf1.png'),
                 pg.image.load('data/img/enemies/Morphling/Morf2.png'),
                 pg.image.load('data/img/enemies/Morphling/Morf3.png'),
                 pg.image.load('data/img/enemies/Morphling/Morf4.png')]

    SF = [pg.image.load('data/img/enemies/Sf/SF1.png'),
          pg.image.load('data/img/enemies/Sf/SF2.png'),
          pg.image.load('data/img/enemies/Sf/SF3.png'),
          pg.image.load('data/img/enemies/Sf/SF4.png'),
          pg.image.load('data/img/enemies/Sf/SF3.png'),
          pg.image.load('data/img/enemies/Sf/SF2.png')]

    BS = [pg.image.load('data/img/enemies/blood_seeker/Blood_Seeker1.png'),
          pg.image.load('data/img/enemies/blood_seeker/Blood_Seeker2.png'),
          pg.image.load('data/img/enemies/blood_seeker/Blood_Seeker3.png'),
          pg.image.load('data/img/enemies/blood_seeker/Blood_Seeker4.png')]

    def __init__(self, pos, type, *groups):
        super().__init__(*groups)
        if type == 'morph':
            # TODO
            self.image = Enemy.MORPHLING[0]
            self.hp = 40
            self.damage = 20
        elif type == 'blood_seeker':
            # TODO
            self.image = Enemy.BS[0]
            self.hp = 70
            self.damage = 30
        self.type = type
        self.pos = pos
        self.rect = self.image.get_rect().move(pos)
        self.vel = (0, 0)
        self.time_passed = 0
        self.frame = 0
        self.fps = 1
        self.dps = 0.3

    def calc_vel(self, target):
        pass

    def find_path_to_player(self):
        d = (player.pos[0] - self.pos[0], player.pos[1] - self.pos[1])
        len_d = math.sqrt(d[0] ** 2 + d[1] ** 2)
        dn = (d[0] / len_d, d[1] / len_d)
        self.vel = dn[0] * 128 * 10, dn[1] * 128 * 10

    def update(self, dt):
        self.time_passed += dt
        if self.time_passed >= 1 / self.dps:
            self.do_damage()
            self.time_passed = 0
        if self.hp <= 0:
            print('killed')
            self.kill()
        #self.do_damage()

        # animation
        if self.type == 'morph':
            self.image = Enemy.MORPHLING[self.frame // 10]
            if self.frame < 39:
                self.frame += 1
            else:
                self.frame -= 39
        if self.type == 'blood_seeker':
            self.image = Enemy.BS[self.frame // 10]
            if self.frame < 19:
                self.frame += 1
            else:
                self.frame -= 19

    def movement(self):
        for tile in pg.sprite.spritecollide(self, level.get_tiles(), False):
            if tile.type == 'wall':
                self.rect = self.rect.move(-self.vel[0], -self.vel[1])

        self.pos = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])
        self.rect.move(self.pos)

    def get_damage(self, dmg):
        self.hp -= dmg

    def do_damage(self):
        if self.type == 'morph':
            b = Bullet((self.rect.centerx + camera.pos[0], self.rect.centery + camera.pos[1]),
                       (player.rect.centerx + camera.pos[0], player.rect.centery + camera.pos[1]),
                       'morph', bullets_group)
            b.rect.x -= camera.pos[0]
            b.rect.y -= camera.pos[1]


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
        self.hp = 100

    def update(self):
        if self.hp <= 0:
            self.kill()
        self.movement()

    def movement(self):
        self.rect = self.rect.move(self.vel)
        for tile in pg.sprite.spritecollide(self, level.get_tiles(), False):
            if tile.type == 'wall':
                self.rect = self.rect.move(-self.vel[0], -self.vel[1])

        # animation
        self.image = pg.image.load(Player.KANEKY[self.frame // 5])
        if self.frame < 25:
            self.frame += 1
        else:
            self.frame -= 25

    def update_vel(self, x, y):
        self.vel = (self.vel[0] + x, self.vel[1] + y)

    def shoot(self, target):
        b = Bullet((self.rect.centerx + camera.pos[0], self.rect.centery + camera.pos[1]),
                   (target[0] + camera.pos[0], target[1] + camera.pos[1]), 'player',
                   bullets_group)
        b.rect.x -= camera.pos[0]
        b.rect.y -= camera.pos[1]

    def get_damage(self, dmg):
        self.hp -= dmg


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
        self.enemies = []
        with open(lvl_path, mode='r') as level_file:
            for y, line in enumerate(level_file):
                line = line.strip()
                for x, symbol in enumerate(line):
                    if symbol == '.':
                        Tile('floor2', (x, y), self.tile_group)
                    if symbol == ',':
                        Tile('floor3', (x, y), self.tile_group)
                    if symbol == '!':
                        Tile('floor1', (x, y), self.tile_group)
                    if symbol == '#':
                        Tile('wall', (x, y), self.tile_group)
                    if symbol == '@':
                        Tile('floor1', (x, y), self.tile_group)
                        self.spawn = (x * Tile.size, y * Tile.size)
                    if symbol == '+':
                        Tile('floor1', (x, y), self.tile_group)
                        self.enemies.append(((x * Tile.size, y * Tile.size), 'morph'))
                    if symbol == '=':
                        Tile('floor2', (x, y), self.tile_group)
                        self.enemies.append(((x * Tile.size, y * Tile.size), 'morph'))
                    if symbol == 'f':
                        Tile('floor3', (x, y), self.tile_group)
                        self.enemies.append(((x * Tile.size, y * Tile.size), 'morph'))
                    if symbol == '-':
                        Tile('floor1', (x, y), self.tile_group)
                        self.enemies.append(((x * Tile.size, y * Tile.size), 'blood_seeker'))

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
        self.pos =(0, 0)

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - DISPLAY_SIZE[0] // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - DISPLAY_SIZE[1] // 2)
        self.pos = (self.pos[0] - self.dx, self.pos[1] - self.dy)


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
                    return
                else:
                    pass

    buttons_group = pg.sprite.Group()
    change_char = Button((215, 310), 'change', buttons_group)
    start_game = Button((215, 435), 'start', buttons_group)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            elif event.type == pg.MOUSEBUTTONDOWN:
                buttons_group.update(event.pos)
                return
        pg.display.flip()
        clock.tick(144)
        buttons_group.draw(screen)


lvl_name = input()

pg.init()
pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP, pg.MOUSEBUTTONDOWN])
pg.display.set_caption('Перемещение героя. Камера')
screen = pg.display.set_mode(DISPLAY_SIZE)
clock = pg.time.Clock()
player_group = pg.sprite.Group()
level = Level(f'data/levels/{lvl_name}.txt')
player = Player(level.spawn, player_group)
bullets_group = pg.sprite.Group()
enemies_group = pg.sprite.Group()
main_menu(screen, DISPLAY_SIZE)
camera = Camera()
if level.enemies:
    for enemy_pos in level.enemies:
        Enemy(*enemy_pos, enemies_group)

while(1):
    print("FPS:", int(clock.get_fps()))
    dt = clock.tick() / 1000
    screen.fill('black')
    for tile in level.tile_group:
        camera.apply(tile)
    for bullet in bullets_group:
        camera.apply(bullet)
    for enemy in enemies_group:
        enemy.movement()
        camera.apply(enemy)
    camera.apply(player)
    camera.update(player)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            terminate()

        if event.type == pg.MOUSEBUTTONDOWN:
            # print((player.rect.centerx + camera.pos[0], player.rect.centery + camera.pos[1]),
            #        (event.pos[0] + camera.pos[0], event.pos[1] + camera.pos[1]))
            player.shoot(event.pos)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                player.update_vel(0, -1 * 7)
            if event.key == pg.K_s:
                player.update_vel(0, 7)
            if event.key == pg.K_a:
                player.update_vel(-7, 0)
            if event.key == pg.K_d:
                player.update_vel(7, 0)
        if event.type == pg.KEYUP:
            if event.key == pg.K_w:
                player.update_vel(0, 7)
            if event.key == pg.K_s:
                player.update_vel(0, -7)
            if event.key == pg.K_a:
                player.update_vel(7, 0)
            if event.key == pg.K_d:
                player.update_vel(-7, 0)

    player.update()
    bullets_group.update(dt)
    enemies_group.update(dt)
    level.draw(screen)
    player_group.draw(screen)
    bullets_group.draw(screen)
    enemies_group.draw(screen)

    pg.display.flip()
pg.quit()