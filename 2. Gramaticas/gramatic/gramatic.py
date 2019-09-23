import re
from pprint import pprint

'''
Steps to solve the problem:
    1. N nulls set.
    2. Null productions set.
    3. Non-terminal firsts set.
    4. Non-terminal firsts production set.
    5. Follow set.
    6. Selection set.

Types:
    1. Special.
    2. Right linear.
    3. S.
    4. Q.
    5. LL(1).
'''

class Gramatic():
    
    def __init__(self, gramaticSet):
        self.gramaticSet = gramaticSet

        self.nullSet()

    def nullSet(self):
        #pprint(self.gramaticSet)

        self._nullSet = []        
        for (index, row) in enumerate(self.gramaticSet):
            if re.findall(r'/', row):
                prod = row[0: str(row).find('->')]

                self._nullSet.append({'pos': index, 'prod': prod})

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