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

def calcRegionSides(mapper, localPos):
    sides = [False, False, False, False]  # Left Right Up Down
    for region in mapper.regions.values():
        if region.pos().x() < localPos.x() < region.pos().x() + (region.size.x() * mapper.zoomLevel) and region.pos().y() < localPos.y() < region.pos().y() + (region.size.y() * mapper.zoomLevel):
            print("test")
            if region.pos().x() - 10 < localPos.x() < region.pos().x() + 10:
                sides[0] = True
            if region.pos().x() + (region.size.x() * mapper.zoomLevel) - 10 < localPos.x() < region.pos().x() + (region.size.x() * mapper.zoomLevel) + 10:
                sides[1] = True
            if region.pos().y() - 10 < localPos.y() < region.pos().y() + 10:
                sides[2] = True
            if region.pos().y() + (region.size.y() * mapper.zoomLevel) - 10 < localPos.y() < region.pos().y() + (region.size.y() * mapper.zoomLevel) + 10:
                sides[3] = True
    return sides