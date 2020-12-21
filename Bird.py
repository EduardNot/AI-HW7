class Bird:

    GRAVITY = 0.25
    BIRD_MOVEMENT = 0
    BIRD_IMG = None
    BIRD_RECT = None

    def __init__(self, BIRD_IMG, BIRD_RECT):
        self.BIRD_IMG = BIRD_IMG
        self.BIRD_RECT = BIRD_RECT

    def move(self, screen):
        self.BIRD_MOVEMENT += self.GRAVITY
        self.BIRD_RECT.centery += self.BIRD_MOVEMENT
        screen.blit(self.BIRD_IMG, self.BIRD_RECT)

    def collision(self):
        if self.BIRD_RECT.centery > 670:
            self.BIRD_RECT.centery = 670
            self.GRAVITY = 0
