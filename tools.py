import random

def generateId(mapper):
    # Generate a random, unique id
    newId = random.randint(0, 65535)

    # Check if it is unique, if not, generate a new one and repeat until unique is found
    idIsUnique = True
    for obj in list(mapper.nodes.values()) + list(mapper.edges.values()):
        if obj.id == newId:
            idIsUnique = False
    while idIsUnique is False:
        newId = random.randint(0, 65535)
        for obj in mapper.nodes.values() + mapper.edges.values():
            if obj.id == newId:
                idIsUnique = False
    return newId