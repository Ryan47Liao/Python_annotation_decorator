'''
Created on May 12, 2021

@author: alienware
'''
import inspect

def param_arg_bindings(f,*args,**kargs):
    f_signature  = inspect.signature(f)
    bound_f_signature = f_signature.bind(*args,**kargs)
    for param in f_signature.parameters.values():
        if not (param.name in bound_f_signature.arguments):
            bound_f_signature.arguments[param.name] = param.default
    return bound_f_signature.arguments

def f(a,b:int)->int:
    return a+b 

if __name__ == '__main__':
    print(param_arg_bindings(f,b=2,a=1))