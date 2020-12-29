import random


class Pipe:
    gap = 175
    PIPE_TOP = None
    PIPE_BOTTOM = None
    passed = False
    next_pipe = False
    height = None

    def __init__(self, img, img_rev):
        self.height = random.randint(300, 625)
        self.IMG = img
        self.IMG_REV = img_rev
        self.PIPE_BOTTOM = self.IMG.get_rect(midtop=(700, self.height))
        self.PIPE_TOP = self.IMG_REV.get_rect(midbottom=(700, self.height - self.gap))

    def move(self):
        self.PIPE_TOP.centerx -= 3
        self.PIPE_BOTTOM.centerx -= 3

    def draw(self, screen):
        screen.blit(self.IMG_REV, self.PIPE_TOP)
        screen.blit(self.IMG, self.PIPE_BOTTOM)
