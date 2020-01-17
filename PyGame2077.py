#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import Libraries
import pygame
from pygame import *
import pyganim
import os

# Pygame Initialization
pygame.init()

# Display Parameters
display_width = 800
display_height = 640
size = (display_width, display_height)

background_color = "#000000"
display = pygame.display.set_mode(size)
pygame.display.set_caption("PyGame")

# Enemy Parameters
monster_width = 32
monster_height = 32
monster_color = "#2110FF"

# Player Parameters
speed = 7
acceleration_speed = 2.5
width = 22
height = 32
color = "#888888"

winner = False
game_finish = False

jump_power = 10
acceleration_jump = 1
grav = 0.35
anim_delay = 0.1
acceleration_anim = 0.05

# Platform Parameters
platform_width = 32
platform_height = 32
platform_color = "#000000"

player_life = 3

# Other Parameters
FILE_DIR = os.path.dirname(__file__)
ICON_DIR = os.path.dirname(__file__)

running_game = True

# Sprites
anim_monster = [('%s/monsters/fire1.png' % ICON_DIR),
                               ('%s/monsters/fire2.png' % ICON_DIR)]

anim_teleport = [
    ('%s/blocks/portal2.png' % ICON_DIR),
    ('%s/blocks/portal1.png' % ICON_DIR)]

anim_princess = [
    ('%s/blocks/princess_l.png' % ICON_DIR),
    ('%s/blocks/princess_r.png' % ICON_DIR)]

anim_walk_right = [('%s/mario/r1.png' % ICON_DIR),
                   ('%s/mario/r2.png' % ICON_DIR),
                   ('%s/mario/r3.png' % ICON_DIR),
                   ('%s/mario/r4.png' % ICON_DIR),
                   ('%s/mario/r5.png' % ICON_DIR)]

anim_walk_left = [('%s/mario/l1.png' % ICON_DIR),
                  ('%s/mario/l2.png' % ICON_DIR),
                  ('%s/mario/l3.png' % ICON_DIR),
                  ('%s/mario/l4.png' % ICON_DIR),
                  ('%s/mario/l5.png' % ICON_DIR)]

anim_jump_left = [('%s/mario/jl.png' % ICON_DIR, 0.1)]
anim_jump_right = [('%s/mario/jr.png' % ICON_DIR, 0.1)]
anim_jump = [('%s/mario/j.png' % ICON_DIR, 0.1)]
anim_stay = [('%s/mario/0.png' % ICON_DIR, 0.1)]


# Print Function
def print_text(message, x, y, font_color=(255, 255, 255), font_type='PingPong.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


# Pause Function
def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        print_text('Paused. Press enter to continue', 160, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()


class Player(sprite.Sprite):
    def __init__(self, x, y):
        global winner, game_finish, player_life
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.yvel = 0
        self.winner = winner
        self.game_finish = game_finish

        self.player_life = player_life

        self.onGround = False
        self.image = Surface((width, height))
        self.image.fill(Color(color))
        self.rect = Rect(x, y, width, height)
        self.image.set_colorkey(Color(color))

        boltAnim = []
        boltAnimSuperSpeed = []

        for anim in anim_walk_right:
            boltAnim.append((anim, anim_delay))
            boltAnimSuperSpeed.append((anim, acceleration_anim))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        self.boltAnimRightSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimRightSuperSpeed.play()

        boltAnim = []
        boltAnimSuperSpeed = []

        for anim in anim_walk_left:
            boltAnim.append((anim, anim_delay))
            boltAnimSuperSpeed.append((anim, acceleration_anim))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        self.boltAnimLeftSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimLeftSuperSpeed.play()

        self.boltAnimStay = pyganim.PygAnimation(anim_stay)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))

        self.boltAnimJumpLeft = pyganim.PygAnimation(anim_jump_left)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(anim_jump_right)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(anim_jump)
        self.boltAnimJump.play()

    def update(self, left, right, up, running, platforms):

        if up:
            if self.onGround:
                self.yvel = -jump_power
                if running and (left or right):
                    self.yvel -= acceleration_jump
                self.image.fill(Color(color))
                self.boltAnimJump.blit(self.image, (0, 0))

        if left:
            self.xvel = -speed
            self.image.fill(Color(color))
            if running:
                self.xvel -= acceleration_speed
                if not up:
                    self.boltAnimLeftSuperSpeed.blit(self.image, (0, 0))
            else:
                if not up:
                    self.boltAnimLeft.blit(self.image, (0, 0))
            if up:
                self.boltAnimJumpLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = speed
            self.image.fill(Color(color))
            if running:
                self.xvel += acceleration_speed
                if not up:
                    self.boltAnimRightSuperSpeed.blit(self.image, (0, 0))
            else:
                if not up:
                    self.boltAnimRight.blit(self.image, (0, 0))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))

        if not (left or right):
            self.xvel = 0
            if not up:
                self.image.fill(Color(color))
                self.boltAnimStay.blit(self.image, (0, 0))

        if not self.onGround:
            self.yvel += grav

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if isinstance(p, BlockDie) or isinstance(p, Monster):
                    self.die()
                elif isinstance(p, BlockTeleport):
                    self.teleporting(p.goX, p.goY)
                elif isinstance(p, Princess):
                    game_lose()
                else:
                    if xvel > 0:
                        self.rect.right = p.rect.left

                    if xvel < 0:
                        self.rect.left = p.rect.right

                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        self.yvel = 0

                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = 0

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY

    def die(self):
        if self.player_life > 0:
            time.wait(500)
            self.teleporting(self.startX, self.startY)
            self.player_life -= 1
            print(self.player_life)
        else:
            game_lose()


