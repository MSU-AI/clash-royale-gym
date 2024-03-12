"""
Various structures to be utilized   
"""

import dataclasses

class Scheduler:
    """
    Scheduling class to handle all timings,
    such as attacks, elixir increase, etc.
    For now, it will just store frame_count.
    """
    def __init__(self, fps: int =30):
        self.fps: int = fps
        self.frame_num: int = 0

    def reset(self):
        self.frame_num = 0

    def step(self, frames: int=1):
        self.frame_num += frames
        # possibly check all event timings here

    def frame(self) -> int:
        return self.frame_num

class GameScheduler:
    """
    Template class for game scheduling
    """
    def __init__(self, scheduler: Scheduler, fps: int=30) -> None:
        self.scheduler: Scheduler = scheduler
        self.fps: int = fps

class DefaultScheduler(GameScheduler):
    """
    Class for default 1v1 game scheduling
    """

    def elixir_rate(self) -> float:
        return 0

    def game_state(self) -> int:
        """
        Function to get current game state:
        ex: Game is over, double elixir, overtime, etc.
        """
        return 0

    def is_game_over(self) -> bool:
        return False

    def is_overtime(self) -> bool:
        return False

@dataclasses.dataclass(slots=True)
class Stats:
    """
    Stats - Various stats to be utilized by entities

    This class contains definitions for entity stats,
    which describe the current state of the entity (health),
    and behavior of the entity (speed, damage, range, ect.)

    It is HIGHLY recommended to have all entities fall under
    this uniform definition of stats.
    This will make all entity interactions much easier.

    We will describe some complicated stats here:

    Attack range is the distance an entity can attack from.
    If an entity is within this range, then it will preform an attack on the enemy.

    Sight range is the distance an entity can detect enemies.
    If an enemy is within the sight range, the entity will select it as a target.
    The entity will then attempt to either attack (if within attack range)
    or navigate to the entity until the entity is dead, or moves outside sight range.
    """

    name: str = ''  # Name of entity
    speed: int = 0  # Number of pixels per second (TODO: Find better unit?)
    attack_range: int = 0  # Attack range, in a radius around the unit in pixels
    sight_range: int = 0  # Sight range, in a radius around the unit in pixels
    health: int = 0  # Health of unit
    damage: int = 0  # Damage of unit
    troop_size: int = 0  # Size of trop pixels, determines how troop will be rendered
    attack_delay: int = 0  # Delay in frames each attack should take
