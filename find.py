import itertools

target = float(input("Meal price: $"))
maxitems = int(input("Max items: "))
tolerance = int(input("Tolerance: $0.0"))
filename = input("Prices file: ./")

pricestext = open(filename).read()
priceslist = pricestext.split("\n")
pricesarray = []
for item in priceslist:
    if("#" not in item.split(": ")[0]):
        pricesarray += [item.split(": ")]
pricesarray.pop(-1)

print("Prices imported")

for targetoffset in range(tolerance + 1):
    print("\n\nTarget: $" + str(target) + "__________________")
    exactmeals = []
    for j in range(maxitems):
        i = j + 1
        print("\nGenerating meals with " + str(i) + " items...")
        meals = list(itertools.combinations(pricesarray, i))
        for meal in meals:
            price = 0.0
            mealincludes = []
            valid = True
            for item in meal:
                if(">" in item[1]):
                    includes = item[1].split(">")[1].split(" ")[0]
                    if(includes in mealincludes):
                        valid = False
                    else:
                        mealincludes += [includes]
                if("<" in item[1]):
                    if(item[1].split("<")[1].split(" ")[0] not in mealincludes):
                        valid = False
                price += float(item[0])
            if(price == target and valid):
                exactmeals += [meal]
                print("\n$" + str(target) + " meal found:")
                for item in meal:
                    print(" -- $" + item[0] + ": " + item[1])

    target -= 0.01

#    exactmeals += list(itertools.combinations(pricesarray, i))
