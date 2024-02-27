"""
High-level components for managing the simulation

This file contains components that are intended to manage and preform the simulation.
The components defined here are probably what end users want to utilize,
as they will greatly simplify the simulation procedure.

How should we decide order? Length Width Height?
I think LxHxCard.
"""

from typing import List, Tuple
import numpy as np
import numpy.typing as npt
import pygame

from clash_royale.envs.game_engine.entities.entity import Entity, EntityCollection
from clash_royale.envs.game_engine.arena import Arena
from clash_royale.envs.game_engine.struct import Scheduler, DefaultScheduler
from clash_royale.envs.game_engine.player import Player


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
        """
        self.width = width  # Width of arena
        self.height = height  # Height of arena
        self.resolution = resolution

        self.arena = Arena(width=self.width, height=self.height)
        self.player1 = Player(deck1)
        self.player2 = Player(deck2)

        self.scheduler = Scheduler(fps=30) # counting frames
        self.game_scheduler = DefaultScheduler(self.scheduler, fps=30) # determining elixir etc.

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

    def make_image(self, player_id: int) -> npt.NDArray[np.uint8]:
        """
        Asks the arena to render itself.

        TODO: We need to figure out this procedure!
        Arena should render any generic components,
        and then ask the entities to render themselves.
        """

        entities = self.arena.get_entities()
        canvas = pygame.Surface(size=self.resolution)

        #...

        return np.array(pygame.surfarray.pixels3d(canvas))

    def apply(self, player_id: int, action: Tuple[int, int, int] | None) -> None:
        """
        Applies a given action to the environment, checks
        for validity of the action via asserts.
        """
        if action is None:
            return
        
        assert(action[0] >= 0 and action[0] < self.width)
        assert(action[1] >= 0 and action[1] < self.height)
        assert(action[2] >= 0 and action[2] < 4)
        
        if player_id == 0:
            curr_player = self.player1
        else:
            curr_player = self.player2

        card = curr_player.hand[action[2]]
        assert(card.elixir <= curr_player.elixir)

        self.arena.play_card(action[0], action[1], card)
        curr_player.play_card(action[2])

    def step(self, frames: int=1):
        """
        Steps through a number of frames,
        applying simulations and updating required components.
        """

        pass

    def legal_actions(self):
        """
        
        Returns a list of legal actions.
        Format is TBD
        """
        pass
