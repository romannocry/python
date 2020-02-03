# Creating a List with  
# mixed type of values 
# (Having numbers and strings) 
List = [1, 2, 'Geeks', 4, 'For', 6, 'Geeks'] 
#print("\nList with the use of Mixed Values: ") 
List2= ['r','r','b','b','r']
ListExt = ['X','Y','Z']
print("***********")
print(set)
print(List2)
print(List2[1:2])
List2.append('lol')
List2.extend('boo')
print(List2)
print(List2[-4])
print(List2.count('r'))
List2.insert(0,"boom")
print(List2)
#print("*****ITERATE THROUGH LIST******")
#for element in List2:
#    print(element)

print("*****ITERATE THROUGH EXTENDED LIST******")
List2.extend(ListExt)
print(List2)

print("*****Delete a range LIST with step******")
del List2[0:len(List2):2]
print(List2)

print("*****Clear list******")
List2.clear()
print(List2)
List2.extend('123')
print("extension")
print(List2)
List2.append(123)
List2.append('123')
print(List2)
List2.reverse()
List2.pop(len(List2)-1)
print(List2)
print(List2[0:2])
List2[0:2] = []
print(List2)
print(List2*2)

List3 = []
List3.append(2)
print(List3)
print(List3*List3[0])
