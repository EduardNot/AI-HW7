class Base:
    BASE_X_POS = 0
    BASE_IMG = None

    def __init__(self, img):
        self.BASE_IMG = img

    def draw(self, screen):
        screen.blit(self.BASE_IMG, (self.BASE_X_POS, 700))
        screen.blit(self.BASE_IMG, (self.BASE_X_POS + 575, 700))

    def move(self, screen):
        self.BASE_X_POS -= 1
        self.draw(screen)
        if self.BASE_X_POS <= -575:
            self.BASE_X_POS = 0
