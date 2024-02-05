import numpy as np
import numpy.typing as npt
import pygame

class Card():
    def __init__(self,
                 elixir: int,
                 pixel_size: npt.ArrayLike) -> None:
        self.elixir = elixir
        self.pixel_size = pixel_size

class Troop(Card):
    def __init__(self,
                 elixir:int,
                 pixel_size:npt.ArrayLike,

                 location: npt.ArrayLike,
                 health:int,
                 damage:int,
                 hit_speed:int,
                 attack_range:int,
                 sight_range:int,
                 troop_targeting:bool,
                 is_air:bool,
                 air_targeting:bool) -> None:
        super().__init__(elixir, pixel_size)
        self.location = location
        self.max_health = health
        self.health = health
        self.damage = damage
        self.hit_speed = hit_speed
        self.attack_range = attack_range
        self.sight_range = sight_range
        self.troop_targeting = troop_targeting
        self.is_air = is_air,
        self.air_targeting = air_targeting

    def render(self, canvas) -> None:
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

class Building(Card):
    def __init__(self,
                 elixir:int,
                 pixel_size:npt.ArrayLike,

                 location: npt.ArrayLike,
                 health:int,
                 damage:int,
                 hit_speed:int,
                 attack_range:int,
                 sight_range:int,
                 air_targeting:bool,) -> None:
        super().__init__(elixir, pixel_size)
        self.location = location
        self.max_health = health
        self.health = health
        self.damage = damage
        self.hit_speed = hit_speed
        self.attack_range = attack_range
        self.sight_range = sight_range
        self.air_targeting = air_targeting

    def render(self, canvas) -> None:
        pass

class PrincessTower(Building):
    pass

class KingTower(Building):
    pass

class Knight(Troop):
    def __init__(self, pixel_size: np.ArrayLike, location: npt.ArrayLike) -> None:
        super().__init__(
            3,
            pixel_size,
            location,
            1766,
            202,
            1.2,
            1.2,
            5.5,
            True,
            False)

name_to_card = {
    'knight' : Knight
}