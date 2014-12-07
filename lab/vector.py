# file: vector.py
from operator import mul

def dot(x, y):
    '''calculate a dot product for vectors

    options:
        -x SCALARS...  x vector
        -y SCALARS...  y vector
    '''
    return sum(map(mul, x, y))

if __name__ == '__main__':
    from clime import now
