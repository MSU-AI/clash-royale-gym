"""
Logic components for attacking.

These components describe how an entity attacks another.
We determine how an entity attacks the target
(single? AOE?)
We also describe what an attack does to an enemy, 
be it do damage (default) or effect done to enemy (slowness)
"""

from typing import TYPE_CHECKING

from clash_royale.envs.game_engine.arena import Arena
from clash_royale.envs.game_engine.entities.entity import Entity
from clash_royale.envs.game_engine.utils import distance

if TYPE_CHECKING:
    from clash_royale.envs.game_engine.entities.logic_entity import LogicEntity


class BaseAttack:
    """
    BaseAttack - Class all attacks should inherit!

    TODO: We need to implement an attack delay,
    that being the time between attacks so entities do not attack each frame.
    Should we also have a delay that determines how long the attack so take?
    """

    def __init__(self) -> None:
        
        self.entity: LogicEntity  # Entity we are managing
        self.arena: Arena  # Arena we are apart of

        self.last_attack: int = 0  # Frame of last attack

    def entity_distance(self, tentity: Entity) -> float:
        """
        Determines the distance between an entity and ourselves.

        :param tentity: Entity to determine distance
        :type tentity: Entity
        :return: Distance between entities
        :rtype: float
        """

        return distance(self.entity.x, self.entity.y, tentity.x, tentity.y)

    def can_attack(self) -> bool:
        """
        Determines if this entity can attack.

        We ensure the targeted entity is within our attack range,
        and that the attack delay has been reached.

        :return: True if we can attack, False if not
        :rtype: bool
        """

        # Determine if we have a target:

        if self.entity.target_ent is not None:

            # Determine if our delay has passed:

            if self.entity.collection.engine.scheduler.frame() > (self.entity.stats.attack_delay + self.last_attack):

                # Determine if entity is within range:

                if self.entity.stats.attack_range <= self.entity_distance(self.entity.target_ent):

                    # Within range, return True:

                    return True
                
        # Otherwise, return False:
                
        return False

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

        # Determine if we can attack:

        if self.can_attack():

            # Otherwise, preform an attack:

            self.entity.target_ent.stats.health -= self.entity.stats.damage
