import gym  # 导入包
env = gym.make('CartPole-v0') # 构建一个名字叫“CartPole-v0”的Gym场景
env.reset() # 初始化场景
for _ in range(200): #
    env.render()  # 画出当前场景情况
    env.step(env.action_space.sample()) # 给环境中Agent一次命令，并让环境演化一步
env.close()  # 关闭环境