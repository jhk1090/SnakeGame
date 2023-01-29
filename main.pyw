from pygame.locals import *
import pygame
import random
from datetime import datetime
from datetime import timedelta
import os
import sys
import enum
import asset

this_path = os.path.dirname(sys.argv[0])

# 2. pygame 초기화
pygame.init()
pygame.mixer.init()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 기본 설정 (수정 금지)
size = [900, 900]
screen = pygame.display.set_mode(size)
# pygame.display.set_icon(pygame.image.load(asset.entity["poop"]))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

done = False
clock = pygame.time.Clock()
last_moved_time = datetime.now()
unoccupied = []
for i in range(30):
    for j in range(30):
        unoccupied.append((i, j))

KEY_DIRECTION = {
    pygame.K_UP: 'N',
    pygame.K_DOWN: 'S',
    pygame.K_LEFT: 'W',
    pygame.K_RIGHT: 'E',
}


def draw_block(screen, color, position):
    block = pygame.Rect((position[1] * 30, position[0] * 30),
                        (30, 30))
    pygame.draw.rect(screen, color, block)

class Snake:
    def __init__(self):
        self.positions = [(14, 2), (14, 1), (14, 0)]  # 뱀의 위치
        self.direction = ''
        self.status = ''
        self.score = 0

    def draw(self):
        for index, position in enumerate(self.positions):
            direction = ''
            if index == 0:
                block = pygame.image.load(asset.sprite["snake"]["head"])
                direction = self.status
            else:
                if index == len(self.positions) - 1:
                    x_diff = position[1] - self.positions[index - 1][1]
                    y_diff = position[0] - self.positions[index - 1][0]
                    if x_diff > 0:
                        direction = 'W'
                    elif x_diff < 0:
                        direction = 'E'
                    elif y_diff > 0:
                        direction = 'N'
                    elif y_diff < 0:
                        direction = 'S'
                    block = pygame.image.load(asset.sprite["snake"]["tail"])
                else:
                    x_diff = position[1] - self.positions[index - 1][1]
                    x_diff_aft = position[1] - self.positions[index + 1][1]
                    y_diff = position[0] - self.positions[index - 1][0]
                    y_diff_aft = position[0] - self.positions[index + 1][0]
                    if x_diff == x_diff_aft:
                        block = pygame.image.load(asset.sprite["snake"]["body"])
                        direction = 'N' # or 'S'
                    elif y_diff == y_diff_aft:
                        block = pygame.image.load(asset.sprite["snake"]["body"])
                        direction = 'W' # or 'E'
                    elif x_diff_aft == 0:
                        if x_diff == 1 and y_diff_aft == 1:
                            block = pygame.image.load(asset.sprite["snake"]["curve"])
                            direction = 'W'
                        elif x_diff == -1 and y_diff_aft == -1:
                            block = pygame.image.load(asset.sprite["snake"]["curve"])
                            direction = 'E'
                        elif x_diff == 1 and y_diff_aft == -1:
                            block = pygame.image.load(asset.sprite["snake"]["curve_west"])
                            direction = 'E'
                        elif x_diff == -1 and y_diff_aft == 1:
                            block = pygame.image.load(asset.sprite["snake"]["curve_west"])
                            direction = 'W'
                    elif y_diff_aft == 0:
                        if y_diff == 1 and x_diff_aft == -1:
                            block = pygame.image.load(asset.sprite["snake"]["curve"])
                            direction = 'N'
                        elif y_diff == -1 and x_diff_aft == 1:
                            block = pygame.image.load(asset.sprite["snake"]["curve"])
                            direction = 'S'
                        if y_diff == 1 and x_diff_aft == 1:
                            block = pygame.image.load(asset.sprite["snake"]["curve_west"])
                            direction = 'S'
                        elif y_diff == -1 and x_diff_aft == -1:
                            block = pygame.image.load(asset.sprite["snake"]["curve_west"])
                            direction = 'N'
            angle = 0
            if direction == 'N':
                angle = 90
            elif direction == 'S': 
                angle = 270
            elif direction == 'W':
                angle = 180
            elif direction == 'E':
                angle = 0
            block = pygame.transform.rotate(block, angle)
            screen.blit(block, (position[1] * 30, position[0] * 30))

    def move(self):
        global unoccupied
        head_position = self.positions[0]
        y, x = head_position
        unoccupied = [item for item in unoccupied if item not in self.positions]

        if self.direction == 'N':
            if self.status != 'S':
                self.positions = [(y - 1, x)] + self.positions[:-1]
                self.status = 'N'
            else:
                self.direction = 'S'
                self.move()
        elif self.direction == 'S':
            if self.status != 'N':
                self.positions = [(y + 1, x)] + self.positions[:-1]
                self.status = 'S'
            else:
                self.direction = 'N'
                self.move()
        elif self.direction == 'W':
            if self.status != 'E':
                self.positions = [(y, x - 1)] + self.positions[:-1]
                self.status = 'W'
            else:
                self.direction = 'E'
                self.move()
        elif self.direction == 'E':
            if self.status != 'W':
                self.positions = [(y, x + 1)] + self.positions[:-1]
                self.status = 'E'
            else:
                self.direction = 'W'
                self.move()

    def grow(self):
        tail_position = self.positions[-1]
        y, x = tail_position

        x_diff = self.positions[-1][1] - self.positions[-2][1]
        y_diff = self.positions[-1][0] - self.positions[-2][0]

        if x_diff < 0 and y_diff == 0:
            self.positions.append((y, x - 1))
        elif x_diff > 0 and y_diff == 0:
            self.positions.append((y, x + 1))
        elif y_diff < 0 and x_diff == 0:
            self.positions.append((y - 1, x))
        elif y_diff > 0 and x_diff == 0:
            self.positions.append((y + 1, x))

        self.score += 1
        print(self.score)

    def reset(self):
        self.positions = [(14, 2), (14, 1), (14, 0)]  # 뱀의 위치
        self.direction = ''
        self.status = ''
        self.score = 0
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((0, 0), (0, 0)))


