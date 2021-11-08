import gym
# env = gym.make('CartPole-v0')
env = gym.make('FormulaEnv-v0', filename='../Protocol/n_mutual.json')

# print(env.action_space)
for i_episode in range(50):
    observation = env.reset()
    # print(observation)
    for t in range(100):
        # env.render()
        # print(observation)
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
env.close()
