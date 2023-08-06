from gym.envs.registration import register

register(
    id='open-v0',
    entry_point='gym_rat_runner.envs:OpenEnv',
    max_episode_steps=200
)

register(
    id='maze-v0',
    entry_point='gym_rat_runner.envs:MazeEnv',
    max_episode_steps = 200
)

register(
    id='maze-stoc-v0',
    entry_point='gym_rat_runner.envs:MazeEnv',
    max_episode_steps = 200,
    nondeterministic = True
)