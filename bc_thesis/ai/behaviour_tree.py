
class BehaviorTreeNode:
    """Zakladni (abstrakntni) trida, kterou dědí všechny uzly stromu."""
    def execute(self):
        raise NotImplementedError("Execute method must be implemented by subclasses.")



#OR - vybere prvni uspesnou akci
class Selector(BehaviorTreeNode):
    """
    Prochází své poduzly (children) jeden po druhém a hledá takový, který uspěje.
    Jakmile jeden uspěje, Selector skončí a vrátí True.
"""
    def __init__(self, children):
        self.children = children

    def execute(self):
        #pokud alespoň jeden poduzel vrati True, selektro skonci a vrati true
        for child in self.children:
            if child.execute():
                return True
        return False #pokud zadny neuspeje, vrati false

#AND - pokud nektery krok selze, cela akce selze
class Sequence(BehaviorTreeNode):
    """Provadí všechny své poduzly (children), dokud jeden z nich neuspěje"""
    def __init__(self, children):
        self.children = children

    def execute(self):
        for child in self.children:
            if not child.execute():
                return False
        return True


class Condition(BehaviorTreeNode):
    """
    Zkontroluje konkrétní podmínku.
    Podmínka je reprezentována funkcí, která vrací True nebo False.
    """
    def __init__(self, func):
        self.func = func #pri inicializaci se ji předá funkce

    def execute(self):
        return self.func() #vrati true nebo false


class Action(BehaviorTreeNode):
    """Provede konkrétní akci."""
    def __init__(self, func):
        self.func = func

    def execute(self):
        self.func()
        return True


