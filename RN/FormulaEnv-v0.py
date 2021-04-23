'''
author: Hongjian Jiang
Date:2021-4-23
'''
import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np


class FormulaEnv(object):
    """The main OpenAI Gym class. It encapsulates an environment with
    arbitrary behind-the-scenes dynamics. An environment can be
    partially or fully observed.
    The main API methods that users of this class need to know are:
        step
        reset
        render
        close
        seed
    When implementing an environment, override the following methods
    in your subclass:
        _step
        _reset
        _render
        _close
        _seed
    And set the following attributes:
        action_space: The Space object corresponding to valid actions
        observation_space: The Space object corresponding to valid observations
        reward_range: A tuple corresponding to the min and max possible rewards
    Note: a default reward range set to [-inf,+inf] already exists. Set it if you want a narrower range.
    The methods are accessed publicly as "step", "reset", etc.. The
    non-underscored versions are wrapper methods to which we may add
    functionality over time.
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
    def __init__(self):
        self.action_space = []
        self.observation_space = []
        self.seed()
        self.viewer = None
        self.state = None

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
    def _step(self, action): raise NotImplementedError
    def _reset(self): raise NotImplementedError
    def _render(self, mode='human', close=False): return
    def _seed(self, seed=None): return []
