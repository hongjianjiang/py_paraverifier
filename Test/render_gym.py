# 首先，导入库文件（包括gym模块和gym中的渲染模块）
import gym
from gym.envs.classic_control import rendering


# 我们生成一个类，该类继承 gym.Env. 同时，可以添加元数据，改变渲染环境时的参数
class Test(gym.Env):
    # 如果你不想改参数，下面可以不用写
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 2
    }

    # 我们在初始函数中定义一个 viewer ，即画板
    def __init__(self):
        self.viewer = rendering.Viewer(600, 400)  # 600x400 是画板的长和框

    # 继承Env render函数
    def render(self, mode='human', close=False):
        # 下面就可以定义你要绘画的元素了
        line1 = rendering.Line((100, 300), (500, 300))
        line2 = rendering.Line((100, 200), (500, 200))
        # 给元素添加颜色
        line1.set_color(0, 0, 0)
        line2.set_color(0, 0, 0)
        # 把图形元素添加到画板中
        self.viewer.add_geom(line1)
        self.viewer.add_geom(line2)

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')


# 最后运行
if __name__ == '__main__':
    t = Test()
    while True:
        t.render()