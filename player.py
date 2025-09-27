class Player:
    def __init__(self, x, y, radius):
        self.alive = True
        self.death_time = None
        self.ball_radius = radius
        self.speed = 8
        self.x = x
        self.y = y