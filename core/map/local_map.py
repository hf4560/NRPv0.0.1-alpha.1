class LocalMap:
    def __init__(self):
        self.__nearNodes = {}

    def getNearNodes(self):
        return self.__nearNodes

    def addNearNode(self, hash_, node):
        self.__nearNodes[hash_] = node
