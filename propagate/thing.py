#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import types, itertools, functools

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
    repeat = 1 + (len(seqs) == 1)
    return itertools.product(*seqs, repeat=repeat)

class Thing:
    
    def __init__(self, val, errs={}, wrongs={}):
        self.val = val
        self.errs = errs
        self.wrongs = wrongs
    
    def propagate(self, other, name):
        # Left side arguments
        a = self.val
        lefts = self.wrong.items()
        errs = self.errs.get(name.strip('_'), [])
        # Right side arguments
        b = getattr(other, 'val', other)
        rights = getattr(other, 'wrongs', {}).items()
        errs += getattr(other, 'errs', {}).get(name.strip('_'), [])
        # Making iterators
        arg_pairs = pairs([lefts, rights], [(a, []), (b, [])])
        err_pairs = itertools.product(errs, repeat=2)
        # Get the function
        func = getattr(self.val, name, lambda x: x)
        wrongs = {}
        for args in arg_pairs:
            vals, descs = zip(*args)
            for errors in err_pairs:
                vals, ds = zip(*[e(a) for e, a in zip(errors, vals)])
                descs = map(lambda d: descs + d, ds)
                if vals != (a, b):
                    wrong = func(*vals)
                    wrongs[wrong] = itertools.chain(descs)
        val = func(a, b)
        return Thing(val, errs, wrongs)
    
    def __getattr__(self, name):
        if name.strip('_') in self.errs:
            f = functools.partialmethod(self.propagate, name=name)
            return f
        else:
            raise AttributeError
