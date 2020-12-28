# ORIGINAL IMAGES FROM https://github.com/samuelcust/flappy-bird-assets
# GAME BASED ON https://www.youtube.com/watch?v=UZg49z76cLw
# AI BASE ON https://www.youtube.com/watch?v=MPFWsRjDmnU&list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2&index=5

import sys

import pygame

from Bird import Bird
from Pipes import Pipes
from Base import Base

WIN_WIDTH = 575
WIN_HEIGHT = 800
GAME_ACTIVE = False
score = 0
high_score = 0


def score_display(game_over):
    if not game_over:
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

    high_score_surface = high_score_font.render('High score: ' + str(high_score), True, (255, 255, 255))
    high_score_rect = high_score_surface.get_rect(center=(288, 60))
    screen.blit(high_score_surface, high_score_rect)


def update_score():
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
    high_score_font = pygame.font.Font('04B_19.TTF', 18)

    # BIRD_IMG = pygame.transform.scale(pygame.image.load('assets/bird1.png'), (51, 36)).convert()
    BIRD_IMG = pygame.transform.scale2x(pygame.image.load('assets/bird1.png')).convert()
    BG_IMG = pygame.transform.scale2x(pygame.image.load('assets/bg.png')).convert()
    BASE_IMG = pygame.transform.scale2x(pygame.image.load('assets/base.png')).convert()
    BIRD_RECT = BIRD_IMG.get_rect(center=(100, 325))
    PIPE_IMG = pygame.transform.scale2x(pygame.image.load('assets/pipe.png')).convert()
    PIPE_IMG_REV = pygame.transform.flip(PIPE_IMG, False, True).convert()
    START_GAME_SUFACE = pygame.image.load('assets/message.png').convert_alpha()
    START_GAME_REC = START_GAME_SUFACE.get_rect(center=(288, 400))

    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 9000)
    pipes = Pipes(PIPE_IMG, PIPE_IMG_REV)

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
                if event.key == pygame.K_SPACE and GAME_ACTIVE is False:
                    GAME_ACTIVE = True
                    BIRD_RECT = BIRD_IMG.get_rect(center=(100, 325))
                    bird = Bird(BIRD_IMG, BIRD_RECT)
                    pipes.pipe_list.clear()
                    score = 0

            if event.type == SPAWNPIPE:
                pipes.add()

        screen.blit(BG_IMG, (0, 0))
        # if len(pipes.pipe_list) > 1:
        #     print("#####PAIR#####")
        #     print(pipes.pipe_list[1].PIPE_TOP.bottom)
        #     print(bird.BIRD_RECT.y)
        #     print(pipes.pipe_list[1].PIPE_BOTTOM.top)
        #     print(abs(pipes.pipe_list[1].PIPE_TOP.bottom - pipes.pipe_list[1].PIPE_BOTTOM.top))
        #     print("#####PAIR#####")

        if GAME_ACTIVE:
            bird.move()
            GAME_ACTIVE = bird.collision(pipes.pipe_list)

            pipes.move(screen)
            pipes.remove_pipe()

            score_display(False)
            score = update_score()
        else:
            screen.blit(START_GAME_SUFACE, START_GAME_REC)
            if score > high_score:
                high_score = score
            score_display(True)

        base.move(screen)
        bird.draw(screen)

        pygame.display.update()
        clock.tick(30)
