#!/usr/bin/env python3

"""Fast Compress. The Fastest Way To Compress.

Copyright (C) 2015 Wesley Scott

PURPOSE
-------

Existing compression algorithms achieve good compression ratio at the expense
of time. Fast Compress achieves good compression ratio while ensuring that
compression takes a reasonable amount of time.

Additionally, Fast Compress includes several security features designed to make
alternatives decompression algorithms more difficult to implement. This prevents
others from creating clones of Fast Compress, which serves to fragment the
community and therefore reduce interoperability and security.

USAGE
-----

This application works with Python3.

Through the command line, simply:

 $ fc --decompress
 Decompressing file.fc......... Done
 See output: file

 $ fc --compress
 Compressing file... Done
 See output: file.fc

LIMITATIONS
-----------

.fc files, at the moment, are text files. Additionally, Fast Compress itself
only works on text files. Fast Compress only works with ASCII characters.

"""

import binascii
import random
import re
import numpy

def matmul(a, b):
    print("I'm in matmul!")
    return [
        [sum(x * y for x, y in zip(r, c))
         for c in zip(*b)]
        for r in a
        ]

def matdiv(c, b):
    return numpy.divide(c, b)

def s_compress(plaintext):
    print("I'm in compress!")
    """Compress the given string, returning a string."""

    # Three parts of output are: HEAD, BODY, FOOT
    head = []
    body = []
    foot = []

    # The first part of the HEAD is the compression version, as a simple ascii
    # string.
    head.append('001')

    # For security purposes, next we will have an encryption key.
    # The STRONGENCRYPT algorithm developed by yours truly is used for maximum
    # security. The encryption key is ended by a slash (/).
    encryption_key = random.choice((
        '!wes!', '!wesley!', '!scott!', '!wscott!', '!northbank!'
        ))
    head.append(encryption_key + '/')

    encrypted_plaintext = s_encrypt(plaintext, encryption_key)
    print(encrypted_plaintext)

    # For security purposes, next we will have a matrix encryption key.
    # Important letters are compressed by multiplication with this matrix
    # encryptor.
    m_encryptor = [
        [random.randint(1, 3) for _ in range(3)]
        for _ in range(3)
        ]
    head.append(repr(m_encryptor) + '/')

    # Here is the core of the compression.
    # Extract random parts of the body and move them to the head,
    # in the form of a dictionary.
    # The sequence @005 will be used to identify the 5th element of the head's
    # dictionary, when it is put in lexicographic order.
    # Some characters are escaped:
    #          @ - @000
    #  (newline) - @999
    #          / - @998
    tokens = []
    for c in encrypted_plaintext:
        if c == '@':
            tokens.append('@000')
        elif c == '\n':
            tokens.append('@999')
        elif c == '/':
            tokens.append('@998')
        else:
            tokens.append(c)

    chunks = 0
    i = 0
    l_chunks = []
    while i < len(tokens):
        if chunks >= 997:
            break

        if i < len(tokens) - 5 and random.random() > 0.8:  # chunk time
            chunk = tokens[i:i+5]
            chunks += 1
            l_chunks.append(chunk)
            head.append("".join(chunk) + '/')
            body.append('@' + '0' * (3 - len(str(chunks))) + str(chunks))
            # For better compression store a securehash of the chunk in the
            # footer.
            foot.append(s_securehash("".join(chunk * 3)))
            i += 4
        elif random.random() > 0.8:  # Matrix multiplication compression
            lst1 = [[0, 0, 0], [1, 2, 3], [3, 2, 1]]
            if tokens[i][0] == '@':
                lst1[0] = []
                for c in tokens[i][1:]:
                    lst1[0].append(int(c) + 10)
            else:
                lst1[0][0] = ord(tokens[i])
            print(m_encryptor, lst1)
            body.append('/' + repr(matmul(lst1, m_encryptor)) + '/')
        else:
            body.append(tokens[i])

        i += 1

    # Next it is time to reorder the body's chunks so that they are in sorted
    # order.
    indices = sorted(enumerate(l_chunks), key=lambda x: (x[1], x[0]))
    for i, part in enumerate(body):
        if part[0] == '@':
            rest = int(part[1:])
            for cv in range(len(indices)):
                if indices[cv][0] == rest - 1:
                    body[i] = '@' + '0' * (3 - len(str(cv+1))) + str(cv+1)

    return "\n".join(("".join(head), "".join(body), "".join(foot)))


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

    def replace(num):
        num = num.group(1)
        print(num)
        if num in {'000', '998', '999'}:
            return '@' + num

        elif len(num) < (len(chunks)):
        	return chunks[int(num)-1]

        else:
        	print (int(num))
            #return chunks[int(num)-1]

    def replace_special(num):
        num = num.group(1)
        if num == '000':
            return '@'
        elif num == '998':
            return '/'
        else:
            return '\n'

    body = re.sub('/(.+?)/', matrix_fix, body)
    body = re.sub('@([0-9]{3})', replace, body)
    body = re.sub('@([0-9]{3})', replace_special, body)

    return s_decrypt(body, key)


