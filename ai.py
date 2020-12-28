# ORIGINAL IMAGES FROM https://github.com/samuelcust/flappy-bird-assets
# GAME BASED ON https://www.youtube.com/watch?v=UZg49z76cLw
# AI BASE ON https://www.youtube.com/watch?v=MPFWsRjDmnU&list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2&index=5
import os
import sys

import neat
import pygame

from Bird import Bird
from Pipe import Pipe
from Base import Base

WIN_WIDTH = 575
WIN_HEIGHT = 800
high_score = 0

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
STAT_FONT = pygame.font.SysFont("comicsans", 50)


def print_alive(birds):
    alive_surface = STAT_FONT.render(f"Alive: {birds}", True, (255, 255, 255))
    alive_rect = alive_surface.get_rect(center=(70, 20))
    screen.blit(alive_surface, alive_rect)


def score_display(score, high_score):
    score_surface = STAT_FONT.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(485, 45))
    screen.blit(score_surface, score_rect)

    high_score_surface = STAT_FONT.render(f"High Score: {high_score}", True, (255, 255, 255))
    high_score_rect = high_score_surface.get_rect(center=(440, 20))
    screen.blit(high_score_surface, high_score_rect)


def update_score(pipes, bird):
    for pipe in pipes:
        if not pipe.passed and pipe.PIPE_BOTTOM.centerx < bird.BIRD_RECT.centerx:
            pipe.passed = True
            return True
    return False


def remove_pipe(pipes):
    pipes_new = []
    for i in range(len(pipes)):
        if pipes[i].PIPE_BOTTOM.centerx > -50:
            pipes_new.append(pipes[i])
    return pipes_new


def add_pipe(pipes, bird):
    for pipe in pipes:
        if bird.BIRD_RECT.centerx + 100 > pipe.PIPE_BOTTOM.centerx and not pipe.next_pipe:
            pipe.next_pipe = True
            return True
    return False


def eval(genomes, config):
    global high_score

    birds = []
    nets = []
    genes = []
    for g_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        BIRD_RECT = BIRD_IMG.get_rect(center=(100, 325))
        birds.append(Bird(BIRD_IMG, BIRD_RECT))
        genes.append(genome)

    base = Base(BASE_IMG)
    pipes = [Pipe(PIPE_IMG, PIPE_IMG_REV)]
    score = 0

    game = True
    while game and len(birds) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(BG_IMG, (0, 0))

        pipe_idx = 0
        if len(birds) > 0:
            if len(pipes) > 1 and pipes[0].passed and birds[0].BIRD_RECT.centerx > pipes[0].PIPE_BOTTOM.topright[1]:
                pipe_idx = 1

        for i, bird in enumerate(birds):
            genes[i].fitness += 0.4
            bird.move()

            output = nets[i].activate((bird.BIRD_RECT.y,
                                       abs(bird.BIRD_RECT.y - pipes[pipe_idx].PIPE_TOP.bottom),
                                       abs(bird.BIRD_RECT.y - pipes[pipe_idx].PIPE_BOTTOM.top)))
            if output[0] > 0.5:
                bird.jump()

        passed_pipe = False
        for bird in birds:
            if not bird.collision(pipes):
                genes[birds.index(bird)].fitness -= 1
                nets.pop(birds.index(bird))
                genes.pop(birds.index(bird))
                birds.pop(birds.index(bird))
            if not passed_pipe:
                passed_pipe = update_score(pipes, bird)
            if add_pipe(pipes, bird):
                pipes.append(Pipe(PIPE_IMG, PIPE_IMG_REV))

        if passed_pipe:
            score += 1
            for g in genes:
                g.fitness += 5

        for bird in birds:
            bird.draw(screen)

        for pipe in pipes:
            pipe.move()
            pipe.draw(screen)

        print_alive(len(birds))
        score_display(score, high_score)

        pipes = remove_pipe(pipes)

        base.move(screen)

        pygame.display.update()
        clock.tick(100)
    if score > high_score:
        high_score = score


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_file)
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.StatisticsReporter())
    winner = pop.run(eval, 100)


if __name__ == '__main__':
    directory = os.path.dirname(__file__)
    config_path = os.path.join(directory, 'neat-config.txt')
    run(config_path)
