# Function definition is here
def changeme( mylist ):
   "This changes a passed list into this function"
   mylist = [1,2,3,4]; # This would assig new reference in mylist
   print ("Values inside the function: ", mylist)
   return

def changeme2( mylist ):
   "This changes a passed list into this function"
   #mylist.extend([1,2,3,4])
   mylist.extend('1234')
   print ("Values inside the function: ", mylist)
   return

# Now you can call changeme function
mylist = [10,20,30]
changeme( mylist )
print ("Values outside the function: ", mylist)
changeme2( mylist )
print ("Values outside the function: ", mylist)