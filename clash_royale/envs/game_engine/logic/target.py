"""
Logic components for targeting.

These components describe how targeting is preformed.
'Targeting' is the process of determining what things get targeted.
If no entities are selected, then we simply defer targeting to another component.
"""

from typing import TYPE_CHECKING

from clash_royale.envs.game_engine.arena import Arena
from clash_royale.envs.game_engine.entities.entity import Entity
from clash_royale.envs.game_engine.utils import distance

if TYPE_CHECKING:
    from clash_royale.envs.game_engine.entities.logic_entity import LogicEntity

class BaseTarget:
    """
    BaseTarget - Class all target components must inherit!
    """

    def __init__(self) -> None:
        
        self.arena: Arena  # Arena component to consider
        self.entity: LogicEntity  # Entity we are attached to

    def entity_distance(self, tentity: Entity) -> float:
        """
        Determines the distance between an entity and ourselves.

        :param tentity: Entity to determine distance
        :type tentity: Entity
        :return: Distance between entities
        :rtype: float
        """

        return distance(self.entity.x, self.entity.y, tentity.x, tentity.y)

    def target(self):
        """
        Finds a target in the arena, and returns an entity.
        """

        raise NotImplementedError("Must be implemented in child class!")


class RadiusTarget(BaseTarget):
    """
    Finds the first entity within our radius.

    We take into consideration the sight range of this entity,
    and will target the first entity within our radius.
    """

    def target(self):
        """
        Finds the first target that is within our radius.
        """

        # Iterate over entities:

        for ent in self.arena.entities:

            # Determine if entity is near us:

            if self.entity.stats.sight_range >= self.entity_distance(self.entity.target_ent):

                # We found a target, set:

                self.entity.target_ent = ent
