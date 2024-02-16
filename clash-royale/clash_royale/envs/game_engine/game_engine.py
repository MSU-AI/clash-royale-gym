"""
High-level components for managing the simulation

This file contains components that are intended to manage and preform the simulation.
The components defined here are probably what end users want to utilize,
as they will greatly simplify the simulation procedure.
"""

from typing import List, Tuple
import numpy as np
import numpy.typing as npt

from clash_royale.envs.game_engine.entities.entity import Entity, EntityCollection
from clash_royale.envs.game_engine.arena import Arena
from clash_royale.envs.game_engine.struct import Scheduler


class GameEngine(EntityCollection):
    """
    Arena - High-level simulation component

    This component is the entry point for the entire simulation!
    We manage and simulate any attached entities,
    and render the final result in some way.

    We contain the entities that are in play,
    and handle the process of simulating them.
    Methods for adding and removing entities are also available.

    TODO: Need to figure out frame independent timekeeping  
    """

    def __init__(self, 
                 width: int =18, 
                 height: int=32, 
                 resolution: Tuple[int, int] =(128, 128),
                 deck1: List[str] =['barbarian'] * 8,
                 deck2: List[str] =['barbarian'] * 8,
                 ) -> None:
        """
        The game_engine should be initialized with settings such as resolution
        and framerate, this shouldn't be used to initialize
        any specific actual game, that will be handled in reset.

        Player class missing.
        """
        self.width = width  # Width of arena
        self.height = height  # Height of arena
        self.resolution = resolution

        self.arena = Arena(width=self.width, height=self.height)
        self.player1 = Player(deck1)
        self.player2 = Player(deck2)
        self.scheduler = Scheduler(fps=30)

    def reset(self) -> None:
        """
        This should be called to reset the game engine
        to its default/starting state.

        Arena.reset() method missing.
        Player.reset() method missing.
        """
        self.arena.reset()
        self.player1.reset(elixir=5)
        self.player2.reset(elixir=5)
        self.scheduler.reset()

    def make_image(self) -> npt.NDArray[np.uint8]:
        """
        Asks the arena to render itself.

        TODO: We need to figure out this procedure!
        Arena should render any generic components,
        and then ask the entities to render themselves.
        """

        pass
