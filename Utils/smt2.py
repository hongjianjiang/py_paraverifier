# coding=utf-8

from z3 import Solver, parse_smt2_string

SPLIT_CHAR = ','


class SMT2(object):
    def __init__(self, context):
        super(SMT2, self).__init__()
        self.context = context

    def check(self, smt2_formula, context=None):
        s = Solver()
        print(((context if context else self.context) + smt2_formula))
        s.add(parse_smt2_string((context if context else self.context) + smt2_formula))
        print("--------------\n")
        if str(s.check()) == "sat":
            print(s.model())
        print("--------------\n")
        return str(s.check())


