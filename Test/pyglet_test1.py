import pyglet as p

#指定文件位置（相对位置、绝对位置）
path="xxx.mp3"
#将路径加载
music=p.media.load(path)
music.play()

if __name__ == '__main__':
    p.app.run()
