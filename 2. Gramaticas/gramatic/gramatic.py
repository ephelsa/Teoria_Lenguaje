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
        print('N and null productions:', self.nullSet())
        print('Firts set', self.firstSet())
        print('Firsts set per Production', self.firstProd())

    def nullSet(self):
        # Patter to catch null productions.
        nullPattern = re.compile(r'/')

        # Null group.
        setOfNulls = []

        # First, get the 'easy' null productions.
        for (index, row) in enumerate(self.gramaticSet):
            if re.findall(nullPattern, row):    # Find the null production.
                leftSide = row[0: str(row).find('->')]  # Get the left side.

                # Store the null production and null non-terminal.
                # Solved: 1 and 2.
                setOfNulls.append({'pos': index, 'prod': leftSide})

        #print('Explicit ->', end='')
        #pprint(setOfNulls)

        # Second, get implicit null productions.
        # Get the N nulls set.
        nullProductions = list(map(lambda x: x['prod'], setOfNulls))
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
                        setOfNulls.append({'pos': index, 'prod': leftSide})

        #print('Complete ->', end='')
        #pprint(setOfNulls)      

        return setOfNulls              

    def nonTerminal(self):
        nonTerminalSet = []

        for prod in self.gramaticSet:
            leftSide = prod[0: str(prod).find('->')]  # Get the left side.

            nonTerminalSet.append(leftSide)

        return list(set(nonTerminalSet)) 

    def firstSet(self):
        # Nonterminals
        nonTerminalSet = self.nonTerminal()

        # Regex to get easily.
        firstExplicitPattern = re.compile(r'^[a-z0-9]+', re.I)
        firstImplicitPatter = re.compile(r'^(<[a-z0-9]>)+[a-z0-9]*', re.I)

        # Firsts group.
        setOfFirsts = {}

        # First, explicit terminals.
        for nonTerminal in nonTerminalSet:
            for prod in self.gramaticSet:
                leftSide = prod[0: str(prod).find('->')]
                rightSide = prod[str(prod).find('->') + 2:]   # Get the rigth side of the prod.
                rightSide = re.match(firstExplicitPattern, rightSide)


                if leftSide == nonTerminal and rightSide:
                    setOfFirsts[leftSide] = [rightSide.group()]

        #print('Before', setOfFirsts)
        
        for nonTerminal in nonTerminalSet:
            for prod in self.gramaticSet:
                leftSide = prod[0: str(prod).find('->')]
                rightSide = prod[str(prod).find('->') + 2:]   # Get the rigth side of the prod.
                rightSide = re.match(firstImplicitPatter, rightSide)


                if leftSide == nonTerminal and rightSide:
                    rightSide = rightSide.group() 
         

                    matched = re.match(r'^(<[a-zA-Z0-9]>)+', rightSide).group()
                    lastTerminal = re.match(r'^(<[a-zA-Z0-9]>)*([a-zA-Z0-9]+)+', rightSide)


                    if matched in setOfFirsts:
                        setOfFirsts[leftSide].extend(setOfFirsts[matched])

                        if lastTerminal:
                            setOfFirsts[leftSide].append(lastTerminal.groups()[1])
                    else:
                        for (key, _) in setOfFirsts.items():
                            if key in matched:
                                setOfFirsts[leftSide].extend(setOfFirsts[key])
        
        for (key, _) in setOfFirsts.items():
            setOfFirsts[key] = list(set(setOfFirsts[key]))


        #print('After', setOfFirsts)

        return setOfFirsts

    def firstProd(self):
        setOfFirsts = self.firstSet()
        setOfFirstsProductions = []

        for prod in self.gramaticSet:
            # Regex
            rightSide = prod[str(prod).find('->') + 2:]   # Get the rigth side of the prod.
            lastTerminal = re.match(r'^(<[a-zA-Z0-9]>)*([a-zA-Z0-9]+)+', rightSide)
            nonTerminal = re.match(r'^(<[a-zA-Z0-9]>)+', rightSide)

            # To insert
            itemsPerProduction = []
            
            if lastTerminal is not None:
                matched = re.match(r'^(<[a-zA-Z0-9]>)+', lastTerminal.group())
                terminal = re.match(r'^([a-zA-Z0-9])+', lastTerminal.group())

                if matched:
                    item = lastTerminal.group().replace(matched.group(), '')
                    itemsPerProduction.append(item)

                    for (key, nonTerminalFirst) in setOfFirsts.items():
                        if key in matched.group():
                            itemsPerProduction.extend(nonTerminalFirst)
                elif terminal:
                    itemsPerProduction.append(terminal.group())

            elif nonTerminal:
                for (key, nonTerminalFirst) in setOfFirsts.items():
                    if key in nonTerminal.group():
                        itemsPerProduction.extend(nonTerminalFirst)
                        


            setOfFirstsProductions.append(itemsPerProduction)

            
        return setOfFirstsProductions

    def nextSet(self):
        pass

    def selectedSet(self):
        pass

    def gramaticType(self):
        pass