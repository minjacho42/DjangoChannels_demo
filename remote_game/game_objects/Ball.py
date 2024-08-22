class Ball:
    ball_speed = 8
    ball_speed_max = 10
    vInit = 4
    em = 0.03
    cof = 0.3
    def __init__(self, x=0, y=0, radius=15):
        self.x = x
        self.y = y
        self.dx = -Ball.ball_speed
        self.dy = 0
        self.radius = radius

    def reset(self, x, y, direction):
        self.x = x
        self.y = y
        if direction == 'L':
            self.dx = -Ball.ball_speed
        else:
            self.dx = Ball.ball_speed
        self.dy = 0