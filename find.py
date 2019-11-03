import itertools

# Get variables to work with
target = float(input('Meal price: $'))
maxitems = int(input('Max items: '))
tolerance = int(input('Tolerance: $0.0'))
filename = input('Prices file: ./')

# Read the prices from a text file
pricestext = open(filename).read()
priceslist = pricestext.split('\n')
pricesarray = []
for item in priceslist:
    if('#' not in item.split(': ')[0] and item != ''):
        pricesarray += [item.split(': ')]

print('Prices imported')

# Array of all exact meals
exactmeals = []

# Run the program once for every available price, based on the tolerance
for targetoffset in range(tolerance + 1):
    # Print current target price
    print('\n\n    Target: $' + str(target) + '\n_____________________________')
    # Find all meals with up to the given number of items
    for j in range(maxitems):
        # Start counting at 1
        i = j + 1
        print('\nGenerating meals with ' + str(i) + ' items...')
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
                print('\n$' + str(target) + ' meal found:')
                for item in meal:
                    print(' -- $' + item[0] + ': ' + item[1])

    target -= 0.01