class Monster(sprite.Sprite):
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp):
        sprite.Sprite.__init__(self)
        self.image = Surface((monster_width, monster_height))
        self.image.fill(Color(monster_color))
        self.rect = Rect(x, y, monster_width, monster_height)
        self.image.set_colorkey(Color(monster_color))
        self.startX = x
        self.startY = y
        self.maxLengthLeft = maxLengthLeft
        self.maxLengthUp = maxLengthUp
        self.xvel = left
        self.yvel = up

        boltAnim = []
        for anim in anim_monster:
            boltAnim.append((anim, 0.3))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self, platforms):
        self.image.fill(Color(monster_color))
        self.boltAnim.blit(self.image, (0, 0))

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        self.collide(platforms)

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel = -self.xvel
        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.yvel = -self.yvel

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:
                self.xvel = - self.xvel
                self.yvel = - self.yvel


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((platform_width, platform_height))
        self.image.fill(Color(platform_color))
        self.image = image.load("%s/blocks/platform.png" % ICON_DIR)
        self.image.set_colorkey(Color(platform_color))
        self.rect = Rect(x, y, platform_width, platform_height)


class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("%s/blocks/dieBlock.png" % ICON_DIR)


class BlockTeleport(Platform):
    def __init__(self, x, y, goX, goY):
        Platform.__init__(self, x, y)
        self.goX = goX
        self.goY = goY

        boltAnim = []
        for anim in anim_teleport:
            boltAnim.append((anim, 0.3))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(platform_color))
        self.boltAnim.blit(self.image, (0, 0))


class Princess(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        boltAnim = []

        for anim in anim_princess:
            boltAnim.append((anim, 0.8))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(platform_color))
        self.boltAnim.blit(self.image, (0, 0))


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):

    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + display_width / 2, -t + display_height / 2

    l = min(0, l)
    l = max(-(camera.width-display_width), l)
    t = max(-(camera.height-display_height), t)
    t = min(0, t)

    return Rect(l, t, w, h)


def loadLevel():
    global playerX, playerY

    levelFile = open('%s/levels/1.txt' % FILE_DIR)
    line = " "
    commands = []
    while line[0] != "/":
        line = levelFile.readline()
        if line[0] == "[":
            while line[0] != "]":
                line = levelFile.readline()
                if line[0] != "]":
                    endLine = line.find("|")
                    level.append(line[0: endLine])

        if line[0] != "":
            commands = line.split()
            if len(commands) > 1:
                if commands[0] == "player":
                    playerX = int(commands[1])
                    playerY = int(commands[2])
                if commands[0] == "monster":
                    mn = Monster(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]),
                                 int(commands[5]), int(commands[6]))
                    entities.add(mn)
                    platforms.append(mn)
                    monsters.add(mn)


def start_screen():
    global display_width, display_height
    intro_text = ["Press any key on Mouse to continue",
                  "Rules: You must reach the Princess, ",
                  "while not touching monsters and spikes"]

    fon_image = pygame.image.load('fon.jpg')
    fon = pygame.transform.scale(fon_image, (display_width, display_height))
    display.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        display.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                return
        pygame.display.update()


def game_lose():
    global display_width, display_height, running_game

    fon_image = pygame.image.load('game-over.png')
    fon = pygame.transform.scale(fon_image, (display_width, display_height))
    display.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()
        pygame.display.update()


def main():
    global running_game, game_finish

    if game_finish == True:
        game_lose()
    start_screen()
    loadLevel()
    pygame.init()

    left = right = False
    up = False
    running = False

    hero = Player(playerX, playerY)
    entities.add(hero)

    timer = pygame.time.Clock()
    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                bd = BlockDie(x, y)
                entities.add(bd)
                platforms.append(bd)
            if col == "P":
                pr = Princess(x, y)
                entities.add(pr)
                platforms.append(pr)
                animatedEntities.add(pr)

            x += platform_width
        y += platform_height
        x = 0

    total_level_width = len(level[0]) * platform_width
    total_level_height = len(level) * platform_height

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while running_game:
        timer.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT:
                 running_game = False

            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                running = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_LSHIFT:
                running = False

            if e.type == KEYDOWN and e.key == K_p:
                pause()

        display.fill(Color(background_color))
        animatedEntities.update()
        monsters.update(platforms)
        camera.update(hero)
        all_sprites.draw(display)
        all_sprites.update()
        hero.update(left, right, up, running, platforms)
        for e in entities:
            display.blit(e.image, camera.apply(e))
        pygame.display.update()


level = []
entities = pygame.sprite.Group()
animatedEntities = pygame.sprite.Group()
monsters = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
platforms = []
main()
quit()
