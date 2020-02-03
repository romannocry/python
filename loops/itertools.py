from itertools import permutations

value = 'ABCD' #10 characters max memory
permutationsList = list(permutations(value,len(value)-2))
print(permutationsList)
print(len(permutationsList))

#4 = 24
#5 = 120
#6 = 720
