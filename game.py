# ORIGINAL IMAGES FROM https://github.com/samuelcust/flappy-bird-assets
# BASED ON https://www.youtube.com/watch?v=UZg49z76cLw

import pygame
import sys
import random

WIN_WIDTH = 575
WIN_HEIGHT = 800


def draw_base():
    screen.blit(BASE_IMG, (BASE_X_POS, 700))
    screen.blit(BASE_IMG, (BASE_X_POS + 575, 700))


def create_pipe():
    height = random.randint(300, 625)
    pipe_bottom = PIPE_IMG.get_rect(midtop=(700, height))
    pipe_top = PIPE_IMG.get_rect(midbottom=(700, height - 225))
    return tuple((pipe_bottom, pipe_top))


def move_pipe(pipes):
    for pipe in pipes:
        pipe[0].centerx -= 5
        pipe[1].centerx -= 5
    return pipes


def draw_pipe(pipes):
    for pipe in pipes:
        screen.blit(PIPE_IMG, pipe[0])
        screen.blit(PIPE_IMG_REV, pipe[1])


def remove_pipe(pipes):
    pipes_copy = pipes.copy()
    for i in range(len(pipes)):
        if pipes[i][0].centerx < -50:
            pipes_copy.pop(i)
    return pipes_copy


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
    pipe_list = []
    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 1200)

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
                print(len(pipe_list))
                pipe_list.append(create_pipe())

        screen.blit(BG_IMG, (0, 0))

        BIRD_MOVEMENT += GRAVITY
        BIRD_RECT.centery += BIRD_MOVEMENT
        screen.blit(BIRD_IMG, BIRD_RECT)

        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        pipe_list = remove_pipe(pipe_list)

        BASE_X_POS -= 1
        draw_base()
        if BASE_X_POS <= -575:
            BASE_X_POS = 0

        pygame.display.update()
        clock.tick(120)
