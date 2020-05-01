def ifmax():
    '''Computes and returns the maximum finite float value. '''
    nn = 1024 # number of digits
    n1 =   53 # number of leading significant digits (binary)
    nz = nn - n1 # number of trailing insignificant digits (binary)

    return float(int('1' * n1 + '0' * nz, 2))
    
n=1023; nn=int('1' * n, 2); nm=2*int('1' * (n-1), 2); fm, fn=float(nm), float(nn);
print(bin(nn), bin(nm), '', nn, nm, '', fn, fm, '{0:014.7e}'.format(fn - fm), sep='\n')

eiffel = 2 ** 53 - 1 # i, full; also, "tallest" integer that "touches the ground" (has a binary 1 in the 1's place).
hollow = int('1' + '0' * 51 + '1', 2) # '0b10000000000000000000000000000000000000000000000000001'
hollow1 = hollow / 2 ** 52

for x in map(lambda x: random(), range(9)):
    print(x, repr(x), x == float(repr(x)), len(repr(x))-2)
    test = x == float(repr(x))
    if not test:
            print('****')
    else:
        print()


 
    
# FIND OUT HOW MANY DECIMAL DIGITS WE REALLY NEED
print(*filter(lambda x: not x[0], (mapchain(
    range(999),
    lambda x: random(),
    lambda x: (x, '{0:.15e}'.format(x)),
    lambda x: (x[0] == float(x[1]), len(x[1]) - 2) + x
))))
    



