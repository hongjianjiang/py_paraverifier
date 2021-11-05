from numpy import *
import os
print("图临接矩阵的行列数:")
n=int(input())#输入矩阵的行列数
print("请输入临接矩阵(行与行回车隔开 列与列空格隔开):")
a=[]
for i in range(0,n):#输入矩阵
         s=input().split(' ')
         s=[int(x) for x in s]
         a.append(s)
a=mat(a)#转化为可计算的矩阵
b=mat(zeros((n,n)))#设置累加矩阵
for i in range(1,n+1):#累加过程
	b+=a**n
if 0 in b:#判断是不是强连通
         print("图不是强连通")
else:
         print("图是强连通")
os.system("pause")