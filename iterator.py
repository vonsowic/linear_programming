def forEach(iterable, function, condition=lambda x: True, recursion=True):
    result = iterable[:]
    for index, item in enumerate(result):
        if type(item) is list and recursion:
            res = forEach(item, function, condition)
            if res is not None:
                result[index] = res
        else:
            try:
                tmp_condition = condition(item)
            except TypeError:
                tmp_condition = condition(result, index)

            if tmp_condition:
                try:
                    res = function(item)
                except TypeError:
                    res = function(result, index)

                if res is not None:
                    result[index] = res

    return result
