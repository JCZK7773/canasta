class Locations():
    def __init__(self):
        pass

    def funct_1(self):
        print("1")


Locate = Locations()


func_dict = {'MasterDeck': Locate.funct_1}


class OverrideAppendList(list):
    def __init__(self, name):
        self.name = name

    def append(self, item):
        if self.name in func_dict:
            func_dict[self.name]()
            func_dict[self.name]()
        super().append(item)


class Deck():
    def __init__(self):
        self.MasterDeck = OverrideAppendList('MasterDeck')


Deck_1 = Deck()


Deck_1.MasterDeck.append(4)
Deck_1.MasterDeck.pop(-1)
Deck_1.MasterDeck.append(4)
