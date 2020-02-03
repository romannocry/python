import itertools
# import requests
import json

# Python code to find the difference in 
# keys in two dictionary 

api = 'https://jsonplaceholder.typicode.com/todos/'  
#response = requests.get(api)

#print(response)

# Initialising dictionary  
dict1= {'igg':'2', 'key2':'For', 'key3':'geeks'} 
dict2= {'key1':'Geeks', 'key2:':'Portal'} 
  
diff = set(dict2) - set(dict1) 
  
# Printing difference in 
# keys in two dictionary 
# print(diff) 
a = [{'igg': '1','name':'x'}, {'rc': 'rc1'}]
b = [{'igg': '1','name':'y'}, {'rc': 'rc2'}]
#for x_values, y_values in zip(x.iteritems(), y.iteritems()):
#    if x_values == y_values:
#        print 'Ok', x_values, y_values
#    else:
#        print 'Not', x_values, y_values

a_minus_b = [item for item in a if item not in b]
b_minus_a = [item for item in b if item not in a]
sym_diff = list(itertools.chain(a_minus_b,b_minus_a))
 
print(b_minus_a)
print(a_minus_b)
# event_date,igg,name,field_change,prev_value,new_value