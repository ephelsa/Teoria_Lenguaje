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
    
    endOfString = '┤'

    def __init__(self, gramaticSet):
        # Pattern to get only non-terminals or the left side.
        self.nonTerminalPattern = re.compile(r'^(<[a-z0-9]+>)+$', re.I)

        # Gramatic set to work on it.
        self.gramaticSet = gramaticSet

        #print('Conjunto de selección: ')
        #pprint(self.selectedSet())
        #print('Nulls ->', self.nullSet())
        #print('First ->', self.firstSet())
        #print('First prod ->', self.firstProd())
        #print('Next ->', self.nextSet())

        self.showSelectedSet()

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


                    nonTerminalGroup = (re.sub('>', '> ', rightSide)).split(' ')[:-1]
                    nullNonTerminal = True
                    
                    for data in nonTerminalGroup:
                        if data not in nullProductions:     # If isn't null                            
                            nullNonTerminal = False             # changes the value to not be stored.
                            break
                    
                    #exit(0)
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

        nullNonTerminals = list(map(lambda x: x['prod'], self.nullSet()))
        
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
                        noNull = False
                        nonTerminalGroup = (re.sub('>', '> ', matched)).split(' ')[:-1]

                        for nonTerminal in nonTerminalGroup:
                            if nonTerminal in nullNonTerminals and not noNull:
                                setOfFirsts[leftSide].extend(setOfFirsts[nonTerminal])
                            else:
                                noNull = True
                        '''
                        for (key, _) in setOfFirsts.items():
                            if key in matched and key in nullNonTerminals and not noNull:                                
                                print('EXTENDED ->', key, matched, setOfFirsts[key])

                                setOfFirsts[leftSide].extend(setOfFirsts[key])
                            else:
                                noNull = True
                        '''
        ## No 
        for (key, _) in setOfFirsts.items():
            setOfFirsts[key] = list(set(setOfFirsts[key]))


        #print('After', setOfFirsts)

        return setOfFirsts

    def firstProd(self):
        setOfFirsts = self.firstSet()
        setOfFirstsProductions = []
        nullNonTerminals = list(map(lambda x: x['prod'], self.nullSet()))

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

                isNull = False 
                nonTerminalGroup = (re.sub('>', '> ', nonTerminal.group())).split(' ')[:-1]
                
                for element in nonTerminalGroup:
                    if element in nullNonTerminals and not isNull:
                        itemsPerProduction.extend(setOfFirsts[element])
                    else:
                        isNull = True
                
                #for (key, nonTerminalFirst) in setOfFirsts.items():
                #    if key in nonTerminal.group():
                #        itemsPerProduction.extend(nonTerminalFirst)
                        


            setOfFirstsProductions.append(itemsPerProduction)

            
        return setOfFirstsProductions

    def nextSet(self):
        # Get null productions.
        nullNonTerminals = list(map(lambda x: x['prod'], self.nullSet()))
        firstsGroup = self.firstSet()

        # No search again the same nexts per non terminal.
        foundNonTerm = []

        nextFounds = []

        toSeekAfter = []

        def insertNextFound(nonTerminal, nextFound):
            if nonTerminal in nextFound:
                index = nextFounds.index(nextFound)
                dataToInsert = nextFound[nonTerminal]

                nextFounds[index][nonTerminal].extend(dataToInsert)
            else:
                for (indexFound, dataFound) in enumerate(nextFounds):
                    if nonTerminal in dataFound:
                        nextFounds[indexFound][nonTerminal].append(nextFound)  

        def findInNextFounds(nonTerminal):
            for (index, data) in enumerate(nextFounds):
                if nonTerminal in data:

                    return index

            return -1


        # Get the left side per prod.
        for (indexProd, prod) in enumerate(self.gramaticSet):
            leftSide = prod[0: str(prod).find('->')]  # Get the left side.

            # Search apparitions.
            foundArr = []            
            if leftSide not in foundNonTerm:
                if indexProd == 0:
                    nextFounds.append({leftSide: [self.endOfString]})

                for (indexSeek, seekProd) in enumerate(self.gramaticSet):
                    seekLeftSide = seekProd[0: str(seekProd).find('->')]  # Get the left side.
                    rightSide = seekProd[str(seekProd).find('->') + 2:]   # Get the rigth side of the prod.

                    if leftSide in rightSide:
                        foundArr.append({'non_terminal': seekLeftSide, 'right_side': rightSide})
                        foundNonTerm.append(leftSide)


                nextsArr = list(
                                map(
                                    lambda x: {
                                        'non_terminal': x['non_terminal'],
                                        'next':x['right_side'][(str(x['right_side']).find(leftSide) + len(leftSide)):]
                                        }, 
                                    foundArr
                                )
                            )

                for nextData in nextsArr:
                    next2NonTerminal = re.match(re.compile(r'^(<[a-z0-9]+>)+', re.I), nextData['next'])
                    next2Terminal = re.match(re.compile(r'^([a-z0-9]+)', re.I), nextData['next'])


                    #print(leftSide, '->', nextData)

                    if nextData['next'] == '':                        
                        if leftSide == nextData['next']:
                            if findInNextFounds(leftSide) is not -1:
                                insertNextFound(nextData['non_terminal'], nextFounds[findInNextFounds(leftSide)])
                        else:
                            if leftSide != nextData['non_terminal']:
                                toSeekAfter.append({'to_seek': leftSide, 'nexts_of': nextData['non_terminal']})



                    elif next2NonTerminal:
                        nonTerminal = next2NonTerminal.group()
                        if nonTerminal in nullNonTerminals:
                            toSeekAfter.append({'to_seek': leftSide, 'nexts_of': nonTerminal})
                        else:
                            if findInNextFounds(leftSide) is not -1:
                                insertNextFound(nextData['non_terminal'], nextFounds[findInNextFounds(leftSide)])
                            else:
                                nextArr = (re.sub('>', '> ', nextData['next'])).split(' ')[:-1]

                                for data in nextArr:
                                    nextFounds.append({leftSide: firstsGroup[data]})

                        
                    elif next2Terminal:
                        if findInNextFounds(leftSide) is not -1:
                            insertNextFound(leftSide, next2Terminal.group())
                        else:
                            nextFounds.append({leftSide: [next2Terminal.group()]})


        newNextFounds = {}
        for data in nextFounds:
            newNextFounds.update(data)
        nextFounds = newNextFounds

        #print('toSeekAfter', toSeekAfter, 'nextFounds', nextFounds)

        for seek in toSeekAfter:
            if seek['to_seek'] in nextFounds and seek['nexts_of'] in nextFounds:
                nextFounds[seek['to_seek']].extend(nextFounds[seek['nexts_of']])
            elif seek['to_seek'] not in nextFounds:
                nextFounds.update({ seek['to_seek']: nextFounds[seek['nexts_of']]})

        for seek in toSeekAfter:            
            nextFounds[seek['to_seek']].extend(nextFounds[seek['nexts_of']])

            nextFounds[seek['to_seek']] = list(set(nextFounds[seek['to_seek']]))

        #print('nextFounds', nextFounds)
        #exit(0)

        return nextFounds

    def selectedSet(self):
        setOfNullsPack = self.nullSet()
        setOfFirstsProd = self.firstProd()
        setOfNexts = self.nextSet() 

        setOfSelecteds = {}

        for (indexProd, prod) in enumerate(self.gramaticSet):
            leftSide = prod[0: str(prod).find('->')]  # Get the left side.
            rightSide = prod[str(prod).find('->') + 2:]   # Get the rigth side of the prod.

            startsNonTerminal = re.match(re.compile(r'^(<[a-z0-9]+>)+', re.I), rightSide)
            startsTerminal = re.match(re.compile(r'^([a-z0-9]+)', re.I), rightSide)
            if startsNonTerminal:
                isNull = False
                for nullData in setOfNullsPack:
                    if nullData['pos'] == indexProd:
                        setOfSelecteds.update({indexProd: setOfFirstsProd[indexProd] + setOfNexts[leftSide]})
                        setOfSelecteds[indexProd] = list(set(setOfSelecteds[indexProd]))
                        isNull = True

                if not isNull:
                    setOfSelecteds.update({indexProd: setOfFirstsProd[indexProd]})

            elif startsTerminal:
                setOfSelecteds.update({indexProd: setOfFirstsProd[indexProd]})

            else:
                setOfSelecteds.update({indexProd: setOfNexts[leftSide]})

        # Order
        for selected in setOfSelecteds:
            setOfSelecteds[selected] = list(set(setOfSelecteds[selected]))
            setOfSelecteds[selected] = sorted(setOfSelecteds[selected])

        return setOfSelecteds

    def gramaticType(self):
        return "Not created yet"
    
    def showSelectedSet(self):
        setOfSelecteds = self.selectedSet()

        for prodIndex in setOfSelecteds:
            print(str(prodIndex + 1), '->', setOfSelecteds[prodIndex])