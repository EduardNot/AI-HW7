class Coin:

    COIN_IMG = None
    COIN_RECT = None
    is_Gotten = False

    def __init__(self, COIN_IMG, COIN_RECT):
        self.COIN_IMG = COIN_IMG
        self.COIN_RECT = COIN_RECT

    def move(self):
        self.COIN_RECT.centerx -= 3

    def draw(self, screen):
        screen.blit(self.COIN_IMG, self.COIN_RECT)
