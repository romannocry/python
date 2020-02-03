import time;  # This is required to include time module.
from itertools import starmap

ticks = time.time()
#print ("Number of ticks since 12:00am, January 1, 1970:", ticks)

localtime = time.localtime(time.time())
#print ("Local current time :", localtime)

def addString(val):
    val = val + 'yo'
    return val

def addInt(val):
    val += 100
    return val

def add(x, y):
    return x + y

def add3(x, y, z):
    return x + y + z

listT = 'a,b,c,d,e,f'.split(',')
print(listT)

list2 = list(map(addString,listT))
print(list2)

ListN = [1,2,3,4]
print(ListN)
listN2 = list(map(addInt,ListN))

print(listN2)
#test tuple - to be reviewed
listTuple = set(map(tuple,['roman','bengi']))
print(listTuple)

#list comprehension
testList = [add(x, 1000) for x in ListN]
print(testList)
#anonymouse function
testList2 = list(map(lambda x: add3(x, 2, 3), [1, 2, 3]))
print(testList2)
#map
def addNew(t):
        x, y, z = t
        return x+y+z

testList3 = list(map(addNew, [(x, 2, 10) for x in [1,2,3]]))
print(testList3)

#starmap - NOPE
# starmap(pow, [(2,5), (3,2), (10,3)]) --> 32 9 1000
print("pow")
testList4 = list(starmap(pow, [(1, 2, 3), (4, 5, 6)]))
print(testList4)
List5 = [(1, 2, 3), (4, 5, 6)]
List6 = [(2, 1), (4, 5)]
print(List5)
testList5 = list(starmap(pow,List6))
print(testList5)