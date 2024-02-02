import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces

MAX_NUMBER_TROOPS = 32
MAX_TROOP_TYPES = 32
MAX_TROOP_HEALTH = 1000

KING_TOWER_RANGE = 7.0
KING_TOWER_DAMAGE = 144
KING_TOWER_HEALTH = 6408

TROOP_COLORS = [(153, 255, 51), (255, 102, 155)]
TROOP_SIZES = [0.5, 0.4]
TROOP_RANGES = [0.8, 5]
TROOP_HEALTH = [888, 403]
TROOP_DAMAGE = [195, 157]

SQUARES_PER_HP = (0.5 / 100)
HEALTH_BAR_HEIGHT = 0.15


def calculate_health_bar_length(max_health):
    return np.log10(max_health/100 + 1)

def draw_rectangle_from_center(canvas, color, location, size):
    pygame.draw.rect(
            canvas,
            color,
            pygame.Rect(
                location - size / 2,
                size,
            ),
        )
    
def draw_health_bar(canvas, health_bar_color, center, health, max_health, pix_square_size):
    draw_rectangle_from_center(canvas, health_bar_color, 
                            center * pix_square_size,
                            [(health / max_health) * calculate_health_bar_length(max_health), 
                             HEALTH_BAR_HEIGHT] * pix_square_size)

def draw_king_tower(canvas, side, location, pix_square_size, health):
    color = (190, 0, 0) if side == 'red' else (0,0,190)
    health_color = (155, 0, 0) if side == 'red' else (0, 0, 155)
    direction = [0, -0.7] if side == 'red' else [0, 0.7]
    draw_rectangle_from_center(canvas, (0, 0, 0), location * pix_square_size, pix_square_size)
    draw_rectangle_from_center(canvas, color, location * pix_square_size, pix_square_size*0.9)
    draw_health_bar(canvas, health_color, 
                    location + direction,
                    health, KING_TOWER_HEALTH, pix_square_size)

def draw_troop(canvas, troop, health_bar_color, pix_square_size):
    #   draws using circles
    troop_type = int(troop[2])
    radius = TROOP_SIZES[troop_type]
    pygame.draw.circle(
        canvas,
        TROOP_COLORS[troop_type],
        troop[:2] * pix_square_size,
        radius * pix_square_size[1],
    )
    draw_health_bar(canvas, health_bar_color,
                    [troop[0], troop[1] - radius - 0.15],
                    troop[3],
                    TROOP_HEALTH[troop_type],
                    pix_square_size)
    
class ArenaEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 8}

    def __init__(self, render_mode=None, width=8, height=18):
        self.width = width  # The size of the square grid
        self.height = height
        self.window_size_width = 360  # The size of the PyGame window width
        self.window_size_height = 810  # The size of the PyGame window height

        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        self.observation_space = spaces.Dict(
            {
                "blue-troops": spaces.Box(0, np.tile(np.array([width, height, MAX_TROOP_TYPES, MAX_TROOP_HEALTH]), (MAX_NUMBER_TROOPS,1,)), shape=(MAX_NUMBER_TROOPS, 4,), dtype=np.float32),
                "red-troops": spaces.Box(0, np.tile(np.array([width, height, MAX_TROOP_TYPES, MAX_TROOP_HEALTH]), (MAX_NUMBER_TROOPS,1,)), shape=(MAX_NUMBER_TROOPS, 4,), dtype=np.float32),
            }
        )

        # We have 4 actions, corresponding to "right", "up", "left", "down"
        self.action_space = spaces.Discrete(4)


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
        return {"blue-troops": self._blue_troops, "red-troops": self._red_troops}
    
    def _get_info(self):
        return {
        }
    
    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        self._king_blue_tower_center_location = np.array([self.width//2, self.height-1])
        self._king_red_tower_center_location = np.array([self.width//2, 1])

        self._king_blue_tower_health = KING_TOWER_HEALTH
        self._king_red_tower_health = KING_TOWER_HEALTH

        self._king_KING_TOWER_RANGE = KING_TOWER_RANGE

        self._blue_troops = np.zeros((MAX_NUMBER_TROOPS,4,), dtype=np.float32)
        self._red_troops = np.zeros((MAX_NUMBER_TROOPS,4,), dtype=np.float32)
        
        #Test
        self._blue_troops[0] = [3.2, 5.6, 0, 150]
        self._red_troops[0] = [5.8, 3.76, 1, 100]
        self._red_troops[1] = [1.3, 10.7, 1, 100]

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info
    
    def step(self, action):
        move_direction = [[[None, 10000] for j in range(MAX_NUMBER_TROOPS)] for i in range(2)]

        for i in range(MAX_NUMBER_TROOPS):
            if self._blue_troops[i][3] <= 0:
                continue

            min_j = min_v = None
            min_dist = 1000
            for j in range(MAX_NUMBER_TROOPS):
                if self._red_troops[j][3] <= 0:
                    continue
                v = (self._red_troops[j] - self._blue_troops[i])[:2]
                dist = np.linalg.norm(v)
                if min_dist > dist:
                    min_j = j
                    min_dist = dist
                    min_v = v / dist
                    
            if min_j is None:
                break

            move_direction[0][i] = min_v, min_dist
            if move_direction[1][min_j][1] > min_dist:
                move_direction[1][min_j] = (-1 * min_v), min_dist

        for i in range(MAX_NUMBER_TROOPS):
            troop = self._blue_troops[i]
            if troop[3] > 0:
                v = self._king_red_tower_center_location - troop[:2]
                dist = np.linalg.norm(v)
                if move_direction[0][i][1] > dist:
                    move_direction[0][i] = v / dist, dist

                v, dist = move_direction[0][i]
                if dist > TROOP_RANGES[int(troop[2])]:
                    v = v * 0.1
                    troop[0] += v[0]
                    troop[1] += v[1]

            troop = self._red_troops[i]
            if troop[3] > 0:
                v = self._king_blue_tower_center_location - troop[:2]
                dist = np.linalg.norm(v)
                if move_direction[1][i][1] > dist:
                    move_direction[1][i] = v/dist, dist

                v, dist = move_direction[1][i]
                if dist > TROOP_RANGES[int(troop[2])]:
                    v = v * 0.1
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
            self._king_KING_TOWER_RANGE * pix_square_size_height,
        )
        pygame.draw.circle(
            canvas,
            (211, 211, 211),
            self._king_red_tower_center_location * pix_square_size,
            self._king_KING_TOWER_RANGE * pix_square_size_height,
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

        draw_king_tower(canvas, "red",
                        self._king_red_tower_center_location, 
                        pix_square_size, self._king_red_tower_health)


        for troop in self._blue_troops:
            if troop[3] > 0:
                draw_troop(canvas, troop, (0,0,155), pix_square_size)
                
        for troop in self._red_troops:
            if troop[3] > 0:
                draw_troop(canvas, troop, (155,0, 0), pix_square_size)


        draw_king_tower(canvas, "blue", 
                        self._king_blue_tower_center_location, 
                        pix_square_size, self._king_blue_tower_health)

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