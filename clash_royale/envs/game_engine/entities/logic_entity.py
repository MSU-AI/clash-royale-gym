"""
Entities that utilize the logical framework    
"""

from clash_royale.envs.ngame_engine.entities.entity import Entity
from clash_royale.envs.ngame_engine.logic.attack import BaseAttack
from clash_royale.envs.ngame_engine.logic.target import BaseTarget
from clash_royale.envs.ngame_engine.logic.movement import BaseMovement


class LogicEntity(Entity):
    """
    An entity that operates within our logical framework.

    This entity allows for logic components to be attached,
    allowing for behavior to be generalized and attached to entities.
    We support all logical components, those being:

    - Targeting
    - Attacking
    - Movement

    The entity will react to these components,
    and will ask them to do something each frame.
    """

    def __init__(self) -> None:
        super().__init__()

        self.attack: BaseAttack = None  # Attack component to use
        self.target: BaseTarget = None  # Target component to use
        self.movement: BaseMovement = None  # Movement component to use

    def simulate(self):
        """
        Preforms an entity simulation.
        """

        # First, ask for targeting:

        self.target = self.target.target()

        # Next, determine attack:

        self.attack.attack()

        # Finally, determine movement:

        self.movement = self.movement.move()

        return super().simulate()