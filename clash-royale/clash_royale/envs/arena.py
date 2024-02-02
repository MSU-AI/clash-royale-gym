import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces

MAX_NUMBER_TROOPS = 32
MAX_TROOP_TYPES = 32
MAX_TROOP_HEALTH = 1000

class ArenaEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 16}

    def __init__(self, render_mode=None, width=8, height=16):
        self.width = width  # The size of the square grid
        self.height = height
        self.window_size_width = 450  # The size of the PyGame window width
        self.window_size_height = 850  # The size of the PyGame window height

        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(np.array([0, 0]), np.array([width - 1, height - 1]), shape=(2,), dtype=int),
                "target": spaces.Box(np.array([0, 0]), np.array([width - 1, height - 1]), shape=(2,), dtype=int),
                "blue-troops": spaces.Box(0, np.tile(np.array([width, height, MAX_TROOP_TYPES, MAX_TROOP_HEALTH]), (MAX_NUMBER_TROOPS,1,)), shape=(MAX_NUMBER_TROOPS, 4,), dtype=np.float32),
                "red-troops": spaces.Box(0, np.tile(np.array([width, height, MAX_TROOP_TYPES, MAX_TROOP_HEALTH]), (MAX_NUMBER_TROOPS,1,)), shape=(MAX_NUMBER_TROOPS, 4,), dtype=np.float32),
            }
        )

        # We have 4 actions, corresponding to "right", "up", "left", "down"
        self.action_space = spaces.Discrete(4)

        """
        The following dictionary maps abstract actions from `self.action_space` to
        the direction we will walk in if that action is taken.
        I.e. 0 corresponds to "right", 1 to "up" etc.
        """
        self._action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1]),
        }

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
        return {"agent": self._agent_location, "target": self._target_location, "blue-troops": self._blue_troops, "red-troops": self._red_troops}
    
    def _get_info(self):
        return {
            "distance": np.linalg.norm(
                self._agent_location - self._target_location, ord=1
            )
        }
    
    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        self._king_blue_tower_draw_location = [3.5, 14.5]
        self._king_red_tower_draw_location = [3.5, 0.5]

        self._king_blue_tower_center_location = [4, 15]
        self._king_red_tower_center_location = [4, 1]

        self._king_tower_range = 4.0

        self._blue_troops = np.zeros((MAX_NUMBER_TROOPS,4,), dtype=np.float32)
        self._red_troops = np.zeros((MAX_NUMBER_TROOPS,4,), dtype=np.float32)
        
        #Test
        self._blue_troops[0] = [3, 3, 0, 150]
        self._red_troops[0] = [4, 12, 1, 100]

        # Choose the agent's location uniformly at random
        self._agent_location = self.np_random.integers(0, [self.width, self.height], size=2, dtype=int)

        # We will sample the target's location randomly until it does not coincide with the agent's location
        self._target_location = self._agent_location
        while np.array_equal(self._target_location, self._agent_location):
            self._target_location = self.np_random.integers(0, [self.width, self.height], size=2, dtype=int)

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info
    
    def step(self, action):
        # Map the action (element of {0,1,2,3}) to the direction we walk in
        direction = self._action_to_direction[action]
        # We use `np.clip` to make sure we don't leave the grid
        self._agent_location = np.clip(
            self._agent_location + direction, 0, [self.width - 1, self.height - 1]
        )
        # An episode is done iff the agent has reached the target
        terminated = np.array_equal(self._agent_location, self._target_location)
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
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode(
                (self.window_size_width, self.window_size_height)
            )
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.window_size_width, self.window_size_height))
        canvas.fill((255, 255, 255))
        pix_square_size_height = (
            self.window_size_height / self.height
        )  # The height of a single grid square in pixels
        pix_square_size_width = (
            self.window_size_width / self.width
        )

        pix_square_size = np.array([pix_square_size_width, pix_square_size_height])


        # Draw tower ranges
        pygame.draw.circle(
            canvas,
            (211, 211, 211),
            self._king_blue_tower_center_location * pix_square_size,
            self._king_tower_range * pix_square_size_height,
        )
        pygame.draw.circle(
            canvas,
            (211, 211, 211),
            self._king_red_tower_center_location * pix_square_size,
            self._king_tower_range * pix_square_size_height,
        )

        # Add some gridlines
        for x in range(self.height + 1):
            pygame.draw.line(
                canvas,
                (0, 0, (x == self.height // 2 - 1 or x == self.height // 2 + 1) * 255),
                (0, pix_square_size_height * x),
                (self.window_size_width, pix_square_size_height * x),
                width=(1 + (x == self.height // 2 - 1 or x == self.height // 2 + 1)),
            )

        for x in range(self.width + 1):
            pygame.draw.line(
                canvas,
                0,
                (pix_square_size_width * x, 0),
                (pix_square_size_width * x, self.window_size_height),
                width=1,
            )

        # Blue tower
        pygame.draw.rect(
            canvas,
            (0, 0, 190),
            pygame.Rect(
                pix_square_size * self._king_blue_tower_draw_location,
                pix_square_size,
            ),
        )

        troop_colors = [(153, 255, 51), (255, 102, 155)]
        troop_sizes = [0.5, 0.4]
        for troop in self._blue_troops:
            if troop[3] > 0:
                pygame.draw.circle(
                    canvas,
                    troop_colors[int(troop[2])],
                    [troop[0], troop[1]] * pix_square_size,
                    troop_sizes[int(troop[2])] * pix_square_size_height,
                )
                pygame.draw.rect(
                    canvas,
                    (0, 0, 155),
                    pygame.Rect(
                        [troop[0] - 0.5, troop[1] - troop_sizes[int(troop[2])] - 0.2] * pix_square_size,
                        [1, 0.2] * pix_square_size,
                    ),
                )
                

        for troop in self._red_troops:
            if troop[3] > 0:
                pygame.draw.circle(
                    canvas,
                    troop_colors[int(troop[2])],
                    [troop[0], troop[1]] * pix_square_size,
                    troop_sizes[int(troop[2])] * pix_square_size_height,
                )
                pygame.draw.rect(
                    canvas,
                    (155, 0, 0),
                    pygame.Rect(
                        [troop[0] - 0.5, troop[1] - troop_sizes[int(troop[2])] - 0.2] * pix_square_size,
                        [1, 0.2] * pix_square_size,
                    ),
                )

        # Red tower
        pygame.draw.rect(
            canvas,
            (190, 0, 0),
            pygame.Rect(
                pix_square_size * self._king_red_tower_draw_location,
                pix_square_size,
            ),
        )

        if self.render_mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )
        
    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()