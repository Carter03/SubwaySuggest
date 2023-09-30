deals = [
        [r'10% Off 1 Sub', r'Free Cookie with 1 Sub', r'Free Drink with 1 Sub', r'Free Chips with 1 Sub'],
        [r'BOGO Subs When You Buy Meals', r'Free Meal Extra When You Buy One', r'Free 2 Cookies With 2 Subs'],
        [r'Free Sub When You Buy 2', r'Free Chips & Drink With 3 Subs', r'Free 3 Cookies With 3 Subs'],
        [r'Free Meal When You Buy 3', r'Free Drinks With 4 Subs', r'Free Chips With 4 Subs', r'Free Cookies With 4 Subs']
        ]

def GetDeals(numPeople):
    return deals[numPeople - 1]