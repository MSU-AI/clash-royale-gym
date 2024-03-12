"""
High-level components for managing the simulation

This file contains components that are intended to manage and preform the simulation.
The components defined here are probably what end users want to utilize,
as they will greatly simplify the simulation procedure.
"""

from __future__ import annotations

from typing import List, Tuple
import numpy as np
import numpy.typing as npt
import pygame

from clash_royale.envs.game_engine.arena import Arena
from clash_royale.envs.game_engine.struct import Scheduler, GameScheduler, DefaultScheduler
from clash_royale.envs.game_engine.player import Player
from clash_royale.envs.game_engine.card import Card


class GameEngine:
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
                 deck1: List[str],
                 deck2: List[str],
                 width: int=18,
                 height: int=32,
                 resolution: Tuple[int, int]=(128, 128),
                 fps: int=30
                 ) -> None:
        """
        The game_engine should be initialized with settings such as resolution
        and framerate, this shouldn't be used to initialize
        any specific actual game, that will be handled in reset.
        """

        self.width: int = width  # Width of arena
        self.height: int = height  # Height of arena
        self.resolution: Tuple[int, int] = resolution
        self.fps: int = fps

        self.arena: Arena = Arena(width=self.width, height=self.height)
        self.player1: Player = Player(deck1, fps)
        self.player2: Player = Player(deck2, fps)

        self.scheduler: Scheduler = Scheduler(fps) # counting frames
        self.game_scheduler: DefaultScheduler = DefaultScheduler(self.scheduler) # determining elixir etc.

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

        individual sprite rendering methods required.
        arena.get_entities() missing
        """

        entities: List[Entity] = self.arena.get_entities()
        canvas = pygame.Surface(size=self.resolution)

        #rendering logic goes here...

        return np.array(pygame.surfarray.pixels3d(canvas))

    def apply(self, player_id: int, action: Tuple[int, int, int] | None) -> None:
        """
        Applies a given action to the environment, checks
        for validity of the action via asserts.
        """
        if action is None:
            return

        assert action[0] >= 0 and action[0] < self.width
        assert action[1] >= 0 and action[1] < self.height
        assert action[2] >= 0 and action[2] < 4

        curr_player: Player
        if player_id == 0:
            curr_player = self.player1
        else:
            curr_player = self.player2

        card: Card = curr_player.hand[action[2]]
        assert card.elixir <= curr_player.elixir

        self.arena.play_card(action[0], action[1], card)
        curr_player.play_card(action[2])

    def step(self, frames: int=1) -> None:
        """
        Steps through a number of frames,
        applying simulations and updating required components.
        """

        # update elixir first, order TBD.
        elixir_rate: float = self.game_scheduler.elixir_rate()
        self.player1.step(elixir_rate, frames)
        self.player2.step(elixir_rate, frames)

        self.arena.step(frames)
        self.scheduler.step(frames)


    def legal_actions(self, player_id: int) -> npt.NDArray[np.float64]:
        """
        Returns a list of legal actions.
        """
        actions = np.zeros(shape=(32, 18, 4), dtype=np.float64)

        hand: List[int]
        if player_id == 0:
            hand = self.player1.get_pseudo_legal_cards()
        else:
            hand = self.player2.get_pseudo_legal_cards()

        placement_mask = self.arena.get_placement_mask()
        for card_index in hand:
            actions[placement_mask, card_index] = 1

        return actions

    def is_terminal(self) -> bool:
        """
        Determines if game has ended
        """
        if self.game_scheduler.is_game_over():
            return True

        if self.game_scheduler.is_overtime():
            player1_val: int = self.arena.tower_count(0)
            player2_val: int = self.arena.tower_count(1)
            if player1_val != player2_val:
                return True

        return False

    def terminal_value(self) -> int:
        """
        Returns side won, otherwise returns -1.
        """
        player1_val: int = self.arena.tower_count(0)
        player2_val: int = self.arena.tower_count(1)
        if player1_val == player2_val:
            player1_val = self.arena.lowest_tower_health(0)
            player2_val = self.arena.lowest_tower_health(1)

        if player1_val > player2_val:
            return 1

        if player2_val > player1_val:
            return 0

        if player1_val == player2_val:
            return -1
