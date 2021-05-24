import gym
env = gym.make('CartPole-v0')
for i_episode in range(20):
    observation = env.reset()  # 得到环境给出的初始反馈
    for t in range(100):
        env.render()
        print('ob:', observation)
        action = env.action_space.sample()  # 产生一个允许范围内的随机行动
        observation, reward, done, info = env.step(action) # 得到该次行动的反馈
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
env.close()