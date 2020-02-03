import random
listOfPeople_reset = ['Roman','Bengi','Doggie']
listOfPeople = ['Roman','Bengi','Doggie']
listOfChores = ['dishes','vaccuming','sex','poop','bj','peeing']

def assign_user_to_action_and_delete():    
    for i in range(0,len(listOfChores)):
        if len(listOfPeople)<1:
            #print('**RESET**')
            listOfPeople.extend(listOfPeople_reset)
        randomChoreIndex = random.randrange(len(listOfChores))
        randomPeopleIndex = random.randrange(len(listOfPeople))
        print(listOfPeople[randomPeopleIndex] + ' is in charge of ' + listOfChores[randomChoreIndex])
        listOfPeople.pop(randomPeopleIndex)
        listOfChores.pop(randomChoreIndex)


def function2():
    listT = ['a','b','c','c','d','e','e']
    setT = set(listT)
    print(listT)
    print(setT)


#assign_user_to_action_and_delete()
function2()