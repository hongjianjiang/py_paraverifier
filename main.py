# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import torch
#!/usr/bin/python
import json

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

class A():
    def __init__(self):
        pass

    def _print(self):
        print(self.ty)


class B(A):
    def __init__(self,t):
        self.ty = t


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    f = open('test.json', 'r')
    content = f.read()
    a = json.loads(content)
    print(type(a))
    print(a)
    f.close()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
