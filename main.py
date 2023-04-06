import pygame
from random import randint

pygame.init()

playerAnimation = [pygame.image.load('Assets\\R0.png'), pygame.image.load('Assets\\R1.png'),
                   pygame.image.load('Assets\\R2.png'),
                   pygame.image.load('Assets\\R3.png'), pygame.image.load('Assets\\R4.png'),
                   pygame.image.load('Assets\\R5.png')]
playerSliding = [pygame.image.load('Assets\\C00.png'), pygame.image.load('Assets\\C01.png'),
                 pygame.image.load('Assets\\C02.png'),
                 pygame.image.load('Assets\\C03.png'), pygame.image.load('Assets\\C04.png'),
                 pygame.image.load('Assets\\C05.png'),
                 pygame.image.load('Assets\\C06.png'), pygame.image.load('Assets\\C07.png'),
                 pygame.image.load('Assets\\C08.png'),
                 pygame.image.load('Assets\\C09.png')]
SwingAnimation = [pygame.image.load('Assets\\S0.png'), pygame.image.load('Assets\\S1.png'),
                  pygame.image.load('Assets\\S2.png'),
                  pygame.image.load('Assets\\S3.png'), pygame.image.load('Assets\\S4.png'),
                  pygame.image.load('Assets\\S5.png')]
dragonAni = [pygame.image.load('Assets\\dragon0.png'), pygame.image.load('Assets\\dragon1.png'),
             pygame.image.load('Assets\\dragon2.png'),
             pygame.image.load('Assets\\dragon3.png')]

window_icon = pygame.image.load('Assets\\Icon.png')
bg = pygame.image.load('Assets\\bg0.png')
fireball = [pygame.image.load('Assets\\fireball0.png'), pygame.image.load('Assets\\fireball1.png'),
            pygame.image.load('Assets\\fireball2.png'), pygame.image.load('Assets\\fireball3.png')]
hearts = [pygame.image.load('Assets\\heart0.png'), pygame.image.load('Assets\\dedhrt0.png')]
screenwidth = 700
screenheight = 256
window = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption('Beta Game 2.0')
pygame.display.set_icon(window_icon)
text = pygame.font.SysFont("Comic", 23)
fps = pygame.time.Clock()

textX = 10
textX2 = 100
textY = 10
latestY = 1
down = False
nextObstical = 0
time2create = 60
obstacles = []
bgX = 0
bgX2 = 700
boss_battle = False
direction = 1
nextY = 150


