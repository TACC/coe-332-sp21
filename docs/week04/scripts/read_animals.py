#!/usr/bin/env python3
import json
import random
import sys

def main():

    with open(sys.argv[1], 'r') as f:
        animal_dict = json.load(f)

    print(random.choice(animal_dict['animals']))

if __name__ == '__main__':
    main()
