import re
from pprint import pprint

'''
Steps to solve the problem:
    1. N nulls set.
    2. Null productions set.
    3. Firsts set.
    4. Firsts production set.
    5. Follow set.
    6. Selection set.

Types:
    I. Special.
    II. Right linear.
    III. S.
    IV. Q.
    V. LL(1).
'''

class Gramatic():
    
    def __init__(self, gramaticSet):
        # Pattern to get only non-terminals or the left side.
        self.nonTerminalPattern = re.compile(r'^(<[a-z0-9]+>)+$', re.I)

        # Gramatic set to work on it.
        self.gramaticSet = gramaticSet

        # Testing the null set.
        self.nullSet()

    def nullSet(self):
        # Patter to catch null productions.
        nullPattern = re.compile(r'/')

        # Null group.
        self._nullSet = []

        # First, get the 'easy' null productions.
        for (index, row) in enumerate(self.gramaticSet):
            if re.findall(nullPattern, row):    # Find the null production.
                leftSide = row[0: str(row).find('->')]  # Get the left side.

                # Store the null production and null non-terminal.
                # Solved: 1 and 2.
                self._nullSet.append({'pos': index, 'prod': leftSide})

        print('Explicit ->', end='')
        pprint(self._nullSet)

        # Second, get implicit null productions.
        # Get the N nulls set.
        nullProductions = list(map(lambda x: x['prod'], self._nullSet))
        for (index, row) in enumerate(self.gramaticSet):
            if not re.findall(nullPattern, row):    # Get non null.
                leftSide = row[0: str(row).find('->')]  # Used to be stored in the set.
                rightSide = row[str(row).find('->') + 2:]   # Get the rigth side of the prod.
                rightSide = re.match(self.nonTerminalPattern, rightSide)    # Only non-terminal.

                if rightSide: # Found non-terminals.
                    rightSide = rightSide.group()  

                    nullNonTerminal = True
                    for nullProduction in nullProductions:
                        if nullProduction not in rightSide:     # If isn't null
                            nullNonTerminal = False             # changes the value to not be stored.
                            break
                    
                    # Store if we found a null production.
                    if nullNonTerminal:
                        self._nullSet.append({'pos': index, 'prod': leftSide})

        print('Complete ->', end='')
        pprint(self._nullSet)                    

    def firstSet(self):
        pass

    def firstProd(self):
        pass

    def nextSet(self):
        pass

    def selectedSet(self):
        pass

    def gramaticType(self):
        pass