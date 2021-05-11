# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import torch
#!/usr/bin/python
import json


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open("n_mutualEx.json",encoding='utf-8') as f:
        data = json.load(f)
        name = data['name']
        vars = []
        for k,v in data['vars'].items():
            vars.append((k,v))
    print(data)
    print(name)
    print(vars)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
