class Bird:

    GRAVITY = 0.25
    BIRD_MOVEMENT = 12
    BIRD_IMG = None
    BIRD_RECT = None

    def __init__(self, BIRD_IMG, BIRD_RECT):
        self.BIRD_IMG = BIRD_IMG
        self.BIRD_RECT = BIRD_RECT

    def move(self, screen):
        self.BIRD_MOVEMENT += self.GRAVITY
        self.BIRD_RECT.centery += self.BIRD_MOVEMENT
        screen.blit(self.BIRD_IMG, self.BIRD_RECT)

    def collision(self, pipes):
        if self.BIRD_RECT.centery > 670:
            self.BIRD_RECT.centery = 670
            return True
        for pipe in pipes:
            if self.BIRD_RECT.colliderect(pipe[0]) or self.BIRD_RECT.colliderect(pipe[1]):
                print("GG")
                return True
        return False

    def jump(self):
        self.BIRD_MOVEMENT = 0
        self.BIRD_MOVEMENT -= 5
