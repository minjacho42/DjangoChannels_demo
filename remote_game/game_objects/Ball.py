
class Ball:
    ball_speed = 5
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

    def move(self, height, left_paddle, right_paddle):
        self.x += self.dx
        self.y += self.dy
        if self.y + self.dy < self.radius or self.y + self.dy > height - self.radius:
            self.dy *= -1
        left_paddle.check_collision(self, 'L')
        right_paddle.check_collision(self, 'R')

    def handle_collision(self, direction, paddle_dy):
        if direction not in ['L', 'R']:
            return
        new_dy = Ball.cof * paddle_dy + self.dy
        if direction == 'L':
            self.dx = min(abs(self.dx) + abs(self.dx) * Ball.em, Ball.ball_speed_max)
        else:
            self.dx = -min(abs(self.dx) + abs(self.dx) * Ball.em, Ball.ball_speed_max)
        self.dy = max(min(new_dy, Ball.ball_speed_max), -Ball.ball_speed_max)