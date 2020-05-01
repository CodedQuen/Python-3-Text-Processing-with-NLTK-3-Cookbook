def arrayproduct(*vectors):
    '''Returns a map that produces the products of the
    corresponding elements of the vector arguments. Dimensions
    beyond the lowest dimension represented by any of the
    vectors are ignored. Example:
            >>> tuple(arrayproduct(range1(3), indefinite(1)))
            (1, 4, 9) 
    '''
    return map(unstar(product), zip(*vectors))

