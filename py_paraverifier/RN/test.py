import gym
import FormulaEnv
env = gym.make(id='FormulaEnv-v0',formula = "~(n[j]=T & x=True & n[i]=C)",filename = '../Protocol/n_mutualEx.json')
# env = FormulaEnv(id='FormulaEnv-v0',formula = "~(n[i]=T & x=True & n[i]=C & n[j]=C)",filename = '../Protocol/n_mutualEx.json')
env.reset()

env.step(env.action_space[0])
print(env.action_space)
for t in range(100):
    env.render()
env.close()