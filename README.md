# py_paraverifier


coding recode
---
2021/4/21 生成ml的json文件
python2 gen.py -m mutualEx.m <br>
2021/4/22 编写paraverifier-type类型、图结构定义<br>
2021/4/23 RN：gym环境定义、引入z3py作为reward判定器<br>
2021/4/25 Type modification & implement of weakest precondition<br>
2021/4/26 实现smt求解器<br>
2021/4/27 实现parse模块
2021/5/11 gen修改支持多重变量定义
2021/5/12 translation翻译german协议

Directory Structure:
---
- Protocol stores the ocaml files of parameterized protocol<br>
- Utils is used for basic function<br>
     - gen: generator of the json file
     - invHold: the judger of the invHold rules and the weakest precondition
     - type:datatype for Paraverifier types
     - smt2: the smt2 checker 
- Graph is used for create the structure of formula's graph<br>
- RN is for files used in reinforce learning <br>


