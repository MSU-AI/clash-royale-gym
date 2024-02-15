from gymnasium.envs.registration import register

register(
     id="clash_royale/ClashRoyale",
     entry_point="clash_royale.envs:ClashRoyaleEnv",
     max_episode_steps=3000,
)