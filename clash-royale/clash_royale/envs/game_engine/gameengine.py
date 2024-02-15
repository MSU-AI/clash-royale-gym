"""
High-level components for managing the simulation

This file contains components that are intended to manage and preform the simulation.
The components defined here are probably what end users want to utilize,
as they will greatly simplify the simulation procedure.
"""

from typing import List

from clash_royale.envs.ngame_engine.entities.entity import Entity, EntityCollection


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

    def __init__(self, width: int =8, height: int=18) -> None:
        
        self.width = width  # Width of arena
        self.height = height  # Height of arena

    def render(self):
        """
        Asks the arena to render itself.

        TODO: We need to figure out this procedure!
        Arena should render any generic components,
        and then ask the entities to render themselves.
        """

        pass
