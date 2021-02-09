#!/usr/bin/env python3
import json
import petname
import random
import sys

def main():

    animal_dict = {}
    animal_dict['animals'] = []

    for i in range(20):
        this_animal = {}
        this_animal['head'] = random.choice(['snake', 'bull', 'lion', 'raven', 'bunny'])
        this_animal['body'] = petname.name() + '-' + petname.name()
        this_animal['arms'] = random.randint(1,5) * 2
        this_animal['legs'] = random.randint(1,4) * 3
        this_animal['tail'] = this_animal['legs'] + this_animal['arms']

        animal_dict['animals'].append(this_animal)

    with open(sys.argv[1], 'w') as f:
        json.dump(animal_dict, f, indent=2)

if __name__ == '__main__':
    main()
