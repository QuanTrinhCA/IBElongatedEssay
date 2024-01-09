# python 3.11

from copy import copy, deepcopy
from time import time

def getNumberOfConnections(vertex):
    return len(vertex["connections"])

def createChainHistory(current, history):
    current.sort(key=getNumberOfConnections)
    history.append(deepcopy(current))
    if len([vertex for vertex in history[-1] if vertex["color"] not in ["r", "g", "b", "y"]]) == 1:
        return history
    for vertexi in [vertex for vertex in current if vertex["id"] in current[0]["connections"]]:
        vertexi["connections"].remove(current[0]["id"])
    current.remove(current[0])
    return createChainHistory(current=deepcopy(current), history=history)

def sameColorRegion(colorPair, vertexB, currentVertex, previousVertex, allVertices):
    if currentVertex["id"] is vertexB["id"]: return True
    possibleNextVertices = [vertex for vertex in allVertices if vertex["id"] in currentVertex["connections"] and vertex["color"] in colorPair and vertex["id"] is not previousVertex["id"]]
    if len(possibleNextVertices) == 0: return False
    isSameColorRegion = False
    for vertexi in possibleNextVertices:
        if sameColorRegion(colorPair=colorPair, vertexB=vertexB, currentVertex=copy(vertexi), previousVertex=copy(currentVertex), allVertices=allVertices):
            isSameColorRegion = True
            break
    return isSameColorRegion

def invertVertexChain(colorPair, currentVertex, previousVertex, allVertices, changedVertices):
    if currentVertex["color"] is colorPair[1]: 
        for vertexi in allVertices:
            if vertexi["id"] is currentVertex["id"]:
                vertexi["color"] = copy(colorPair[0])
                changedVertices.append(copy(vertexi))
    else:
        for vertexi in allVertices:
            if vertexi["id"] is currentVertex["id"]:
                vertexi["color"] = copy(colorPair[1])
                changedVertices.append(copy(vertexi))
    possibleNextVertices = [vertex for vertex in allVertices if vertex["id"] in currentVertex["connections"] and vertex["color"] in colorPair and vertex["id"] is not previousVertex["id"] and vertex["id"] not in [vertex["id"] for vertex in changedVertices]]
    if len(possibleNextVertices) == 0: return changedVertices
    for vertexi in possibleNextVertices:
        changedVertices.extend(invertVertexChain(colorPair=colorPair, currentVertex=copy(vertexi), previousVertex=copy(currentVertex), allVertices=deepcopy(allVertices), changedVertices=copy(changedVertices)))
    changedVertices = list(set(changedVertices))
    for changedVertex in changedVertices:
        for vertexi in allVertices:
            if changedVertex["id"] is vertexi["id"]:
                vertexi["color"] = copy(changedVertex["color"])
    return allVertices

def caseDegreeFour(baseVertex, current):
    vertexA = ""
    vertexB = ""
    for vertexi in current:
        if vertexi["id"] in baseVertex["connections"]:
            vertexA = copy(vertexi)
            break
    for vertexi in current:
        if vertexi["id"] in baseVertex["connections"] and vertexi["id"] not in vertexA["connections"]:
            vertexB = copy(vertexi)

    if sameColorRegion(colorPair=[vertexA["color"], vertexB["color"]], vertexB=copy(vertexB), currentVertex=copy(vertexA), previousVertex=copy(vertexA), allVertices=deepcopy(current)):
        for vertexi in current:
            if vertexi["id"] == baseVertex["connections"] and vertexi["id"] is not vertexA["id"] and vertexi["id"] is not vertexB["id"]: 
                vertexA = copy(vertexi)
                break
        for vertexi in current:
            if vertexi["id"] in baseVertex["connections"] and vertexi["id"] not in vertexA["connections"]:
                vertexA = copy(vertexi)
                break
    current = invertVertexChain(colorPair=[vertexA["color"], vertexB["color"]], currentVertex=copy(vertexA), previousVertex=copy(vertexA), allVertices=deepcopy(current), changedVertices=[])
    colorsUsed = [vertex["color"] for vertex in current if vertex["id"] in baseVertex["connections"]]
    [vertex for vertex in current if vertex["id"] is baseVertex["id"]][0]["color"] = [color for color in ["r", "g", "b", "y"] if color not in colorsUsed][0]
    return current

def colorGraph(history):
    current = history.pop()

    while len(history) != 0:
        for vertexHistory in history[-1]:
            for vertexCurrent in current:
                if vertexCurrent["id"] is vertexHistory["id"]:
                    vertexHistory["color"] = copy(vertexCurrent["color"])
                    break
        current = history.pop()
        for vertexi in current:
            if vertexi["color"] in ["r", "g", "b", "y"]: continue
            numberOfConnections = len(vertexi["connections"])
            if numberOfConnections < 4:
                colorsUsed = [vertex["color"] for vertex in current if vertex["id"] in vertexi["connections"]]
                vertexi["color"] = [color for color in ["r", "g", "b", "y"] if color not in colorsUsed][0]
                continue
            if numberOfConnections == 4:
                current = deepcopy(caseDegreeFour(baseVertex=copy(vertexi), current=deepcopy(current)))
                continue
            if numberOfConnections == 5:
                continue
    return current


def checkAndPrintResult(output):
    ansGud = True
    for vertexi in output:
        colorsUsed = [vertex["color"] for vertex in output if vertex["id"] in vertexi["connections"]]
    if vertexi["color"] in colorsUsed:
        ansGud = False
    print(output)
    if ansGud:
        print("Gud - HELLL YEAHHH!")
    else:
        print("Bad - NOOOOOOOOO!!!")

if __name__ == "__main__":
    startTime = time()

    input = [{"id":"1","connections":["2","3","4","5"],"color":""},{"id":"2","connections":["1","5","7","8","9","3"],"color":""},{"id":"3","connections":["1","2","9","12","16","19","4"],"color":""},{"id":"4","connections":["1","5","6","3","19","20"],"color":""},{"id":"5","connections":["7","2","1","4","6"],"color":""},{"id":"6","connections":["5","4"],"color":""},{"id":"7","connections":["8","2","5"],"color":""},{"id":"8","connections":["10","9","2","7"],"color":""},{"id":"9","connections":["8","10","12","3","2"],"color":""},{"id":"10","connections":["11","12","9","8"],"color":""},{"id":"11","connections":["10","12","13"],"color":""},{"id":"12","connections":["3","9","10","11","13","15","16"],"color":""},{"id":"13","connections":["11","12","15","14"],"color":""},{"id":"14","connections":["13","15","17"],"color":""},{"id":"15","connections":["12","13","14","17","16"],"color":""},{"id":"16","connections":["3","12","15","17","19"],"color":""},{"id":"17","connections":["14","15","16","19","18"],"color":""},{"id":"18","connections":["17","19","20"],"color":""},{"id":"19","connections":["3","4","20","18","17","16"],"color":""},{"id":"20","connections":["18","19","4"],"color":""}]

    checkAndPrintResult(colorGraph(createChainHistory(current=deepcopy(input), history=[])))

    endTime = time()
    print("Execution time:", (endTime-startTime), "s")