# ORIGINAL IMAGES FROM https://github.com/samuelcust/flappy-bird-assets
# BASED ON https://www.youtube.com/watch?v=UZg49z76cLw

import sys

import pygame

from Bird import Bird
from Pipes import Pipes
from Base import Base

WIN_WIDTH = 575
WIN_HEIGHT = 800
GAME_ACTIVE = True
score = 0


def draw_base():
    screen.blit(BASE_IMG, (BASE_X_POS, 700))
    screen.blit(BASE_IMG, (BASE_X_POS + 575, 700))


def score_display():
    score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(288, 100))
    screen.blit(score_surface, score_rect)


def update_score(pipes, bird, score):
    for pipe in pipes.pipe_list:
        if not pipe.passed and pipe.PIPE_BOTTOM.centerx < bird.BIRD_RECT.centerx:
            pipe.passed = True
            return score + 1
    return score


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    game_font = pygame.font.Font('04B_19.ttf', 40)

    # BIRD_IMG = pygame.transform.scale(pygame.image.load('assets/bird1.png'), (51, 36)).convert()
    BIRD_IMG = pygame.transform.scale2x(pygame.image.load('assets/bird1.png')).convert()
    BG_IMG = pygame.transform.scale2x(pygame.image.load('assets/bg.png')).convert()
    BASE_IMG = pygame.transform.scale2x(pygame.image.load('assets/base.png')).convert()
    BIRD_RECT = BIRD_IMG.get_rect(center=(100, 325))
    PIPE_IMG = pygame.transform.scale2x(pygame.image.load('assets/pipe.png')).convert()
    PIPE_IMG_REV = pygame.transform.flip(PIPE_IMG, False, True).convert()

    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 900)
    pipes = Pipes(PIPE_IMG, PIPE_IMG_REV)

    BASE_X_POS = 0

    bird = Bird(BIRD_IMG, BIRD_RECT)

    base = Base(BASE_IMG)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and GAME_ACTIVE:
                    bird.jump()
                if event.key == pygame.K_SPACE and GAME_ACTIVE == False:
                    GAME_ACTIVE = True
                    BIRD_RECT = BIRD_IMG.get_rect(center=(100, 325))
                    bird = Bird(BIRD_IMG, BIRD_RECT)
                    pipes.pipe_list.clear()
                    score = 0

            if event.type == SPAWNPIPE:
                pipes.add()

        screen.blit(BG_IMG, (0, 0))

        if GAME_ACTIVE:
            bird.move(screen)
            GAME_ACTIVE = bird.collision(pipes.pipe_list)

            pipes.move(screen)
            pipes.remove_pipe()

            score_display()
            score = update_score(pipes, bird, score)

        base.move(screen)

        pygame.display.update()
        clock.tick(100)
