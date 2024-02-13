"""
Logic components for targeting.

These components describe how targeting is preformed.
'Targeting' is the process of determining what things get targeted.
If no entities are selected, then we simply defer targeting to another component.
"""

from clash_royale.envs.ngame_engine.arena import Arena
from clash_royale.envs.ngame_engine.entities.entity import Entity
from clash_royale.envs.ngame_engine.utils import distance


class BaseTarget:
    """
    BaseTarget - Class all target components must inherit!
    """

    def __init__(self) -> None:
        
        self.arena: Arena = None  # Arena component to consider
        self.entity: Entity = None  # Entity we are attached to

    def entity_distance(self, tentity: Entity) -> float:
        """
        Determines the distance between an entity and ourselves.

        :param tentity: Entity to determine distance
        :type tentity: Entity
        :return: Distance between entities
        :rtype: float
        """

        return distance(self.entity.x, self.entity.y, tentity.x, tentity.y)

    def target(self) -> Entity:
        """
        Finds a target in the arena, and returns an entity.

        If no target is found, simply return None.
        """

        raise NotImplementedError("Must be implemented in child class!")


class RadiusTarget(BaseTarget):
    """
    Finds the first entity within our radius.

    We take into consideration the sight range of this entity,
    and will target the first entity within our radius.
    """

    def target(self) -> Entity:
        """
        Finds the first target that is within our radius.

        :return: Entity to target
        :rtype: Entity
        """

        # Iterate over entities:

        for ent in self.arena.entities:

            # Determine if entity is near us:

            if self.entity.sight_range >= distance():

                # We found a target, return:

                return ent

        # We found no target:

        return None
