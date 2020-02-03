tup1 = ({'Name': 'Zara'}, {'Age': 7}, {'Class': 'First'})
tup2 = ({'Name': 'Zara'}, {'Age': 10}, {'Class': 'First'})


res = [j for j in tup2 if j not in tup1] 
print(res)

#objective is to
    #compare any datasets given a primary key that we can select(col name) or create one by concatenation
    #Check that the primary key selected is indeed a unique column
    #generate a list of changes/events

#depending if we are comparing 2 raw excel/csv files, one excel file to database extract