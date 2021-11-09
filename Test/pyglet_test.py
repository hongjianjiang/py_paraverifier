#使用import语句导入pyglet库
import pyglet as p

#创建pyglet.window.Window实例，使用myWindow变量命来接收（类首字母大写）
#参数对应着窗口的长、宽、标题等等。
myWindow = p.window.Window(1000,500,caption="我的窗口！！！！！！！")
#创建pyglet.text.Lable实例，使用label变量名进行接收
#参数对应设置标签上显示的内容，后两个参数显示在窗口的坐标为（250,250）
l = ['~(n i=crit & n j=crit)', '~(x=True & n j=crit)', '~(n j=crit & n i=exit)', '~(x=True & n i=exit)', '~(n i=exit & n j=exit)']
label=p.text.Label(str(l),x=20,y=250)

#使用修饰器@myWindow.event将后面定义的on_draw()方法关联到窗口对象game_win
@myWindow.event
def on_draw():
    #清除窗口中所有内容，窗口默认黑色背景
    myWindow.clear()
    #调用文本标签对象label的draw()方法，在窗口中绘制出文本标签的外观
    label.draw()

if __name__ == '__main__':
    #调用pyglet.app.run()方法让程序进入Pyglet的默认事件循环
    p.app.run()

