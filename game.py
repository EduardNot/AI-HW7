# ORIGINAL IMAGES FROM https://github.com/samuelcust/flappy-bird-assets
# BASED ON https://www.youtube.com/watch?v=UZg49z76cLw

import pygame
import sys
import random
import copy

WIN_WIDTH = 575
WIN_HEIGHT = 800


class Pipes:
    pipe_list = []
    gap = 225

    def add(self):
        height = random.randint(300, 625)
        pipe_bottom = PIPE_IMG.get_rect(midtop=(700, height))
        pipe_top = PIPE_IMG.get_rect(midbottom=(700, height - self.gap))
        self.pipe_list.append((pipe_bottom, pipe_top))

    def move(self):
        for pipe in self.pipe_list:
            pipe[0].centerx -= 5
            pipe[1].centerx -= 5
        self.draw()

    def draw(self):
        for pipe in self.pipe_list:
            screen.blit(PIPE_IMG, pipe[0])
            screen.blit(PIPE_IMG_REV, pipe[1])

    def remove_pipe(self):
        pipes_new = []
        for i in range(len(self.pipe_list)):
            if self.pipe_list[i][0].centerx > -50:
                pipes_new.append(self.pipe_list[i])
        self.pipe_list = copy.deepcopy(pipes_new)


def draw_base():
    screen.blit(BASE_IMG, (BASE_X_POS, 700))
    screen.blit(BASE_IMG, (BASE_X_POS + 575, 700))


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    BIRD_IMG = pygame.transform.scale(pygame.image.load('assets/bird1.png'), (51, 36)).convert()
    # BIRD_IMG = pygame.transform.scale2x(pygame.image.load('assets/bird1.png')).convert()
    BG_IMG = pygame.transform.scale2x(pygame.image.load('assets/bg.png')).convert()
    BASE_IMG = pygame.transform.scale2x(pygame.image.load('assets/base.png')).convert()
    BIRD_RECT = BIRD_IMG.get_rect(center=(100, 325))
    PIPE_IMG = pygame.transform.scale2x(pygame.image.load('assets/pipe.png')).convert()
    PIPE_IMG_REV = pygame.transform.flip(PIPE_IMG, False, True).convert()

    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 1200)
    pipes = Pipes()

    GRAVITY = 0.25
    BIRD_MOVEMENT = 0
    BASE_X_POS = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    BIRD_MOVEMENT = 0
                    BIRD_MOVEMENT -= 8
            if event.type == SPAWNPIPE:
                pipes.add()

        screen.blit(BG_IMG, (0, 0))

        BIRD_MOVEMENT += GRAVITY
        BIRD_RECT.centery += BIRD_MOVEMENT
        screen.blit(BIRD_IMG, BIRD_RECT)

        pipes.move()
        pipes.remove_pipe()

        BASE_X_POS -= 1
        draw_base()
        if BASE_X_POS <= -575:
            BASE_X_POS = 0

        pygame.display.update()
        clock.tick(120)
