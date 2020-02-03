List1 = [-1,-2,-3]
print(List1)
List1.extend(range(0,5,1))
List1.extend('567')
print(List1)
for element in List1:
    print(element)

print("**************")
for i in range(len(List1)):
    print(List1[i])
print(List1)

