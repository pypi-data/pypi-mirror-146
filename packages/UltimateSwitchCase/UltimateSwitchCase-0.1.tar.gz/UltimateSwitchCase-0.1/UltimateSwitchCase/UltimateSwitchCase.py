# var is the variable you want to iterate trough
# dict is a dictionary that has as keys the possible values of var
# and as elements the wanted return


def switch(var, dict):

    chad = list(dict)

    for i in chad:
        if var == i:
            return dict[i]
    return 0
