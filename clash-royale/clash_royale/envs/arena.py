import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces
import clash_royale.envs.game_engine as engine


class ArenaEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"]}

    def __init__(self, fps: int=30, render_mode: str=None):
        self.width = 18
        self.height = 32
        self.window_size_width = 128
        self.window_size_height = 128

        self.fps = fps

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
    
    def step(self, action, frames=1):
        
        for j in range(MAX_NUMBER_TROOPS):
            troop_type_j = int(self._red_troops[j][2])
            if self._red_troops[j][3] <= 0 or TROOP_BUILDING_TARGETING[troop_type_j]:
                continue

            min_v = None
            min_dist = 1000
            for i in range(MAX_NUMBER_TROOPS):
                if self._blue_troops[i][3] <= 0:
                    continue
                v = (self._blue_troops[i] - self._red_troops[j])[:2]
                dist = np.linalg.norm(v)
                if min_dist > dist and dist <= TROOP_SIGHT_RANGE[troop_type_j]:
                    min_dist = dist
                    min_v = v / dist
                    
            if not min_v is None:
                move_direction[1][j] = min_v, min_dist

        for i in range(MAX_NUMBER_TROOPS):
            troop = self._blue_troops[i]
            if troop[3] > 0:
                v = self._king_red_tower_center_location - troop[:2]
                dist = np.linalg.norm(v)
                if move_direction[0][i][1] > dist:
                    move_direction[0][i] = v / dist, dist

                v, dist = move_direction[0][i]
                if dist > TROOP_ATTACK_RANGE[int(troop[2])]:
                    v = v * TROOP_SPEEDS[int(troop[2])] / self.metadata["render_fps"]
                    troop[0] += v[0]
                    troop[1] += v[1]

            troop = self._red_troops[i]
            if troop[3] > 0:
                v = self._king_blue_tower_center_location - troop[:2]
                dist = np.linalg.norm(v)
                if move_direction[1][i][1] > dist:
                    move_direction[1][i] = v/dist, dist
 
                v, dist = move_direction[1][i]
                if dist > TROOP_ATTACK_RANGE[int(troop[2])]:
                    v = v * TROOP_SPEEDS[int(troop[2])] / self.metadata["render_fps"]
                    troop[0] += v[0]
                    troop[1] += v[1]

        # An episode is done iff the agent has reached the target
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