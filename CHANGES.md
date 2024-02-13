# Controversial Changes

This document outlines some very opinionated changes that are done to the backend.
These changes SHOULD be discussed and SHOULD be debated if we want to move forward.

This branch contains a decent redesign of the backend architecture,
which aims to make the backend engine 
(let's come up with a cute name for this, maybe Clash royal Simulation Engine (CSE))
generic and modular, so new cards (and maybe game features)
can be quickly developed and integrated.

All the changes live under `ngame_engine`, and can be merged/deleted as we see fit.

## Arena

We utilize a new implementation of the CSE arena.
This component is the highest level component in our engine,
and it will be what most people will primarily interact with.

This component has the following goals:

- Rendering - Renders frames of the simulation for display/further processing
- Entity Management - Adding, removal, and entity simulation operations
- Time Handling - An attempt to make timekeeping independent of framerate, i.e accurate simulation with arbitrary framerate
- Maybe some more...

Most of these are implemented by other components, such as pygame, and we will go into detail as to how this is done.

## Entity

An 'entity' is something that is displayed on screen,
and something that (probably) has logic and interacts with other entities.
EVERYTHING is an entity in CSE.
There are specializations, such as buildings and troops,
but everything is an entity and inherits entity features.

Entity's have the following goals:

- Rendering - Each entity MUST render themselves
- Logic - Each entity gets a function that is executed each time the entity is asked to simulate
- State - Entities keep track of their state, and can hook custom actions into each state
