from __future__ import annotations
from typing import Tuple

import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces

from clash_royale.envs.game_engine.game_engine import GameEngine

class ClashRoyaleEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 16}

    def __init__(self, render_mode: str | None=None, width: int=18, height: int=32):
        self.width: int = width  # The size of the square grid
        self.height: int = height
        resolution: Tuple[int, int] = (128, 128)

        self.observation_space = spaces.Dict(
        )

        self.action_space = spaces.Discrete(1)


        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None 

    def _get_obs(self):
        pass

    def _get_info(self):
        pass

    def reset(self, seed=None, options=None):
        pass

    def step(self, action):
        pass

    def render(self):
        pass

    def _render_frame(self):
        pass

    def close(self):
        pass
