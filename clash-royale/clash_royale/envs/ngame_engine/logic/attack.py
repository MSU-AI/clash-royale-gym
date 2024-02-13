"""
Logic components for attacking.

These components describe how an entity attacks another.
We determine how an entity attacks the target
(single? AOE?)
We also describe what an attack does to an enemy, 
be it do damage (default) or effect done to enemy (slowness)
"""

from clash_royale.envs.ngame_engine.arena import Arena
from clash_royale.envs.ngame_engine.entities.entity import Entity
from clash_royale.envs.ngame_engine.utils import distance


class BaseAttack:
    """
    BaseAttack - Class all attacks should inherit!

    TODO: We need to implement an attack delay,
    that being the time between attacks so entities do not attack each frame.
    Should we also have a delay that determines how long the attack so take?
    """

    def __init__(self) -> None:
        
        self.entity: Entity = None  # Entity we are managing
        self.arena: Arena = None  # Arena we are apart of

    def entity_distance(self, tentity: Entity) -> float:
        """
        Determines the distance between an entity and ourselves.

        :param tentity: Entity to determine distance
        :type tentity: Entity
        :return: Distance between entities
        :rtype: float
        """

        return distance(self.entity.x, self.entity.y, tentity.x, tentity.y)

    def attack(self):
        """
        Preforms an attack on a target, if any.
        """

        raise NotImplementedError("Must implement this function!")
    

class SingleAttack(BaseAttack):
    """
    SingleAttack - An attack on a singular entity.

    We simply determine if the entity has a target,
    determines if we are within the entity range,
    and preforms an attack by subtracting health from damage.
    """

    def attack(self):
        """
        Preforms an attack operation.
        """

        # First, determine if we have a target:

        if self.entity.target is None:

            # No target, do nothing:

            return

        # Determine if target is within range:

        if self.entity.stats.attack_range <= self.entity_distance(self.entity, self.entity.target):

            # Not within range, do nothing

            return

        # Otherwise, preform an attack:

        self.entity.target.stats.health -= self.entity.stats.damage
