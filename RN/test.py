import random

import gym
import FormulaEnv
env = gym.make(id='FormulaEnv-v0',filename = '../Protocol/n_mutual.json')
env.reset()

print('action_space:', env.action_space)
print('observation_space:',env.observation_space)
action = env.action_space.sample()
print(env.step(action))
print(env.action_space)
for i_episode in range(20):
    observation = env.reset()
    for t in range(100):
        # env.render()
        print(observation)
        action = env.action_space.sample()
        print('action:',action)
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
env.close()
# env.step(random.sample(env.action_space,1)[0])
# for i in range(100):
#     print('choice',random.sample(env.action_space,1))
# print(env.action_space)
# for i_episode in range(20):
#     observation = env.reset()
#     for t in range(100):
#         env.render()
#         print(observation)
#         action = random.sample(env.action_space,1)[0]
#         observation, reward, done, info = env.step(action)
#         if done:
#             print("Episode finished after {} timesteps".format(t+1))
#             break
env.close()
