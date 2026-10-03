"""Fish types that swim horizontally and wrap around the pond."""

import pygame


class Fish:
    def __init__(self, x, y, speed, width=36, height=18, point_value=10, color=(80, 180, 220)):
        self.x = float(x)
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.point_value = point_value
        self.color = color

    def update(self, screen_width):
        self.x += self.speed
        if self.speed > 0 and self.x > screen_width:
            self.x = -self.width
        elif self.speed < 0 and self.x < -self.width:
            self.x = screen_width

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )


class SlowFish(Fish):
    """A large, easy-to-catch green fish worth 10 points."""

    def __init__(self, x, y, direction=1):
        super().__init__(
            x=x,
            y=y,
            speed=1.5 if direction >= 0 else -1.5,
            width=46,
            height=24,
            point_value=10,
            color=(70, 200, 120),
        )


class FastFish(Fish):
    """A small, quick orange fish worth 25 points."""

    def __init__(self, x, y, direction=1):
        super().__init__(
            x=x,
            y=y,
            speed=4 if direction >= 0 else -4,
            width=30,
            height=15,
            point_value=25,
            color=(255, 145, 55),
        )
