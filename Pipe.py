import random


class Pipe:
    gap = 175
    PIPE_TOP = None
    PIPE_BOTTOM = None
    passed = False

    def __init__(self, img, img_rev):
        height = random.randint(300, 625)
        self.PIPE_BOTTOM = img.get_rect(midtop=(700, height))
        self.PIPE_TOP = img_rev.get_rect(midbottom=(700, height - self.gap))
