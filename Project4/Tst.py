'''
Created on May 19, 2021

@author: alienware
'''
"""
AssertionError: 'x' annotation predicate(<function <lambda> at 0x0022C540>) raised exception
  exception = TypeError: '>' not supported between instances of 'str' and 'int'
list[1] check: <function <lambda> at 0x0022C540>
"""

def check_f(param,annot,value):
    try: 
        annot(value) #Expecting int/float:
    except TypeError as E:
        assert False ,f"{param} annotation predicate({value}) raised exception \n\
        exception = {E} " 


if __name__ == '__main__':
    # f(x:[lambda x : x>0]):... called as f([1,0]) t
    check_f('X', lambda x: x>0, [1,0])
