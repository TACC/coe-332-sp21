import json

def check_char_count(mystr):
    if ( len(mystr) == 2 ):
        return( f'{mystr} count passes' )
    else:
        return( f'{mystr} count FAILS' )

def check_char_type(mystr):
    if ( mystr.isupper() and mystr.isalpha() ):
        return( f'{mystr} type passes' )
    else:
        return( f'{mystr} type FAILS' )

def check_char_match(str1, str2):
    if ( str1[0] == str2[0] ):
        return( f'{str1} match passes' )
    else:
        return( f'{str1} match FAILS' )


with open('states.json', 'r') as f:
    states = json.load(f)


for i in range(50):
    print(check_char_count( states['states'][i]['abbreviation'] ))
    print(check_char_type( states['states'][i]['abbreviation'] ))
    print(check_char_match( states['states'][i]['abbreviation'], states['states'][i]['name'] ))
