from gymnasium.envs.registration import register

register(
     id="clash-royale",
     entry_point="clash_royale.envs:ClashRoyaleEnv",
     max_episode_steps=14400,
)
