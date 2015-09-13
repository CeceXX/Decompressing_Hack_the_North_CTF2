# Minimal code to decompress.

import argparse

def s_decompress(x):
    print("I'm in decompress!")

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

