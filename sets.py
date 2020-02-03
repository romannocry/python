set1 = set(['Bengi','Roman','Roman','David'])
set2 = set(['Roman','Bengi',6])


############ Actions END #########
print("****SET****")
#prints unique values
print(str(set1)+' of size '+str(len(set1)))
print(str(set2)+' of size '+str(len(set2)))
print("******UNION*****")
set3 = set1.union(set2)
#prints unique values of a union of sets
print(str(set3)+' of size '+str(len(set3)))
print("***********")
print("******INTERSECT*****")
set4 = set1.intersection(set2)
#prints unique values of a union of sets
print(str(set4)+' of size '+str(len(set4)))
print("***********")
print("******INTERSECT INVERSED/SYMMETRIC DIFF*****")
set5 = set1.symmetric_difference(set2)
#prints unique values of a union of sets
print(str(set5)+' of size '+str(len(set5)))
print("***********")
print("******DIFF*****")
set6 = set1.difference(set2)
#prints unique values of a union of sets
print(str(set6)+' of size '+str(len(set6)))
print("***********")

print("******calculus*****")
setA = set (['A','B','C','D','E'])
setB = set (['D','E'])
##############Actions#############
setA.add('F')
setA.remove('A')
print(setA>setB)
print(setB>setA)
print(setB.issubset(setA))
print(setA.isdisjoint(setB))
print("***********")
