'''
# Submitter: bliao2 (Liao, Bowen)
# Partner: boiv (Vo, Boi Loc) 
We certify that we worked cooperatively on this programming assignment, 
according to the rules for pair programming 
'''

from goody import type_as_str
import inspect

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation:
    # Begin by binding the class attribute to True allowing checking to occur
    #   (only if the object's attribute self._checking_on is also bound to True)
    checking_on  = True
  
    # To check the decorated function f, begin by binding self._checking_on to True
    def __init__(self, f):
        self._f = f
        self._checking_on = True

    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''): 
        check_history += f'Checking:{annot}|{value}\n'
        def layer(iterable)->int:
            "Return the maximum depth of an iterable."
            if not isinstance(iterable, (list,tuple,set,frozenset,dict)):
                return 0
            else:
                return 1 + max(layer(sublayer) for sublayer in iterable)
                
            return 1+ max( layer(sublayer) for sublayer in iterable)   
        
        def ERROR(param, annot, value): 
            raise AssertionError(f' {param} failed annotation check(wrong type): value = {value}\n \
                        was type {type(value)} ...should be type {annot}  ')
        
        def check_iterable_base(annot,value,data_structure):
            #Fail if value is not a list
            if type(value) is not data_structure: 
                ERROR(param, annot, value)
            else:
                #annot has just one element-annotation, 
                #and any of the elements in the value list fails the element-annotation check 
                if len(annot) == 1: 
                    #Base Case:
                    # def check(self,param,annot,value,check_history=''): 
                    for i in value: 
                        self.check(param, annot[0], i) 
                        
                    
                #annot has more than one element-annotation, and
                # the annot and value lists have a different number of elements, or
                # any element in the value list fails its corresponding element-annotation check
                else: 
                    if len(annot) != len(value):
                        ERROR(param, annot, value)
                        
                    else:
                        for i,j in zip(value, annot):
                            if not isinstance(i,j):
                                ERROR(param, annot, value)
                        
                    
                        
        def check_iterable(annot,value,param):
            nonlocal check_history
            #Base Case:
            if layer(annot) == 1:
                #print(check_history)
                return check_iterable_base(annot,value,type(annot))
            else:
                # if layer(value) == 1:
                    # return self.check(param,annot[0],value[0],check_history=check_history)
                # else:
                [self.check(param,annot[0],i,check_history=check_history) for i in value]
                   
        def check_set(TYPE):
            assert type(value) == TYPE, f" {param} failed annotation check(wrong type): value = {value}\
  was type {type(value)} ...should be type {TYPE}"
            assert len(annot) == 1,f"{param} annotation inconsistency: set should have 1 item but had 2\
  annotation = {annot}"
            [isinstance(obj,list(annot)[0] ) for obj in value]
            
            
        def ERROR_STR(param, anot, value):
            error = f"'{param}' failed annotation check(str predicate: {annot}) args for evaluation: "
            for param in value:
                error += str(param) + '->' + str(value[param]) + ', '
            error = error[:-2]
            raise AssertionError(error)
        
        def ERROR_EXCEPTION(param, anot, value):
            raise AssertionError(f"'{param}' annotation check(str predicate: {annot}) raised exception \n \
        exception = {type(e).__name__}: {e} ")
            
            
        # MEGA Ifs
        if annot == None: 
            pass
        
        elif type(annot) == type:
            if not isinstance(value,annot): 
                ERROR(param, annot, value)
        elif type(annot) == list: 
            return check_iterable(annot,value,param)
            
        elif type(annot) == tuple: 
            return check_iterable(annot,value,param)
        
        elif isinstance(annot, dict):
            #When there are more than 1 pair of key/value
            assert len(annot) == 1,f"{param} annotation inconsistency: dict should have 1 item but had 2\
  annotation = {annot}"
            if not isinstance(value, dict):
                ERROR(param, annot, value)
            #Check if the key and value match the annots: value: 
            # check(param,annot[0],value[0],check_history=check_history)
            [self.check( param, list(annot.keys())[0], list(value.keys())[i] )  for i in range(len(value))]
            [self.check( param, list(annot.values())[0], list(value.values())[i] )  for i in range(len(value))]
                # if type( list(value.values())[i] ) != list(annot.values())[0]:
                    # return False 
            
        
        elif isinstance(annot, set): 
            return check_set(set)
        elif isinstance(annot,frozenset):
            return check_set(frozenset)
        elif inspect.isfunction(annot):
            assert len(inspect.getargspec(annot).args) == 1,\
            f'AssertionError: {param} annotation inconsistency: predicate should have 1 parameter but had {len(inspect.getargspec(annot).args)}\
              predicate = {annot}'
           
            try: 
                if annot(value) == False: 
                    ERROR(param, annot, value)
                
            except TypeError as e:
                ERROR_EXCEPTION(param, annot, value)
        elif type(annot) == str: 
            
            temp = '(lambda '
            for param in value: 
                if param in annot: 
                    if param == 'return':
                        param = '_' + str(param)
                    temp += param  + ','
            
            temp = temp[:-1] + ':' 
            temp += annot + ')' + '('
            
            for param in value: 
                if param in annot:
                    
                    temp += f"{repr(value[str(param)])},"
                    
            temp = temp[:-1] + ')'
            # print(value)
            # print(temp)
            
            try: 
                if eval(temp) == False: 
                    ERROR_STR(param, annot, value)
               
            except TypeError  as e:
                ERROR_EXCEPTION(param, annot, value)
           
        else:
            try: 
                if annot.__check_annotation__(self.check, param, value, check_history) == False: 
                    ERROR(param, annot, value)
                
            #case 1: no check annotation 
            
            #case 2:check annotation fail
            
            #case 3: check annotation raise other exceptions
            except AttributeError: 
                raise AssertionError(f'AssertionError: {param} annotation undecipherable: {annot}')
            except TypeError as e: 
                ERROR_EXCEPTION(param, annot, value)
            
            
            
        
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)

        # Begin by comparing check's function annotation with its arguments

        pass 
        
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        
        # Return the argument/parameter bindings in an OrderedDict (it's derived
        #   from a dict): bind the function header's parameters in its order
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        if self._checking_on == True:
            except_to_raise = None 
            try:
                # For each found annotation, check it using the parameter's value
                param_annot = self._f.__annotations__
                param_arg = param_arg_bindings()
                if 'return' in param_annot: 
                    param_arg['return'] = self._f(*args, **kargs)
                
                if len(param_annot) == 1 and type(param_annot.get(str(list(param_annot.keys())[0]))) == str: 
                    if  param_annot.get(list(param_annot.keys())[0]) is not None : 
                        self.check(param = list(param_annot.keys())[0] ,annot = param_annot[list(param_annot.keys())[0]],
                                          value = param_arg, check_history='')
                else:        
                              
                    for arg_name in param_arg:
                        
                        if  param_annot.get(arg_name) is not None : 
                            self.check(param = arg_name ,annot = param_annot[arg_name],
                                              value = param_arg[arg_name], check_history='')
                            except_to_raise = None
                                
            # On first AssertionError, print the source lines of the function and reraise 
            except AssertionError:
                raise
            # finally:
                # if except_to_raise is not None:
                    # raise except_to_raise
                    
        return self._f(*args, **kargs)



  
if __name__ == '__main__':   
     
    # def f(x:'x>0'): pass
    # f = Check_Annotation(f)
    # f('a')
    
    # def f(x,y)->'_return < x or _return < y': return x + y
    # f = Check_Annotation(f)
    # f(5,3)
    
    # def f(x : {Check_All_OK(str,lambda x : len(x)<=3):Check_Any_OK(str,int)}): pass
    # f = Check_Annotation(f)
    # f({'a' : 1, 'b': 2, 'c':'c'}) 
    # # an example of testing a simple annotation 
    # def f(x : [int]):pass
    # f = Check_Annotation(f)   
    # f([1,'b']) 
    #
    # def f(x : frozenset([str])): pass
    # f = Check_Annotation(f)   
   # f(frozenset({'a','b'}))
    #driver tests
    
    import driver
    driver.default_file_name = 'bscp4S21.txt'
    # driver.default_show_exception= True
    # driver.default_show_exception_message= True
    # driver.default_show_traceback= True
    driver.driver()
