import copy

from Pipe import Pipe


class Pipes:
    pipe_list = []
    gap = 175
    PIPE_IMG = None
    PIPE_IMG_REV = None

    def __init__(self, pipe_img, pipe_img_rev):
        self.pipe_list = []
        self.PIPE_IMG = pipe_img
        self.PIPE_IMG_REV = pipe_img_rev
        self.add()

    def add(self):
        self.pipe_list.append(Pipe(self.PIPE_IMG, self.PIPE_IMG_REV))

    def move(self, screen):
        for pipe in self.pipe_list:
            pipe.PIPE_TOP.centerx -= 5
            pipe.PIPE_BOTTOM.centerx -= 5
        self.draw(screen)

    def draw(self, screen):
        for pipe in self.pipe_list:
            screen.blit(self.PIPE_IMG_REV, pipe.PIPE_TOP)
            screen.blit(self.PIPE_IMG, pipe.PIPE_BOTTOM)

    def remove_pipe(self):
        pipes_new = []
        for i in range(len(self.pipe_list)):
            if self.pipe_list[i].PIPE_BOTTOM.centerx > -50:
                pipes_new.append(self.pipe_list[i])
        self.pipe_list = copy.deepcopy(pipes_new)
