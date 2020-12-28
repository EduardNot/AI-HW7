# ORIGINAL IMAGES FROM https://github.com/samuelcust/flappy-bird-assets
# GAME BASED ON https://www.youtube.com/watch?v=UZg49z76cLw
# AI BASE ON https://www.youtube.com/watch?v=MPFWsRjDmnU&list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2&index=5
import os
import sys

import neat
import pygame

from Bird import Bird
from Pipes import Pipes
from Base import Base

WIN_WIDTH = 575
WIN_HEIGHT = 800

pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

game_font = pygame.font.Font('04B_19.ttf', 40)

# BIRD_IMG = pygame.transform.scale(pygame.image.load('assets/bird1.png'), (51, 36)).convert()
BIRD_IMG = pygame.transform.scale2x(pygame.image.load('assets/bird1.png')).convert()
BG_IMG = pygame.transform.scale2x(pygame.image.load('assets/bg.png')).convert()
BASE_IMG = pygame.transform.scale2x(pygame.image.load('assets/base.png')).convert()
PIPE_IMG = pygame.transform.scale2x(pygame.image.load('assets/pipe.png')).convert()
PIPE_IMG_REV = pygame.transform.flip(PIPE_IMG, False, True).convert()
START_GAME_SUFACE = pygame.image.load('assets/message.png').convert_alpha()

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 900)


def score_display(score):
    score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(288, 100))
    screen.blit(score_surface, score_rect)


def update_score(pipes, bird):
    for pipe in pipes.pipe_list:
        if not pipe.passed and pipe.PIPE_BOTTOM.centerx < bird.BIRD_RECT.centerx:
            pipe.passed = True
            return True
    return False


def eval(genomes, config):
    BIRD_RECT = BIRD_IMG.get_rect(center=(100, 325))

    birds = []
    nets = []
    genes = []

    for g_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(BIRD_IMG, BIRD_RECT))
        genes.append(genome)

    base = Base(BASE_IMG)
    pipes = Pipes(PIPE_IMG, PIPE_IMG_REV)
    score = 0

    game = True
    while game and len(birds) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # if event.type == SPAWNPIPE:
            #     pipes.add()

        screen.blit(BG_IMG, (0, 0))
        score_display(score)

        pipe_idx = 0
        if len(birds) > 0:
            if len(pipes.pipe_list) > 1 and pipes.pipe_list[0].passed:
                pipe_idx = 1
        # for i, pipe in enumerate(pipes.pipe_list):
        #     if not pipe.passed:
        #         pipe_idx = i

        for i, bird in enumerate(birds):
            genes[i].fitness += 0.1
            bird.move()

            output = nets[i].activate((bird.BIRD_RECT.y,
                                       abs(bird.BIRD_RECT.y - pipes.pipe_list[pipe_idx].PIPE_TOP.bottom),
                                       abs(bird.BIRD_RECT.y - pipes.pipe_list[pipe_idx].PIPE_BOTTOM.top)))
            if output[0] > 0.5:
                bird.jump()

        passed_pipe = False
        for bird in birds:
            if bird.collision(pipes.pipe_list):
                genes[birds.index(bird)].fitness -= 1
                nets.pop(birds.index(bird))
                genes.pop(birds.index(bird))
                birds.pop(birds.index(bird))
            passed_pipe = update_score(pipes, bird)

        if passed_pipe:
            score += 1
            pipes.add()
            for g in genes:
                g.fitness += 5

        for bird in birds:
            bird.draw(screen)

        pipes.move(screen)
        pipes.remove_pipe()

        base.move(screen)

        pygame.display.update()
        clock.tick(30)


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_file)
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.StatisticsReporter())
    winner = pop.run(eval, 50)


if __name__ == '__main__':
    directory = os.path.dirname(__file__)
    config_path = os.path.join(directory, 'neat-config.txt')
    run(config_path)
