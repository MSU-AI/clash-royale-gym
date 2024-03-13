"""
Entities that utilize the logical framework    
"""

from clash_royale.envs.game_engine.entities.entity import Entity
from clash_royale.envs.game_engine.logic.attack import BaseAttack
from clash_royale.envs.game_engine.logic.target import BaseTarget
from clash_royale.envs.game_engine.logic.movement import BaseMovement


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

        self.attack: BaseAttack  # Attack component to use
        self.target: BaseTarget  # Target component to use
        self.movement: BaseMovement  # Movement component to use

        self.target_entity: Entity  # Current entity being considered

    def simulate(self):
        """
        Preforms an entity simulation.
        """

        # First, ask for targeting:

        self.target_entity = self.target.target()

        # Next, determine attack:

        self.attack.attack()

        # Finally, determine movement:

        self.movement.move()

        return super().simulate()
