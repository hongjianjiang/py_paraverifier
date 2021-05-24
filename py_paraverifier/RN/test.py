import random

import gym
import FormulaEnv
env = gym.make(id='FormulaEnv-v0',formula = "~(n i=T  &  x=True  &  n j=C)",filename = '../Protocol/n_mutual.json')
env.reset()
print(env.action_space)
env.step(env.action_space[0])
# env.step(random.sample(env.action_space,1)[0])
# for i in range(100):
#     print('choice',random.sample(env.action_space,1))
print(env.action_space)
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
