"""
High-level components for managing the simulation

This file contains components that are intended to manage and preform the simulation.
The components defined here are probably what end users want to utilize,
as they will greatly simplify the simulation procedure.
"""

from typing import List

from clash_royale.envs.ngame_engine.entities.entity import Entity, EntityCollection


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
        
        self.width = width  # Width of arena
        self.height = height  # Height of arena
