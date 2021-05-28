#author:Hongjian Jiang

import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np
import json
import re
from z3 import Solver
from gym.utils.smt2 import  *
from gym.utils.Paraverifier import  *
import numpy as np

class FormulaEnv(gym.Env):
    """
    Description:
        A pole is attached by an un-actuated joint to a cart, which moves along
        a frictionless track. The pendulum starts upright, and the goal is to
        prevent it from falling over by increasing and reducing the cart's
        velocity.

    Source:
        This environment corresponds to the version of the cart-pole problem
        described by Barto, Sutton, and Anderson

     Observation:
        Type:Discrete(2)
        Num     Observation
        0       SAT
        1       UNSAT
    Actions:
        Type:Discrete(index)
        Num     Action
        0       Choose first literal
        1       Choose second literal
        ...
        index-1 Choose last literal
    Reward:
        # Reward of 0 is awarded if the agent reached the flag of SAT.
        # Reward of -1 is awarded if the agent reached the flag of UNSAT
        When the invHold3 meet between the formula and the guarded command, the reward set positive
        When the invHold1 meet between the formula and the guarded command, the reward set positive
        When the literal occurs in the formula, the reward set positive
        When the initial satisfies the formula, the reward set positive
        When the guard of the guarded commands, the reward set negative

    Starting State:
        The initial state is the original CNF formula.

    Episode Termination:
        The chosed formula is Unsat checked by the SAT solver.
    """
    def __init__(self,filename):
        self.smt2 = SMT2(filename)
        self.paraverif = load_system(filename)
        self.formula = self.paraverif.invForm
        # print(self.formula)
        self.relation = self.paraverif.relation
        self.allinvs = self.paraverif.allinvs
        self.queue = []
        invs = []
        for f in self.formula:
            for f1 in self.paraverif.searchInvFromGivenFormula(f):
                invs.append(f1)
                self.queue.append(f1)
            invs.append(f)
        len1 = len(self.paraverif.states)*2 + 2
        low = np.zeros(len1)
        high = np.ones(len1)
        self.observation_space = spaces.Box(low,high,dtype=np.float32)
        self.action_space = spaces.Discrete(self.paraverif.max)
        self.seed()
        self.viewer = None
        self.state = None
        self.originalInv = []

    def seed(self,seed = None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _close(self):
        pass

    def step(self, action):
        reward=0
        curform = self.queue[0] # ~(n i=T & x=True & n j=C)
        curfs = re.findall(r'~\((.*)\)', curform, re.S)[0] # n i=T & x=True & n j=C
        temp = curfs.split('&')
        curfsl = []
        for i in temp:
            curfsl.append(i.strip())
        if action> len(curfsl)-1:
            print(curform,'1')
            form = "~("+ curfs + ")"
        elif len(curfsl) == 1:
            print(curform,'2')
            form = "~("+ curfs + ")"
            pass
        else:
            print(curform,'3')
            curfsl.remove(curfsl[action])
            form = "~("+" & ".join(curfsl)+")"
        print(form)
        self.queue.remove(self.queue[0])
        nfs = self.paraverif.searchInvFromGivenFormula(form) # new formulas
        print('nfs:',nfs)
        self.queue.append(form)
        for i in nfs:
            self.queue.append(i)
        cinit = self.paraverif.initSatInv(form)
        if cinit == 'sat': #initial condition satisfies the formula
            reward -= 10
        list1 = re.findall(r'[(](.*)[)]', form, re.S)[0].split('&')
        for l in list1: # keep the original inv
            if l.strip() in self.originalInv:
                reward += 3
        cinv1,cinv3 =  self.paraverif.judgeInv(form) # inv1 & inv3 hold
        if self.paraverif.judgeGuard2Formula(form): # guard equals to inv
            reward -= 10
        reward = reward + cinv1 * 3 + cinv3 * 3
        formulastr = "".join(self.formula)
        done = bool(
            '&' not in formulastr
        )
        print('--------')
        return self.paraverif.transform2onehot(form),reward,done,{}
        # raise NotImplementedError

    def reset(self):
        # print("reset :" , self.formula)
        print('===========')
        return self.paraverif.transform2onehot(self.formula[0])

    def _render(self, mode='human', close=False): return

    def _seed(self, seed=None): return []


