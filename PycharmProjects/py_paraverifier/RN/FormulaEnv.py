#author:Hongjian Jiang

import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np
import json
import re
from z3 import Solver


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
        Reward of 0 is awarded if the agent reached the flag of SAT.
        Reward of -1 is awarded if the agent reached the flag of UNSAT
    Starting State:
        The initial state is the original CNF formula.
    Episode Termination:
        The chosed formula is Unsat checked by the SAT solver.
    """
    def __init__(self,formula,filename):
        result = re.findall(r'[(](.*)[)]', formula.replace(" ",""), re.S)
        self.CNF = result[0]
        self.formula = formula
        self.action_space = self.CNF.split('&')
        self.observation_space = ["sat","unsat"]
        self.seed()
        self.viewer = None
        self.state = None
        self.smt2 = SMT2(filename)

    def seed(self,seed = None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    # Override in SOME subclasses
    def _close(self):
        pass

    # Set these in ALL subclasses
    action_space = None
    observation_space = None

    # Override in ALL subclasses
    def _step(self, action):
        list1 = self.CNF.split('&')
        if list1.index(action) == 0 :
            self.formula ="~("+"&".join(list1[1:])+")"
            self.action_space.remove(action)
        else:
            if action in list1:
                list1.remove(action)
                self.formula = "~("+"&".join(list1)+")"
                self.action_space.remove(action)
                print(self.formula)
        obs =  self.smt2.check(self.formula)
        if obs == "unsat":
            reward = -1
        else:
            reward = 0
        done = False
        return obs,reward,done,{}
        # raise NotImplementedError
    def _reset(self): 
        print("orignial formula :" , self.formula)
        # raise NotImplementedError
    def _render(self, mode='human', close=False): return
    def _seed(self, seed=None): return []


class SMT2(object):
    '''
    Given the protocol's json file address and the invariant
    Json file servers as the context of the z3 environment
    Invariant servers as the assertation
    SMT2 returns the bool value whether it is true or not
    '''
    def __init__(self, file):
        super(SMT2, self).__init__()
        self.file = file

    def getStringInFormula(self,formula):
        result = re.findall(r'[(](.*)[)]', formula, re.S)
        return result[0]

    def getPrefixInArray(self,formula):
        if '[' in formula:
            result = re.findall(r"(.*?)\[.*\]+", formula, re.S)
            res = result[0]
        else:
            res= formula
        return res

    def check(self, smt2_formula):
        s = Solver()
        nsf = self.getStringInFormula(smt2_formula).replace("(","").replace(")","")# the negation of the smt2 formula
        with open(self.file) as f:
            data = json.load(f)
            states = data['states']
            boollist = ["True","False"]
            vars = data['vars']
            str_tmp = ""
            str_tmp1 = ""
            for i in states:
                str_tmp += " "+ i
            str_states = '(declare-datatypes () ((state' + str_tmp + ')))'
            for i in vars:
                if '=>' in vars[i]:
                    str_tmp1 += ' (declare-const '+ i +' (Array Int state))'
                elif 'bool' in vars[i]:
                    str_tmp1 += ' (declare-const '+ i + ' Bool)'
            str_context = str_states + str_tmp1
        str_formula = " (assert ("
        if '&' in nsf:
            str_formula += 'and'
            if '[' in nsf:
                str_context += ' (declare-const i Int)'
            for i in (nsf.replace(' ', '').split('&')):
                l1 = i.split('=')
                str_formula +=' (='
                for j in l1:
                    if j in states:
                        str_formula += " " + j
                    elif j in boollist:
                        str_formula += " " + j.lower()
                    elif self.getPrefixInArray(j) in vars:
                        if j.count('[') > 0:
                            str_formula += " (select "+self.getPrefixInArray(j) + ' i)'
                        else:
                            str_formula += " "+j
                str_formula += ')'
            str_formula += '))'
        else:
            if '[' in nsf:
                str_context += ' (declare-const i Int)'
            for i in (nsf.replace(' ', '').split('&')):
                l1 = i.split('=')
                str_formula += '='
                for j in l1:
                    if j in states:
                        str_formula += " " + j
                    elif self.getPrefixInArray(j) in vars:
                        if j.count('[') > 0:
                            str_formula += " (select " + self.getPrefixInArray(j) + ' i)'
                str_formula += ')'
            str_formula += ')'
        # print(str_context+str_formula)
        s.from_string(str_context+str_formula)
        # s.add(parse_smt2_string((context if context else self.context) + smt2_formula))
        # print("--------------\n")
        # if str(s.check()) == "sat":
        #     print(s.model())
        # print("--------------\n")
        return str(s.check())