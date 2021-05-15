import gym
import FormulaEnv
env = gym.make(id='FormulaEnv-v0',formula = "~(n[j]=T & x=True & n[i]=C)",filename = '../Protocol/n_mutualEx.json')
# env = FormulaEnv(id='FormulaEnv-v0',formula = "~(n[i]=T & x=True & n[i]=C & n[j]=C)",filename = '../Protocol/n_mutualEx.json')
env.reset()

env.step(env.action_space[0])
print(env.action_space)
for t in range(100):
    env.render()
env.close()

"Cache": "nat=>nat",
"Chan1": "nat=>nat",
"Chan2": "nat=>nat",
"Chan3": "nat=>nat",
"InvSet": "boolean",
"ShrSet": "boolean",
"ExGntd": "boolean",
"CurCmd": "MSG_CMD",
"CurPtr": "NODE",
"MemData": "DATA",
"AuxData": "DATA"


"Cache_State": "nat=>nat",
        "Cache_Data": "nat=>nat",
        "Chan1_Cmd": "nat=>nat",
        "Chan1_Data": "nat=>nat",
        "Chan2_Cmd": "nat=>nat",
        "Chan2_Data": "nat=>nat",
        "Chan3_Cmd": "nat=>nat",
        "Chan3_Data": "nat=>nat",
        "InvSet": "boolean",
        "ShrSet": "boolean",
        "ExGntd": "boolean",
        "CurCmd": "nat=>nat",
        "CurPtr": "NODE",
        "MemData": "DATA",
        "AuxData": "DATA"