import gym

env = gym.make('GridWorld-v1')
env.reset()
for t in range(100):
    env.render()
env.close()