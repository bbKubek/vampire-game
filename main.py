import pygame
import random
import sys
import os
import time
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

icon = pygame.image.load("images/icon.png")
pygame.display.set_caption('Vampire game')
pygame.display.set_icon(icon)

W, H = 1920, 1080
HW, HH = W / 16, H / 2
AREA = W * H

win = pygame.display.set_mode((W, H))
bg = pygame.image.load("images/background.png").convert()

invs = (0, 0, 0, 0)

score = 0


class player(object):
    # ANIMACJE POSTACI
    walkRight = [pygame.image.load("images/vampire/runR1.png"), pygame.image.load("images/vampire/runR2.png"),
                 pygame.image.load("images/vampire/runR3.png")]
    walkLeft = [pygame.image.load("images/vampire/runL1.png"), pygame.image.load("images/vampire/runL2.png"),
                pygame.image.load("images/vampire/runL3.png")]
    from_bat_to_human = [pygame.image.load("images/vampire/from_bat_to_human1.png"),
                         pygame.image.load("images/vampire/from_bat_to_human2.png"),
                         pygame.image.load("images/vampire/from_bat_to_human3.png"),
                         pygame.image.load("images/vampire/from_bat_to_human4.png"),
                         pygame.image.load("images/vampire/from_bat_to_human5.png"),
                         pygame.image.load("images/vampire/from_bat_to_human6.png"),
                         pygame.image.load("images/vampire/from_bat_to_human7.png"),
                         pygame.image.load("images/vampire/from_bat_to_human8.png"),
                         pygame.image.load("images/vampire/from_bat_to_human9.png"),
                         pygame.image.load("images/vampire/from_bat_to_human10.png")]
    from_human_to_bat = [pygame.image.load("images/vampire/from_bat_to_human10.png"),
                         pygame.image.load("images/vampire/from_bat_to_human9.png"),
                         pygame.image.load("images/vampire/from_bat_to_human8.png"),
                         pygame.image.load("images/vampire/from_bat_to_human7.png"),
                         pygame.image.load("images/vampire/from_bat_to_human6.png"),
                         pygame.image.load("images/vampire/from_bat_to_human5.png"),
                         pygame.image.load("images/vampire/from_bat_to_human4.png"),
                         pygame.image.load("images/vampire/from_bat_to_human3.png"),
                         pygame.image.load("images/vampire/from_bat_to_human2.png"),
                         pygame.image.load("images/vampire/from_bat_to_human1.png")]
    dead = [
        pygame.image.load("images/vampire/death1.png"),
        pygame.image.load("images/vampire/death2.png"),
        pygame.image.load("images/vampire/death3.png"),
        pygame.image.load("images/vampire/death4.png"),
        pygame.image.load("images/vampire/death5.png"),
        pygame.image.load("images/vampire/death6.png"),
        pygame.image.load("images/vampire/death7.png"),
        pygame.image.load("images/vampire/death8.png"),
        pygame.image.load("images/vampire/death9.png"),
        pygame.image.load("images/vampire/death10.png")]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.right = False
        self.left = False
        self.is_dead = False
        self.is_moving = True
        self.walkCount = 0
        self.deadCount = 0
        self.vel = 5  # prędkość bohatera
        self.attack_frame = 0
        self.hitbox = (self.x + 45, self.y + 49, self.width - 40, self.height - 10)
        self.bullets = []
        self.cooldown_count = 0

    def move(self):
        # PLAYER MOVEMENT
        if self.is_moving:
            if keys[
                pygame.K_LEFT] and self.x > -125 + self.width - self.vel:  # postać nie może wychodzić poza ekran z lewej strony
                self.x -= self.vel
                self.left = True
                self.right = False
            elif keys[
                pygame.K_RIGHT] and vampire.x < 900 - self.width + self.vel:  # postać nie może wychodzić poza ekran z prawej strony
                self.x += self.vel
                self.left = False
                self.right = True
            else:
                self.right = True
                self.left = False  # w pozycji defaultowej obraca się w prawo
                # vampire.walkCount = 0  # kończy animacje
            if keys[
                pygame.K_UP] and vampire.y > 680 + self.height - self.vel:  # postać nie może wychodzić poza ekran z góry
                self.y -= self.vel
                self.right = True
            if keys[
                pygame.K_DOWN] and vampire.y < 1040 - self.height - self.vel:  # postać nie może wychodzić poza ekran z dołu
                self.y += self.vel
                self.right = True

    def shoot(self):
        self.punch()
        self.hit()
        self.cooldown()
        if self.attack_frame + 1 >= 50:
            self.attack_frame = 0
        if keys[pygame.K_SPACE] and self.cooldown_count == 0:
            bullet = Bullet(self.x, self.y)
            self.bullets.append(bullet)
            self.cooldown_count = 1
        for bullet in self.bullets:
            bullet.move()
            if bullet.range():
                self.bullets.remove(bullet)
        self.attack_frame += 1

    def punch(self):
        if keys[pygame.K_SPACE]:
            punch = [pygame.image.load("images/vampire/punch1.png"), pygame.image.load("images/vampire/punch2.png"),
                     pygame.image.load("images/vampire/punch3.png"), pygame.image.load("images/vampire/punch4.png"),
                     pygame.image.load("images/vampire/punch5.png")]
            win.blit(punch[self.attack_frame // 10], (self.x, self.y))

    def cooldown(self):
        if self.cooldown_count >= 50:  # prędkość strzelania
            self.cooldown_count = 0
        elif self.cooldown_count > 0:
            self.cooldown_count += 1

    def hit(self):
        global score
        for enemy in enemies:
            for bullet in self.bullets:
                if bullet.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and bullet.hitbox[1] + bullet.hitbox[3] > \
                        enemy.hitbox[1]:  # check y cords
                    if bullet.hitbox[0] + bullet.hitbox[2] > enemy.hitbox[0] and bullet.hitbox[0] < enemy.hitbox[0] + \
                            enemy.hitbox[2]:  # check x cords
                        enemies.remove(enemy)
                        self.bullets.remove(bullet)
                        # print("HIT")
                        score += 1

    def draw(self, win):
        self.hitbox = (self.x + 45, self.y + 49, self.width - 40, self.height - 10)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

        if self.deadCount + 1 >= 200:
            self.deadCount = 0

        if self.is_dead:
            win.blit(self.dead[self.deadCount // 20], (self.x, self.y))
            self.deadCount += 1
        else:
            if self.walkCount + 1 >= 18:
                self.walkCount = 0  # kontynuowanie animacji poprzez pętlę
            if self.left:  # rysowanie animacji postaci, która idzie w lewo
                win.blit(self.walkLeft[self.walkCount // 6], (self.x, self.y))
                self.walkCount += 1
            elif self.right:  # rysowanie animacji postaci, która idzie w prawo
                win.blit(self.walkRight[self.walkCount // 6], (self.x, self.y))
                self.walkCount += 1
            else:
                if self.right:
                    win.blit(self.walkRight[0], (self.x, self.y))
                else:
                    win.blit(self.walkLeft[0], (self.x, self.y))


class Enemy:
    # SKELETON MOVEMENT
    skeleton_walk = [pygame.image.load("images/skeleton/skeleton_run1.png"),
                     pygame.image.load("images/skeleton/skeleton_run2.png"),
                     pygame.image.load("images/skeleton/skeleton_run3.png"),
                     pygame.image.load("images/skeleton/skeleton_punch.png")]

    def __init__(self, x, y, width, height):
        self.transparent = (0, 0, 0, 0)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left = True
        self.attacking = False
        self.is_moving = True
        self.walkCount = 0
        self.passed_time = 0
        self.vel = 5
        self.hitbox = (self.x, self.y - 5, self.width, self.height)

    def draw(self, win):
        self.hitbox = (self.x + 50, self.y - 5, self.width - 20, self.height + 7)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # rysowanie obramowania hitboxów
        if self.walkCount + 1 >= 32:
            self.walkCount = 0  # kontynuowanie animacji poprzez pętlę
        if self.left:  # rysowanie animacji przeciwnika, która idzie w lewo
            win.blit(self.skeleton_walk[self.walkCount // 8], (self.x, self.y))
            self.walkCount += 1

    def last(self):
        if self.left:
            win.blit(self.skeleton_walk[3], (self.x, self.y))

    def collide(self, hitbox):
        if self.hitbox[1] < hitbox[1] + hitbox[3] and self.hitbox[1] + self.hitbox[3] > hitbox[1]:  # check y cords
            if self.hitbox[0] + self.hitbox[2] > hitbox[0] and self.hitbox[0] < hitbox[0] + hitbox[2]:  # check x cords
                return True
        return False


class Bullet:
    def __init__(self, x, y):
        self.x = x + 30
        self.y = y + 25
        self.hitbox = (self.x, self.y, 10, 10)

    def draw_bullet(self):
        self.hitbox = (self.x + 50, self.y + 65, 30, 20)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # rysowanie obramowania hitboxów
        fireball = pygame.image.load("images/vampire/fireball.png")
        win.blit(fireball, (self.x + 50, self.y + 70))

    def move(self):
        self.x += 15

    def range(self):
        return not (0 <= self.x <= vampire.x + 400)


def redrawWindow():
    vampire.draw(win)
    vampire.move()
    vampire.shoot()
    for bullet in vampire.bullets:
        bullet.draw_bullet()

    for enemy in enemies:
        enemy.draw(win)

    font = pygame.font.SysFont('comicsans', 50)
    text = font.render("Score: " + str(score), False, (0, 0, 0))
    win.blit(text, (10, 10))


enemies = []
vampire = player(200, 850, 90, 90)  # spawn X, spawn y, player width, player height


def text_objects(text, font):  # objekt tekstu
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, ic, ac, action=None):  # objekt przycisku
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(win, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(win, ic, (x, y, w, h))
    smallText = pygame.font.SysFont("comicsans", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    win.blit(textSurf, textRect)


def mainMenu():  # main menu
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quitGame()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_loop()

        win.blit(pygame.image.load("images/main_menu.jpg"), (0, 0))

        largeFont = pygame.font.SysFont('comicsans', 80)  # creates a font object
        currentScore = largeFont.render('Vampire Game ', True, (0, 0, 0))
        win.blit(currentScore, (W / 2 - 280, H / 2 - 300))

        button("START", 880, 450, 100, 50, (255, 0, 0), (200, 0, 0), main_loop)
        button("Quit", 880, 550, 100, 50, (255, 0, 0), (200, 0, 0), quitGame)

        pygame.display.update()


def main_loop():  # główna pętla gry
    global circlePosX, playerPosY, playerVelocityX, fallSpeed, pic_time, current_time, keys, FPS
    bgWidth, bgHeight = bg.get_rect().size

    stageWidth = bgWidth * 100
    stagePosX = 0

    startScrollingPosX = HW

    circleRadius = 25
    circlePosX = circleRadius

    playerPosX = circleRadius
    playerPosY = 0
    playerVelocityX = 0

    pause = 0
    fallSpeed = 0

    pygame.time.set_timer(USEREVENT + 1, 1000)  # randomowy czas w jakich pojawiają się przeciwnicy
    pygame.time.set_timer(USEREVENT + 2, 500)  # co pół sekundy zszybszaj prędkość gry
    pic_time = 0
    FPS = 60
    run = True
    while run:
        if pause > 0:
            pause += 1
        if pause > 199:  # długość trwania gry przed wyświetleniem end screenu
            endScreen()

        for enemy in enemies:  # jeżeli szkielet dotknie gracza, gracz przegrywa
            if enemy.is_moving:
                enemy.x -= 6  # prędkość przeciwnika
            if enemy.x < enemy.width * -2:  # gdy przeciwnik dotrze do końca przegyrwa grę
                enemies.remove(enemy)  # szkielet znika
                endScreen()
                if pause > 199:  # długość trwania gry przed wyświetleniem end screenu
                    endScreen()
                # print("DEAD")
            if enemy.collide(vampire.hitbox):
                vampire.is_dead = True
                vampire.is_moving = False
                for enemy in enemies:
                    enemy.is_moving = False
                if pause == 0:  # Sprawdzanie czy postać została już zabita, jeżeli tak nie kontynuuj animacji
                    fallSpeed = FPS
                    pause = 1
                # print("DEAD")

        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():  # interpetowanie eventów przez grę
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    mainMenu()
                    run = False

            if event.type == USEREVENT + 1:  # pojawianie przeciwników na drodze
                r = random.randrange(0, 2)  # randomizacja pojawiania się przeciwników
                if r == 0:
                    enemy = Enemy(1920, 830, 90, 90)
                    enemies.append(enemy)
                    # print("UP")
                else:
                    enemy = Enemy(1920, 970, 90, 90)
                    enemies.append(enemy)
                    # print("DOWN")
            if event.type == USEREVENT + 2:  # co pół sekundy zszybszaj prędkość gry
                FPS += 1

        keys = pygame.key.get_pressed()

        # poruszanie się bg wraz z postacią
        if vampire.is_moving:
            playerVelocityX = 5  # prędkość z jaką porusza się ekran/kółko
            playerPosX += playerVelocityX  # automatycznie poruszanie się kółka
        else:
            playerVelocityX = 0

        # if playerPosX < circleRadius:
        #     playerPosX = circleRadius
        if playerPosX < startScrollingPosX:  # scrollowanie bg wraz z postacią
            circlePosX = playerPosX
        elif playerPosX > stageWidth - startScrollingPosX:
            circlePosX = playerPosX - stageWidth + W
        else:
            circlePosX = startScrollingPosX
            stagePosX += -playerVelocityX  # poruszanie się ekranu wraz z prędkością kuli

        rel_x = stagePosX % bgWidth  # scrollowanie bg wraz z postacią
        win.blit(bg, (rel_x - bgWidth, 0))  # nakładanie drugiego obrazu na pierwszy
        if rel_x < W:
            win.blit(bg, (rel_x, 0))  # rysowanie przesuwającego się bg

        clock.tick(FPS)
        redrawWindow()
        pygame.display.update()
        pygame.display.flip()


def endScreen():
    global pause, score, FPS, enemies
    pause = 0
    FPS = 60
    enemies = []

    # another game loop
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE or K_SPACE or MOUSEBUTTONDOWN:
                    run = False
                    vampire.is_dead = False
                    vampire.x, vampire.y = 200, 850
                    vampire.is_moving = True
                    for enemy in enemies:
                        enemy.is_moving = True

        win.blit(bg, (0, 0))
        largeFont = pygame.font.SysFont('comicsans', 80)  # creates a font object
        currentScore = largeFont.render('Score: ' + str(score), True, (0, 0, 0))
        died = largeFont.render('YOU DIED ', True, (255, 0, 0))
        win.blit(currentScore, (W / 2 - 200, H / 2 - 100))
        win.blit(died, (W / 2 - 240, H / 2 - 200))
        pygame.display.update()

    score = 0
    main_loop()


def quitGame():
    pygame.quit()
    quit()


mainMenu()
main_loop()
quitGame()
