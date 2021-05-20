'''
Created on May 20, 2021

@author: alienware
'''
def layer(iterable)->int:
    "Return the maximum depth of an iterable."
    if not isinstance(iterable, (list,tuple,set,frozenset,dict)):
        return 0
    else:
        return 1 + max(layer(sublayer) for sublayer in iterable)
        
    return 1+ max( layer(sublayer) for sublayer in iterable)    

def check(param,annot,value,check_history=''): 
    
    def check_iterable_base(annot,value,data_structure):
        #Fail if value is not a list
        if type(value) is not data_structure: 
            return False
        else:
            #annot has just one element-annotation, 
            #and any of the elements in the value list fails the element-annotation check 
            if len(annot) == 1: 
                #Base Case:
                
                for i in value: 
                    if type(i) != annot[0]:
                        return False
                return True 
            #annot has more than one element-annotation, and
            # the annot and value lists have a different number of elements, or
            # any element in the value list fails its corresponding element-annotation check
            else: 
                if len(annot) != len(value):
                    return False 
                else:
                    for i,j in zip(value, annot):
                        if not isinstance(i,j):
                            return False 
                    return True   
                
    def check_iterable(data_structures,annot,value,param):
        #Base Case:
        if layer(annot) == 1:
            return check_iterable_base(annot,value,data_structures)
        else:
            if layer(value) == 1:
                return check(param,annot[0],value[0],check_history='')
            else:
                return all(check(param,annot[0],i,check_history='') for i in value)
            
    if type(annot) == list: 
        return check_iterable(list,annot,value,param)

if __name__ == '__main__':
    param = 'x'
    annot = [[str,int]]
    value = [['a',1],['1',3],['3',3]]
    print(check(param,annot,value))