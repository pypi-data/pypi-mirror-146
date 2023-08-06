def powerset(arg):
    result = [[]]
    for x in arg:
        newsubset = [subset + [x] for subset in result]
        result.extend(newsubset)
    return result
