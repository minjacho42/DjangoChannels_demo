class Paddle:
    vInit = 6
    em = 0.03
    cof = 0.3
    def __init__(self, x=0, y=0, width=10, height=100):
        self.x = x
        self.y = y
        self.dy = 0
        self.accel = 0.15
        self.width = width
        self.height = height

    def move(self, screen_height):
        if 0 <= self.y + self.dy <= screen_height - self.height:
            self.y += self.dy