import random


class Pipe:
    gap = 175
    PIPE_TOP = None
    PIPE_BOTTOM = None
    passed = False
    height = None

    def __init__(self, img, img_rev):
        self.height = random.randint(300, 625)
        self.PIPE_BOTTOM = img.get_rect(midtop=(700, self.height))
        self.PIPE_TOP = img_rev.get_rect(midbottom=(700, self.height - self.gap))
