def mean(iterable):
    values = tuple(iterable)
    return NaN() if not len(values) else precise_sum(values) / len(values)

