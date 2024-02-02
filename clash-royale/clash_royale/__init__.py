from gymnasium.envs.registration import register

register(
     id="clash_royale/Arena-v0",
     entry_point="clash_royale.envs:ArenaEnv",
     max_episode_steps=300,
)