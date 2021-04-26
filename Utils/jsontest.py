import json


with open('../Protocol/n_mutualEx.json') as f:
    data = json.load(f)

print(data['states'])
print(data['vars'])

