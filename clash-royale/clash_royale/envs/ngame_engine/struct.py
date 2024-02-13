"""
Various structures to be utilized   
"""

import dataclasses


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
