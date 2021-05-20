'''
Created on May 20, 2021

@author: alienware
'''
"""
annot is a lambda (or any function object) that is a predicate with one parameter and returning a value that can be interpreted as a bool. Fail if
annot has zero/more than one parameters: this is actually a bad/illegal annotation, not a failed annotation
Calling the lambda/function on value returns False
Calling the lambda/function on value raises an exception
"""

def check(param,annot,value,check_history=''): 
    if isinstance(annot, lambda):
        