import pygame

class Bird:
    GRAVITY = 0.25
    BIRD_MOVEMENT = 0
    BIRD_IMG = None
    BIRD_RECT = None
    JUMP_HEIGHT = 6
    TIMING = 0

    def __init__(self, BIRD_IMG, BIRD_RECT):
        self.BIRD_IMG = BIRD_IMG
        self.BIRD_RECT = BIRD_RECT

    def animation(self):
        if self.TIMING % 30 == 0:
            self.BIRD_IMG = pygame.transform.scale2x(pygame.image.load('assets/bird3.png')).convert()
        elif self.TIMING % 20 == 0:
            self.BIRD_IMG = pygame.transform.scale2x(pygame.image.load('assets/bird2.png')).convert()
        elif self.TIMING % 10 == 0:
            self.BIRD_IMG = pygame.transform.scale2x(pygame.image.load('assets/bird1.png')).convert()
        self.TIMING += 1

    def move(self):
        self.BIRD_MOVEMENT += self.GRAVITY
        self.BIRD_RECT.centery += self.BIRD_MOVEMENT
        self.animation()

    def draw(self, screen):
        image, rect = self.rotate(self.BIRD_IMG, self.BIRD_RECT, self.BIRD_MOVEMENT * -3)
        screen.blit(image, rect)

    def collision(self, pipes):
        if self.BIRD_RECT.top <= -100 or self.BIRD_RECT.bottom >= 900:
            return False
        for pipe in pipes:
            if self.BIRD_RECT.colliderect(pipe.PIPE_TOP) or self.BIRD_RECT.colliderect(pipe.PIPE_BOTTOM):
                return False
        return True

    def rotate(self, image, rect, angle):
        new_image = pygame.transform.rotate(image, angle)
        rect = new_image.get_rect(center=rect.center)
        return new_image, rect

    def jump(self):
        self.BIRD_MOVEMENT = 0
        self.BIRD_MOVEMENT -= self.JUMP_HEIGHT
