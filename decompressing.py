# Minimal code to decompress. No fluff. 

import argparse

if __name__ == "__main__": 
    print("I'm in main!")
    parser = argparse.ArgumentParser(description='Decompressing has never been easier!')
    parser.add_argument('--decompress', dest='compress', action='store_const',
                       const=False, default=True)
    args = parser.parse_args()

