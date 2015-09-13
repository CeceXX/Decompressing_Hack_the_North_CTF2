# Minimal code to decompress.
# 1st -> main
# 2nd -> s_decompress
# 3rd -> sort

import argparse
import numpy

def r_sort(lst):
    print("I'm in sort!")
    """Return a clone of the list in sorted order."""
    clone = lst[:]
    return sorted(clone)

def matdiv(c, b):
    return numpy.divide(c, b)

def s_decompress(x):
    print("I'm in decompress!")
    version, x = int(x[:3]), x[3:]
    head, body, foot, ignore = x.split('\n')
    key, mkey, *head = head.split('/')
    mkey = eval(mkey)
    chunks = r_sort(head[:-1])
    print(len(chunks))
    def matrix_fix(lst):
        lst = eval(lst.group(1))
        soln = matdiv(lst, mkey)
        if soln[0][1] == 0:
            return chr(int(soln[0][0]))
        else:
            return '@' + ''.join(str(int(i)-10) for i in soln[0])

if __name__ == "__main__": 
    print("I'm in main!")
    parser = argparse.ArgumentParser(description='Decompressing has never been easier!')
    parser.add_argument('--decompress', dest='compress', action='store_const',
                       const=False, default=True)
    args = parser.parse_args()
    if args.compress:
        with open('file.fc') as f:
            with open('file', 'w') as k:
                k.write(s_decompress(f.read()))

