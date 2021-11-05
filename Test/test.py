from graphviz import Digraph

dot = Digraph(comment='The Test Table')
# 添加圆点A,A的标签是Dot A
dot.node('A', '!(n[1]=C&n[2]=C',color='red')
# 添加圆点 B, B的标签是Dot B
dot.node('B', '!(x=True&n[1]=C&n[2]=T)',color='red')
# dot.view()
# 添加圆点 C, C的标签是Dot C
dot.node(name='C', label= '!(x=True&n[1]=C)',color='red')
dot.node('D', '!(n[1]=C&n[2]=T)')
dot.node('E', '!(x=True&n[2]=T)')
dot.node(name='F', label= '!(n[1]=C&n[2]=E&x=False)',color='red')
dot.node(name='H', label= '!(n[1]=C&n[2]=E)',color='red')
dot.node(name='G', label= '!(n[2]=E&x=False)')
dot.node(name='I', label= '!(n[1]=C&x=False)')
dot.node(name='i', label= '!(n[1]=T&n[2]=E & x=True)',color='red')
dot.node(name='M', label= '!(n[2]=E&x=True)',color='red')
dot.node(name='j', label= '!(n[2]=C&n[1]=C)',color='red')
dot.node(name='N', label= '!(n[1]=T&x=True)')
dot.node(name='h', label= '!(n[1]=T&n[2]=E)')
dot.node(name='a', label= '!(x=False&n[1]=E & n[2]=E)',color='red')
dot.node(name='b', label= '!(x=True&n[2]=C)',color='red')
dot.node(name='c', label= '!(x=False&n[1]=E)')
dot.node(name='d', label= '!(x=False&n[2]=E)')
dot.node(name='r', label= '!(n[1]=E&n[2]=E)',color='red')
dot.node(name='e', label= '!(n[2]=E&n[1]=C)',color='red')
dot.node(name='f', label= '!(n[2]=E&x=True&n[1]=T)',color='red')
dot.node(name='g', label= '!(n[1]=C&n[2]=C)',color='red')
dot.node(name='x', label= '!(n[2]=E&x=True)',color='red')
dot.node(name='y', label= '!(n[2]=E&n[1]=T)')
dot.node(name='z', label= '!(x=True&n[1]=T)')

# dot.view()
# 创建一堆边，即连接AB的两条边，连接AC的一条边。
dot.edges(['AB', 'BC', 'BD', 'BE','CF','FH','FG','FI','Hi','Hj','iN','iM','ih','Ma','Mb','ac','ad','ar','re','ef','eg','fx','fy','fz'])
# dot.view()
# 在创建两圆点之间创建一条边
# dot.edge('B', 'C', 'test')
# dot.view()

# 获取DOT source源码的字符串形式
print(dot.source)
dot.view()
dot.render('test-table.gv', view=True)
