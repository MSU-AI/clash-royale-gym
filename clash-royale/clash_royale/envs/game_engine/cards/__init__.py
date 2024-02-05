import numpy as np
import numpy.typing as npt
import pygame

class Card():
    def __init__(self, pixel_size: npt.ArrayLike):
        self.pixel_size = pixel_size

class Troop(Card):
    def __init__(self,
                 pixel_size:npt.ArrayLike,

                 location: npt.ArrayLike,
                 elixir:int,
                 health:int,
                 damage:int,
                 hit_speed:int,
                 attack_range:int,
                 sight_range:int,
                 troop_targeting:bool,
                 is_air:bool):
        super().__init__(pixel_size)
        self.location = location
        self.elixir = elixir
        self.max_health = health
        self.health = health
        self.damage = damage
        self.hit_speed = hit_speed
        self.attack_range = attack_range
        self.sight_range = sight_range
        self.troop_targeting = troop_targeting
        self.is_air = is_air

    def render(self, canvas):
        pygame.draw.circle(
            canvas,
            (0,0,0),
            self.location * self.pixel_size,
            0.3 * self.pixel_size[0], #  0.3 temp set size, using height as sizes
        )
        pygame.draw.circle(
            canvas,
            (255, 255, 255),
            self.location * self.pixel_size,
            0.3 * self.pixel_size[0]*0.95,#  0.3 temp set size, using height as sizes
        )

class Knight(Troop):
    def __init__(self, pixel_size: np.ArrayLike, location: npt.ArrayLike):
        super().__init__(
            pixel_size,
            location,
            3,
            1766,
            202,
            1.2,
            1.2,
            5.5,
            True,
            False)
    def render(self):
        pass

name_to_card = {
    'knight' : Knight
}