class NotSortedException(Exception):
    pass


def r_sort(lst):
    print("I'm in sort!")
    """Return a clone of the list in sorted order."""
    clone = lst[:]
    return sorted(clone)


def s_encrypt(plaintext, key):
    print("I'm in encrypt!")
    """Use the STRONGENCRYPT algorithm to encrypt the plaintext."""
    encrypted_plaintext = []
    for i, c in enumerate(plaintext):
        e = key[i % len(key)]
        if ord(c) < ord(e) - 32:
            encrypted_plaintext.append('A')  # type A encryption
            encrypted_plaintext.append(chr(ord(e) - ord(c)))
        elif ord(e) < ord(c) - 32:
            encrypted_plaintext.append('B')  # type B encryption
            encrypted_plaintext.append(chr(ord(c) - ord(e)))
        else:
            encrypted_plaintext.append('C')  # type C encryption
            encrypted_plaintext.append(c)

    return "".join(encrypted_plaintext)


def s_decrypt(encrypted, key):
    print("I'm in decrypt!")
    """Decrypt a STRONGENCRYPTed string."""
    plaintext = []

    while encrypted != s_encrypt("".join(plaintext), key):
        plaintext = []

        for i, c in enumerate(encrypted):
            if i % 2 == 0:
                continue  # even numbers are just ABC, irrelevant to encryption
            k = key[i // 2 % len(key)]
            possibilities = []
            try:
                possibilities.append(chr(ord(k) - ord(c)))
            except:
                pass
            try:
                possibilities.append(chr(ord(k) + ord(c)))
            except:
                pass
            try:
                possibilities.append(c)
            except:
                pass
            plaintext.append(random.choice(possibilities))

    return "".join(plaintext)


def s_securehash(plaintext):
    print("I'm in securehash!")
    """Return a hex digest of a hash of the given string."""
    hsh = bytearray(16)
    plaintext = plaintext.encode('ascii')
    hsh[15] = len(plaintext)
    for i, byte in enumerate(plaintext):
        hsh[i%15] ^= table[i%8][byte]
    return binascii.hexlify(hsh).decode('ascii')


### GENERATE THE SECUREHASH TABLE ###

table = [{} for _ in range(8)]

for byte in range(32, 128):
    for i in range(8):
        b = byte ^ 0x55
        result = (b + (b << i) + (b >> i)) % 256
        table[i][byte] = result


if __name__ == "__main__":
    print("I'm in main!")
    import argparse

    parser = argparse.ArgumentParser(description='Compress quickly.')
    parser.add_argument('--compress', dest='compress', action='store_const',
                       const=True, default=False)
    parser.add_argument('--decompress', dest='compress', action='store_const',
                       const=False, default=True)
    args = parser.parse_args()
    if args.compress:
        with open('file') as f:
            with open('file.fc', 'w') as k:
                k.write(s_compress(f.read()))
    else:
        with open('file.fc') as f:
            with open('file', 'w') as k:
                k.write(s_decompress(f.read()))