class Apple:
    def __init__(self, position=(5, 5)):
        self.position = position

    def draw(self):
        block = pygame.image.load(asset.sprite["apple"])
        screen.blit(block, (self.position[1] * 30, self.position[0] * 30))

    def reset(self):
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((0, 0), (0, 0)))


class SceneEnum(enum.Enum):
    LOBBY = 0
    START = 1
    END = 2

# 4. pygame 무한루프


class Game:
    def __init__(self):
        global done, last_moved_time
        # 게임 시작 시, 뱀과 사과를 초기화
        self.snakeSprite = Snake()
        self.appleSprite = Apple()
        self.wallhitSound = pygame.mixer.Sound(asset.sound["sfx"]["hurt"])
        self.bgmusicSound = pygame.mixer.Sound(asset.sound["background"]["Start"])
        self.applebiteSound = []
        for i in asset.sound["sfx"]["apple_bite"]:
            self.applebiteSound.append(pygame.mixer.Sound(i))
        self.bgmusicSound.set_volume(0.2)
        self.wallhitSound.set_volume(0.2)
        for sound in self.applebiteSound:
            sound.set_volume(0.6)

        self.scene = [SceneEnum.LOBBY, SceneEnum.START, SceneEnum.END]
        self.sceneInit = [False, False, False]
        self.sceneNumber = 0

    def moveToScene(self, enum: SceneEnum):
        """
        장면을 이동합니다.
        """
        self.sceneNumber = enum.value

    def isSelectedScene(self, scene: SceneEnum):
        """
        인자로 받은 장면이 현재 장면인지 확인합니다.
        """
        return self.scene[self.sceneNumber] == scene

    def sceneLobby(self):
        ### 처음에만 실행 ###
        if not self.sceneInit[self.sceneNumber]:
            self.sceneInit = [False, False, False]
            self.sceneInit[self.sceneNumber] = True
        ### 처음에만 실행 ###

        background = pygame.image.load(asset.background["Lobby"])
        screen.blit(background, (0, 0))

    def sceneStart(self):
        global done, last_moved_time, unoccupied

        ### 처음에만 실행 ###
        if not self.sceneInit[self.sceneNumber]:
            self.bgmusicSound.play()
            self.sceneInit = [False, False, False]
            self.sceneInit[self.sceneNumber] = True
        ### 처음에만 실행 ###

        background = pygame.image.load(asset.background["Start"])
        screen.blit(background, (0, 0))

        if timedelta(seconds=0.1) <= datetime.now() - last_moved_time:
            self.snakeSprite.move()
            last_moved_time = datetime.now()

        if self.snakeSprite.positions[0] == self.appleSprite.position:
            self.applebiteSound[random.randint(0, 2)].play()
            self.snakeSprite.grow()
            self.appleSprite.position = unoccupied[random.randint(0, len(unoccupied) - 1)]

        if self.snakeSprite.positions[0] in self.snakeSprite.positions[1:]:
            self.moveToScene(SceneEnum.END)

        if self.snakeSprite.positions[0][1] > 29 or self.snakeSprite.positions[0][1] < 0 or self.snakeSprite.positions[0][0] < 0 or self.snakeSprite.positions[0][0] > 29:
            self.moveToScene(SceneEnum.END)

        self.snakeSprite.draw()
        self.appleSprite.draw()

    def sceneEnd(self):
        ### 처음에만 실행 ###
        if not self.sceneInit[self.sceneNumber]:
            self.snakeSprite.reset()
            self.appleSprite.reset()
            self.bgmusicSound.stop()
            self.wallhitSound.play()
            self.sceneInit = [False, False, False]
            self.sceneInit[self.sceneNumber] = True
        ### 처음에만 실행 ###

        background = pygame.image.load(asset.background["End"])
        screen.blit(background, (0, 0))

    def run(self):
        global done, last_moved_time
        while not done:
            clock.tick(240)
            # screen.fill((220, 201, 29))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if self.isSelectedScene(SceneEnum.START):
                        if event.key in KEY_DIRECTION:
                            self.snakeSprite.direction = KEY_DIRECTION[event.key]
                    if self.isSelectedScene(SceneEnum.LOBBY):
                        if event.key == pygame.K_SPACE:
                            self.moveToScene(SceneEnum.START)
                    if self.isSelectedScene(SceneEnum.END):
                        if event.key == pygame.K_SPACE:
                            self.moveToScene(SceneEnum.LOBBY)

            if self.isSelectedScene(SceneEnum.LOBBY):
                self.sceneLobby()
            elif self.isSelectedScene(SceneEnum.START):
                self.sceneStart()
            elif self.isSelectedScene(SceneEnum.END):
                self.sceneEnd()

            pygame.display.update()


game = Game()
game.run()

pygame.quit()
