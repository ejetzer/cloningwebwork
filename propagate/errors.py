#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def sign_error(x):
    return -x, 'You switched the sign of ${}$ to ${}$.'.format(x, -x)

def forgot_term(x):
    return 0, 'You forgot to add ${}$.'.format(x)

def forgot_factor(x):
    return 1, 'You forgot to multiply by ${}$.'.format(x)

def rounding_error(x):
    return round(x), 'You rounded ${}$ when you shouldn\'t.'.format(x)

basic_errors = {'add': [sign_error, forgot_term, rounding_error],
                'mul': [sign_error, forgot_factor, rounding_error]}
basic_errors['sub'] = basic_errors['add']
basic_errors['div'] = basic_errors['mul']
