from remote_game.game_objects.Ball import Ball

class Paddle:
    vInit = 4
    em = 0.03
    cof = 0.3
    def __init__(self, x=0, y=0, width=10, height=100):
        self.x = x
        self.y = y
        self.dy = 0
        self.accel = 0
        self.width = width
        self.height = height

    def move(self, screen_height):
        if 0 <= self.y + self.dy <= screen_height - self.height:
            self.y += self.dy

    def check_collision(self, ball, direction):
        if not (self.x - ball.radius <= ball.x <= self.x + self.width + ball.radius):
            return
        ballL = ball.x - ball.radius
        ballR = ball.x + ball.radius
        ballT = ball.y - ball.radius
        ballB = ball.y + ball.radius
        padL = self.x
        padR = self.x + self.width
        padT = self.y
        padB = self.y + self.height

        # 좌측 패들의 우측면 충돌 판정
        if direction == 'L' and padR > ballL > padL:
            # 우측면 충돌
            if ball.dx <= 0:
                # 우상단 -> 좌하단 접근 시
                if ball.dy <= 0 and padT <= ballB < self.y + self.height / 2:
                    ball.handle_collision('L', self.dy)
                # 우하단 -> 좌상단 접근 시
                elif ball.dy >= 0 and padB >= ballT > self.y + self.height / 2:
                    ball.handle_collision('L', self.dy)
                # 패들과 겹치는 경우
                elif ballB >= padT and ballT <= padB:
                    ball.handle_collision('L', self.dy)

        # 우측 패들의 좌측면 충돌 판정
        elif direction == 'R' and padL < ballR < padR:
            # 좌측면 충돌
            if ball.dx >= 0:
                # 좌상단 -> 우하단 접근 시
                if ball.dy <= 0 and padT <= ballB < self.y + self.height / 2:
                    ball.handle_collision('R', self.dy)
                # 좌하단 -> 우상단 접근 시
                elif ball.dy >= 0 and padB >= ballT > self.y + self.height / 2:
                    ball.handle_collision('R', self.dy)
                # 패들과 겹치는 경우
                elif ballB >= padT and ballT <= padB:
                    ball.handle_collision('R', self.dy)