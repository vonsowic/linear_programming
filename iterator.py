def forEach(iterable, function, condition=lambda x: True, recursion=True):
    result = iterable[:]
    for index, item in enumerate(result):
        if type(item) is list and recursion:
            res = forEach(item, function, condition)
            if res is not None:
                result[index] = res
        else:
            if condition(item):
                res = function(item)
                if res is not None:
                    result[index] = res
    return result

if __name__ == "__main__":
    l = ['a', 'b', ['c', 'd', ['e', 'f'], 'g', ['h', 'i', ['j', 'k', 'l'], 'm', 'n', 'o'], 'p'], 1, 2, 3]


    def cond(arg):
        if type(arg) is str:
            return True
        else:
            return False

    def assignRandomNumber(arg):
        import random
        return random.random()


    forEach(l, print)
    forEach(l, print, cond)
    forEach(l, print, recursion=False)
    nl = forEach(l, assignRandomNumber)
    print(nl)
