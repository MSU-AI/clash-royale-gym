"""
High-level components for managing the simulation

This file contains components that are intended to manage and preform the simulation.
The components defined here are probably what end users want to utilize,
as they will greatly simplify the simulation procedure.
"""

from typing import TYPE_CHECKING

from clash_royale.envs.game_engine.entities.entity import EntityCollection

if TYPE_CHECKING:
    # Only import for typechecking to prevent circular dependency
    from clash_royale.envs.game_engine.game_engine import GameEngine

class Arena(EntityCollection):
    """
    Arena

    This component handles high level logic for the Arena of the game.
    No rendering occurs here, and information is sent
    to the GameEngine component for final rendering.

    We contain the entities that are in play,
    and handle the process of simulating them.
    Methods for adding and removing entities are also available.

    TODO: Need to figure out frame independent timekeeping  
    """

    def __init__(self, width: int =8, height: int=18) -> None:

        super().__init__()

        self.width: int = width  # Width of arena
        self.height: int = height  # Height of arena

        self.engine: GameEngine  # Game engine that is managing this arena

    def reset(self) -> None:
        pass

    def step(self) -> None:
        pass
