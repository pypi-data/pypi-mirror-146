def printer(*args,newln=False,operator=","):
    brek = (' {} '+operator+'')*len(args) if newln == False else ' {} \n'*len(args)
    print(brek.format(*args)[:-1])