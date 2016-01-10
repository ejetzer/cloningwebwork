#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import types, itertools

def compose(funcs):
    def final(arg):
        res = args
        for func in funcs:
            res = func(res)
        return res
    return final

def compositions(funcs):
    res = []
    for i in range(len(funcs)):
        for f in itertools.combinations(funcs, i):
            res.append(compose(f))
    return res

def pairs(seqs, fills):
    seqs = [list(seq) + [fill] for seq, fill in zip(seqs, fills)]
    repeat = 1 + len(seqs) == 1
    return itertools.product(*seqs, repeat=repeat)

class Thing:
    
    def __init__(self, val, errs={}, wrongs={}):
        self.val = val
        self.errs = errs
        self.wrongs = wrongs
    
    def propagate(self, other, name):
        # Get the operands
        a, b = self.val, getattr(other, 'val', other)
        # Get the wrong values
        lefts = self.wrongs.items()
        rights = getattr(other, 'wrongs', {}).items()
        arg_pairs = pairs([lefts, rights], [(a, []), (b, [])])
        # Get the error functions
        errs = self.errs.get(name.strip('_'), [])
        errs += getattr(other, 'errs', {}).get(name.strip('_'), [])
        err_pairs = itertools.product(errs, repeat=2)
        # Get the function
        func = getattr(self.val, name, lambda x: x)
        wrongs = {}
        for left, right in arg_pairs:
            left_val, left_desc = left
            right_val, right_desc = right
            for left_error, right_error in err_pairs:
                left_val, desc = left_error(left_val)
                left_desc += desc
                right_val, desc = right_error(right_val)
                right_desc += desc
                if (left_val, right_val) != (a, b):
                    wrong = func(left_val, right_val)
                    wrongs[wrong] = left_desc + right_desc
        val = func(a, b)
        return Thing(val, errs, wrongs)
    
    def __getattr__(self, name):
        func = getattr(self.val, name, None)
        if name.strip('_') in self.errs:
            return lambda s, o: s.propagate(o, name)
        else:
            raise AttributeError
