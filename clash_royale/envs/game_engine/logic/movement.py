"""
Logic components for movement.

These components describe how movement is preformed.
All entities have targets that they will move to.
This class will move towards a target in some way.
"""

import math

from typing import TYPE_CHECKING

from clash_royale.envs.game_engine.entities.entity import Entity
from clash_royale.envs.game_engine.arena import Arena
from clash_royale.envs.game_engine.utils import slope

if TYPE_CHECKING:
    from clash_royale.envs.game_engine.entities.logic_entity import LogicEntity


class BaseMovement:
    """
    BaseMovement - Class all movement components must inherit!
    """

    def __init__(self) -> None:
        
        self.entity: LogicEntity  # Entity we are attached to
        self.arena: Arena  # Arena component to consider

    def move(self):
        """
        Moves the entity in some way.

        Probably, we want the entities to move towards targets,
        be it another entity or an interest point.
        """

        raise NotImplementedError("MUST implement this method!")


class SimpleMovement(BaseMovement):
    """
    SimpleMovement - Simply move in a straight line to the target 
    """

    def move(self):
        """
        Moves in a straight line towards target.
        """

        # Determine slopes:

        dx = self.entity.x - self.entity.target_ent.x
        dy = self.entity.y - self.entity.target_ent.y

        # Find angle between entities:

        angle = math.atan2(dy, dx)

        # Determine new position:

        speed = self.entity.stats.speed

        self.entity.x += int(speed * math.cos(angle))
        self.entity.y += int(speed * math.sin(angle))
