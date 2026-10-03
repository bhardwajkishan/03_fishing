"""Game state and per-frame logic for the fishing game."""

import math

from game.hook import CASTING, Hook, IDLE
from game.fish import FastFish, SlowFish
from game.catch import check_catch
from game.renderer import WIDTH, HEIGHT, SURFACE_Y, MAX_DEPTH_Y

ROUND_DURATION = 30.0


class GameEngine:
    def __init__(self):
        self.hook = Hook(x=WIDTH / 2, surface_y=SURFACE_Y, max_depth_y=MAX_DEPTH_Y, speed=5)
        self.restart_round()

    @staticmethod
    def _create_fish():
        return [
            SlowFish(x=100, y=180, direction=1),
            FastFish(x=500, y=230, direction=-1),
            SlowFish(x=400, y=310, direction=-1),
            FastFish(x=180, y=390, direction=1),
        ]

    def restart_round(self):
        """Reset all round state so the player can play again."""
        self.hook.reset()
        self.fish_list = self._create_fish()
        self.hooked_fish = None
        self.score = 0
        self.time_remaining = ROUND_DURATION
        self.round_over = False

    def start_cast(self):
        """Handle a player's cast request."""
        if self.round_over:
            return False
        return self.hook.start_cast()

    def update(self, delta_seconds):
        if self.round_over:
            return

        self.time_remaining = max(0.0, self.time_remaining - delta_seconds)
        if self.time_remaining <= 1e-9:
            self.time_remaining = 0.0
            self.round_over = True
            self.hooked_fish = None
            self.hook.reset()
            return

        self.hook.update()

        for fish in self.fish_list:
            fish.update(WIDTH)

        if self.hooked_fish is not None:
            self.hooked_fish.x = self.hook.x
            self.hooked_fish.y = self.hook.y
            if self.hook.state == IDLE:
                self.score += self.hooked_fish.point_value
                self.hooked_fish = None
        elif self.hook.state == CASTING:
            caught = check_catch(self.hook, self.fish_list)
            if caught is not None:
                self.fish_list.remove(caught)
                self.hooked_fish = caught
                self.hooked_fish.x = self.hook.x
                self.hooked_fish.y = self.hook.y
                self.hook.catch_fish()

    def draw(self, surface, font):
        from game import renderer
        draw_list = list(self.fish_list)
        if self.hooked_fish is not None:
            draw_list.append(self.hooked_fish)
        renderer.draw_scene(surface, self.hook, draw_list)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(
            surface,
            font,
            f"Time: {math.ceil(self.time_remaining)}",
            (WIDTH - 130, 10),
        )

        if self.round_over:
            renderer.draw_text(surface, font, "R: New Round", (10, 40))
            renderer.draw_banner(surface, font, f"Time's up! Final score: {self.score}", -20)
            renderer.draw_banner(surface, font, "Press R to play again", 20)
        else:
            renderer.draw_text(surface, font, "SPACE: Cast", (10, 40))
