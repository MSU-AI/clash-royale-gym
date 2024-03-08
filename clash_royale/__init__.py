from clash_royale.envs.clash_royale_env import ClashRoyaleEnv
from gym import make
from gymnasium.envs.registration import register

register(
     id="ClashRoyale",
     entry_point="clash_royale.envs:ClashRoyaleEnv",
     max_episode_steps=14400,
)
