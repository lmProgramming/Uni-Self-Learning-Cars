def somefunc_cy(K):
    accum = 0
    for i in range(K):
        if i % 5:
            accum = accum + i
    return accum