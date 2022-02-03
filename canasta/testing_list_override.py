def funct_1():
    print("1")

func_dict = {'MasterDeck': funct_1()}


class OverrideAppendList(list):
    def __init__(self, name):
        self.name = name

    def append(self, item):
        if self.name in func_dict:
            func_dict[self.name]
        super(OverrideAppendList, self).append(item)


class Deck():
    def __init__(self):
        self.MasterDeck = OverrideAppendList('MasterDeck')

Deck_1 = Deck()

print(Deck_1.MasterDeck)
print(type(Deck_1.MasterDeck))
Deck_1.MasterDeck.append(4)
Deck_1.MasterDeck.append(5)
print(Deck_1.MasterDeck)
# print(Deck_1.MasterDeck)
