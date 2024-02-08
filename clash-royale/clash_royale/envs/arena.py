import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces
import clash_royale.envs.game_engine as engine


class ArenaEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"]}

    def __init__(self, render_mode=None):
        self.width = 18
        self.height = 32
        self.window_size_width = 128  # The size of the PyGame window width
        self.window_size_height = 128  # The size of the PyGame window height

        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        self.observation_space = spaces.Dict(
            {
                "p1-view": spaces.Box(0, 255, shape=(self.window_size_width, self.window_size_height, 3), dtype=np.uint8),
                "p2-view": spaces.Box(0, 255, shape=(self.window_size_width, self.window_size_height, 3), dtype=np.uint8),
            }
        )

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        # Width x Height x "cards"
        self.action_space = spaces.Discrete(18*32*5)

    def _get_obs(self):
        return {"p1-view": self._p1_view, "p2-view": self._p2_view}
    
    def _get_info(self):
        return {
        }
    
    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        self._p1_view = np.zeros(shape=(self.window_size_width, self.window_size_height, 3), dtype=np.uint8)
        self._p2_view = np.zeros(shape=(self.window_size_width, self.window_size_height, 3), dtype=np.uint8)

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info
    
    def step(self, action):
        
        terminated = False
        reward = 1 if terminated else 0  # Binary sparse rewards
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        #if self.window is None and self.render_mode == "human":
            #pygame.init()
            #pygame.display.init()
            #self.window = pygame.display.set_mode(
            #    (self.window_size_width, self.window_size_height)
            #)
        #if self.clock is None and self.render_mode == "human":
            #self.clock = pygame.time.Clock()

        if self.render_mode == "human":
            pass
            # The following line copies our drawings from `canvas` to the visible window
            #self.window.blit(canvas, canvas.get_rect())
            #pygame.event.pump()
            #pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            #self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.zeros(shape=(self.window_size_width, self.window_size_height, 3), dtype=np.uint8)
            #return np.transpose(
            #    np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            #)
        
    def close(self):
        pass