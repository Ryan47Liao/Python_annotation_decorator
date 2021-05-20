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
        
        def check_iterable(data_structure):
            if type(value) is not data_structure: 
                return False
            else: 
                if len(annot) == 1: 
                    for i in value: 
                        if type(i) != annot[0]:
                            return False
                    return True 
                else: 
                    if len(annot) != len(value):
                        return False 
                    else:
                        for i,j in zip(value, annot):
                            if not isinstance(i,j):
                                return False 
                        return True   
                   
        def check_set(TYPE):
            assert type(value) == set, f" {param} failed annotation check(wrong type): value = {value}\
  was type {type(value)} ...should be type {TYPE}"
            assert len(annot) == 1,f"{param} annotation inconsistency: set should have 1 item but had 2\
  annotation = {annot}"
            return all([isinstance(obj,list(annot)[0] ) for obj in value])
        
        
        if annot == None: 
            return True
        
        elif type(annot) == type:
            return isinstance(value,annot)
        elif type(annot) == list: 
            return check_iterable(list)
        elif type(annot) == tuple: 
            return check_iterable(tuple)
        elif isinstance(annot, dict):
            #When there are more than 1 pair of key/value
            assert len(annot) == 1,f"{param} annotation inconsistency: dict should have 1 item but had 2\
  annotation = {annot}"
            #Check if the key and value match the annots: value: 
            if type( value.keys()[0] ) != annot.keys()[0]:
                return False
            if type( value.values()[0] ) != annot.values()[0]:
                return False 
            return True 
        elif isinstance(annot, set): 
            return check_set(set)
        elif isinstance(annot,frozenset):
            return check_set(frozenset)
        else:
            pass
             
  
            
            
        
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
                for arg_name in param_arg:
                    
                    if  param_annot.get(arg_name) is not None: 
                        assert self.check(param = arg_name ,annot = param_annot[arg_name],
                                          value = param_arg[arg_name], check_history=''),\
                        f' {arg_name} failed annotation check(wrong type): value = {param_arg[arg_name]}\n \
                        was type {type(param_arg[arg_name])} ...should be type {param_annot[arg_name]}  '
                        except_to_raise = None
                            
            # On first AssertionError, print the source lines of the function and reraise 
            except AssertionError:
                # print(80*'-')
                # for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
                    # print(l.rstrip())
                # print(80*'-')
                except_to_raise = AssertionError(f' {arg_name} failed annotation check(wrong type): value = {param_arg[arg_name]}\n \
                        was type {type(param_arg[arg_name])} ...should be type {param_annot[arg_name]}  ') 
            finally:
                if except_to_raise is not None:
                    raise except_to_raise
        
        return self._f(*args, **kargs)



  
if __name__ == '__main__':     
    # an example of testing a simple annotation  
    def f(x : [[str]]): pass
    f = Check_Annotation(f)   
    try:  
        f([['a','b'],['c','d']])
    except Exception as E:
        print(Exception)
        print(E) 
    #driver tests
    import driver
    driver.default_file_name = 'bscp4S21.txt'
    # driver.default_show_exception= True
    # driver.default_show_exception_message= True
    # driver.default_show_traceback= True
    driver.driver()