class Player:
    def __init__(self):
        self.width = 40
        self.height = 56
        self.jumping = False
        self.x = 70
        self.y = 150
        self.vel = 5
        self.walk_count = 0
        self.score = 0
        self.sliding = False
        self.high_score = 0
        self.crouchcount = 0
        self.canSwing = False
        self.isSwing = False
        self.swingCount = 0

    def create_hitbox(self):
        self.hitbox = pygame.Rect((self.x, self.y), (self.width, self.height))

    def draw(self, window):
        global direction
        if self.walk_count + 1 >= 15:
            self.walk_count = 0
        if self.crouchcount + 1 >= 15:
            self.crouchcount = 0
        if self.swingCount == 18:
            self.isSwing = False
            self.swingCount = 0
        if not self.sliding and not boss_battle:
            window.blit(playerAnimation[self.walk_count // 3], (self.x, self.y))
        elif boss_battle and not self.isSwing:
            window.blit(SwingAnimation[0], (self.x - 3, self.y))
        elif self.sliding:
            window.blit(playerSliding[self.crouchcount // 3], (self.x, self.y))
        if self.isSwing:
            window.blit(SwingAnimation[self.swingCount // 3], (self.x - 3, self.y))
            self.swingCount += 1

    def collide(self):
        global file, obstacles, direction
        self.vel = 5
        obstacles = []
        if self.score > self.high_score:
            with open("highscore.txt", 'w') as file:
                file.write(str(self.score))
        with open("highscore.txt") as file:
            self.high_score = int(file.read())
        self.score = 0
        self.walk_count = 0
        self.sliding = False
        self.jumping = False
        dragon.x = 900
        reset_values()


user = Player()


class Dragon:
    def __init__(self):
        self.x = 900
        self.y = 128
        self.health = 3
        self.collide = False
        self.flapcount = 0

    def draw(self):
        global latestY
        if self.flapcount + 1 >= 12:
            self.flapcount = 0
        window.blit(dragonAni[self.flapcount // 3], (self.x, self.y - 40))
        latestY = self.y


dragon = Dragon()


class obstical():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stage_num = 0

    def draw(self, window):
            global latestY
            if self.stage_num + 1 >= 12:
                self.stage_num = 0
            window.blit(fireball[self.stage_num // 3], (self.x, self.y))
            self.stage_num += 1
            latestY = self.y


def refreshwindow():
    window.blit(bg, (bgX, 0))
    window.blit(bg, (bgX2, 0))
    user.draw(window)
    show_score(1, textX, textY)
    show_score(2, textX2, textY)
    dragon.draw()
    for obstical in obstacles:
        obstical.draw(window)
    current_fps = text.render("Fps: " + cf, True, (0, 0, 0))
    window.blit(current_fps, (640, 10))
    show_hearts(dragon.x, dragon.y - 60)
    pygame.display.update()


def jump():
    global down
    if user.y > 50 and not down:
        user.y -= user.vel * 1.3
    else:
        down = True
        if user.y < 150:
            user.y += user.vel * 1.3
        else:
            user.jumping = False
            down = False


def createObstical():
    global nextY
    if nextObstical % time2create == 0:
        obstacles.append(obstical(dragon.x - 14, nextY))
        nextY = randint(130, 190)


def show_hearts(x, y):
    if boss_battle:
        ogX = x
        for i in range(0, 3):
            if i <= dragon.health - 1:
                window.blit(hearts[0], (x, y))
            else:
                window.blit(hearts[1], (x, y))
            x += 30
        x = ogX


def show_score(scoreMode, x, y):
    if scoreMode == 1:
        score = text.render("Score: " + str(user.score), True, (0, 0, 0))
        window.blit(score, (x, y))
    else:
        score1 = text.render("High Score: " + str(user.high_score), True, (0, 0, 0))
        window.blit(score1, (x, y))


def reset_values():
    global time2create, latestY, bgX, bgX2, boss_battle, direction
    user.y = 150
    time2create = 60
    latestY = 1
    bgX = 0
    bgX2 = 700
    dragon.x = 900
    boss_battle = False
    user.isSwing = False
    user.swingCount = 0
    direction = 1


with open("highscore.txt") as file:
    user.high_score = int(file.read())

running = True

if __name__ == '__main__':
    while running:
        fps.tick(30)
        cf = str(int(fps.get_fps()))

        user.create_hitbox()
        dragonHitbox = pygame.Rect((dragon.x, latestY), (dragonAni[0].get_width(), dragonAni[0].get_width()))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.QUIT

            if user.sliding:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        user.sliding = False
                        user.y = 150

            if not user.isSwing and boss_battle:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    user.isSwing = True

        keys_pressed = pygame.key.get_pressed()

        if not user.jumping:
            if keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
                user.jumping = True

        if not user.sliding:
            if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
                user.sliding = True
                user.jumping = False
                user.y = 170

        if user.jumping:
            user.sliding = False
            jump()

        for obstacle in obstacles:
            obstacleRect = pygame.Rect((obstacle.x, obstacle.y), (14, 6))
            if obstacle.x > 700 and direction == -1:
                obstacles.pop(obstacles.index(obstacle))
            if obstacle.x > 0:
                obstacle.x -= user.vel * direction
            else:
                obstacles.pop(obstacles.index(obstacle))

            collide = pygame.Rect.colliderect(obstacleRect, user.hitbox)
            dragCollide = pygame.Rect.colliderect(dragonHitbox, obstacleRect)
            if dragCollide:
                dragon.health -= 1
                direction = 1
                obstacles.pop(obstacles.index(obstacle))
                if dragon.health <= 0:
                    dragon.x = 900
                    boss_battle = False
                    direction = 1
                    time2create = oldt2t
            if collide and not user.isSwing:
                user.collide()
            if collide and user.isSwing:
                direction = -1

        if time2create > 0:
            try:
                if nextObstical % 900 == 0:
                    user.vel += 2
                    if not boss_battle:
                        time2create -= 2
            except ZeroDivisionError:
                time2create = 60
        nextObstical += 1
        user.score += 1
        if user.score == 10000:
            textX2 += 5
        if not boss_battle:
            bgX -= user.vel // 1.5
            bgX2 -= user.vel // 1.5
            if bgX < screenwidth * -1:
                bgX = screenwidth
            if bgX2 < screenwidth * -1:
                bgX2 = screenwidth
            dragon.x -= .2
            user.walk_count += 1
            user.crouchcount += 1
        if user.score % 2500 == 0 and user.score != 0:
            boss_battle = True
            user.walk_count = 0
            user.crouchcount = 0
            user.canSwing = True
            dragon.health = 3
            oldt2t = time2create
            time2create = 80
        if dragon.y != nextY:
            if dragon.y < nextY:
                dragon.y += 1
            elif dragon.y > nextY:
                dragon.y -= 1
        else:
            createObstical()
        dragon.flapcount += 1
        refreshwindow()
