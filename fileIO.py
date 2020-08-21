import xmltodict
import pprint
import json
from itertools import chain
import re

# Warning: this function is likely to fail on bad data.
# This is currently unsafe and *will* crash the program
def parseFile(inFile):
    if inFile[-3:] == ".mm":
        with open(inFile) as fd:
            doc = xmltodict.parse(fd.read())

            conv = {"version": "0.0.1"}

            main = doc["map"]["node"]

            test = makeMindMapNode(None, main, "mindmap")

            globals()["nodeList"] = []
            x = untangleTree(test)

            return globals()["nodeList"]


        #pprint.pprint(main)
    else:
        raise BaseException("Not yet implemented")

def makeMindMapNode(parent, inNode, inputType):
    retNode = {}
    try:
        retNode["id"] = int(re.sub("[^0-9]", "", inNode["@ID"]))
    except:
        retNode["id"] = 0
    if "@TEXT" in inNode:
        retNode["name"] = inNode["@TEXT"]
    else:
        # TODO: parse rich context, like, at all
        retNode["name"] = "UNPARSED STRING"
    if "@POSITION" not in inNode:
        retNode["position"] = 0
    else:
        retNode["position"] = -1 if inNode["@POSITION"] == "left" else 1
    children = []
    retNode["connections"] = []
    if parent is not None:
        retNode["connections"].append(parent)
        retNode["data"] = {"parent": parent}
    else:
        retNode["data"] = {"parent": None}
            
    if "node" in inNode:
        if type(inNode["node"]) == list:
            for node in inNode["node"]:
                x = makeMindMapNode(retNode["id"], node, inputType)
                children.append(x)
                if type(x) == list:
                    retNode["connections"].append(x[-1]["id"])
                else:
                    retNode["connections"].append(x["id"])
        else:
            x = makeMindMapNode(retNode["id"], inNode["node"], inputType)
            children.append(x)
            if type(x) == list:
                retNode["connections"].append(x[-1]["id"])
            else:
                retNode["connections"].append(x["id"])
            
        children.append(retNode)
        return children
    else:
        return retNode

# This function takes the parsed data from makeMindMapNode() and returns a list of usable nodes to globals()["nodeList"]
# I am aware that this is bad practice, and this needs to be tidied up.
def untangleTree(node):
    if type(node) == list:
        for subNode in node:
            untangleTree(subNode)
    elif type(node) == dict:
        globals()["nodeList"].append(node)
        return

def serializeNode(node):
    return {
            "id": node.id,
            "name": node.name,
            "position": node.position,
            "connections": node.connections,
            "data": node.data # TODO: cull unnecessary MindMap data
    }

def serializeEdge(edge):
    return {
            "node1": edge.node1,
            "node2": edge.node2,
    }


# Save a map object into a file
def saveFile(mapperObject, fileName):
    # TODO: possibly remove duplicate connections
    output = {}
    output["version"] = "0.0.1" # Version numbers currently unused
    nodes = []
    for node in mapperObject.nodes.values():
        savedNode = serializeNode(node)
        nodes.append(savedNode)
    output["nodes"] = nodes
    with open(fileName, "w") as outputFile:
        outputFile.write(json.dumps(output))

# Simply opens the filename and loads the json data into a dictionary
# As with parseFile, this is currently unsafe
def openFile(fileName):
    data = {}
    with open(fileName, "r") as inputFile:
        data = json.load(inputFile)
    return data["nodes"]