#!/usr/bin/env python3

import itertools

# Get variables to work with
target = float(input('Meal price: $'))
origtarget = target
maxitems = int(input('Max items: '))
tolerance = int(input('Tolerance: $0.0'))
filename = input('Prices file: ./')
blacklist = input('Avoid (keywords separated by ,): ').split(',')
whitelist = input('Mandatory items (exact match): ').split(',')

mandatory = []

# Read the prices from a text file
pricestext = open(filename).read()
priceslist = pricestext.split('\n')
pricesarray = []
for item in priceslist:
    # If it isn't commented out and exists, get it
    if '#' not in item.split(': ')[0] and item != '':
        itemarray = item.split(': ')
        # Ignore the item if it has a blacklisted keyword
        for black in blacklist:
            if black in itemarray[1] and black != '':
                itemarray[0] = ''
        for white in whitelist:
            # If an item name exactly matches the whitelist,
            if itemarray[1] == white:
                # add it to mandatory and account for it
                mandatory += [itemarray]
                target -= float(itemarray[0])
                maxitems -= 1
        if itemarray[0] != '':
            pricesarray += [itemarray]

print('Prices imported')
j = 0
for i in range(len(pricesarray)):
    if float(pricesarray[j][0]) > target:
        del(pricesarray[j])
        j -= 1

# Array of all exact meals
exactmeals = []

# Run the program once for every available price, based on the tolerance
for targetoffset in range(tolerance + 1):
    # Print current target price
    print('\n\n    Target: $' + str(origtarget) +
          '\n_____________________________')
    # Find all meals with up to the given number of items
    for j in range(maxitems):
        # Start counting at 1
        i = j + 1
        print('\nGenerating meals with ' + str(i + len(mandatory)) + ' items...')
        # Generate a list of all possible combinations with the menu
        meals = list(itertools.combinations(pricesarray, i))

        # Go through every meal
        for meal in meals:
            # Start with a price pf 0
            price = 0.0
            # Start with no base includes (one allowed in a category, allows condiments)
            mealincludes = []
            # Valid unless proven otherwise
            valid = True

            # For every item in the meal:
            for item in meal:
                # If it doesn't depend on an include:
                if('<' not in item[1]):
                    # If it's an include:
                    if('>' in item[1]):
                        # Find the include
                        includes = item[1].split('>')[1].split(' ')[0]
                        # If there's already one there, meal is invalid
                        if(includes in mealincludes):
                            valid = False
                        else:
                            # Add the include to the includes
                            mealincludes += [includes]
                    # Add the price to the total
                    price += float(item[0])
            for item in meal:
                # If it depends on an include:
                if('<' in item[1]):
                    # If the include isn't in the meal, it's invalid
                    if(item[1].split('<')[1].split(' ')[0] not in mealincludes):
                        valid = False
                    # Add the price to the total
                    price += float(item[0])

            # If the meal matches the target and it's valid, print it
            if(price == target and valid):
                exactmeals += [meal]
                print('\n$' + str(origtarget) + ' meal found:')
                # Print mandatory items first
                for item in mandatory:
                    print(' -- $' + item[0] + ': ' + item[1])
                for item in meal:
                    print(' -- $' + item[0] + ': ' + item[1])

    # Decrease target for next round
    target -= 0.01
    origtarget -= 0.01
