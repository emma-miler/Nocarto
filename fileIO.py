import xmltodict
import pprint
import json
from itertools import chain
import re

def parseFile(inFile):
    if inFile[-3:] == ".mm":
        with open(inFile) as fd:
            doc = xmltodict.parse(fd.read())

            conv = {"version": "0.0.1"}

            main = doc["map"]["node"]

            test = makeNode(None, main, "mindmap")

            pprint.pprint(test)
            print("\n\n\n")

            globals()["nodeList"] = []
            x = untangleTree(test)
            pprint.pprint(globals()["nodeList"])
            print("\n\n\n")

            return globals()["nodeList"]


        #pprint.pprint(main)
    else:
        raise BaseException("Not yet implemented")

def makeNode(parent, inNode, inputType):
    retNode = {}
    try:
        retNode["id"] = int(re.sub("[^0-9]", "", inNode["@ID"]))
    except:
        retNode["id"] = 0
    if "@TEXT" in inNode:
        retNode["text"] = inNode["@TEXT"]
    else:
        # TODO: parse rich context, like, at all
        retNode["text"] = "UNPARSED STRING"
    if inputType == "mindmap":
        if "@POSITION" not in inNode:
            retNode["position"] = 0
        else:
            retNode["position"] = -1 if inNode["@POSITION"] == "left" else 1
    else:
        pass
        # TODO: implement positioning for freemaps
    children = []
    retNode["connections"] = []
    if parent is not None:
        retNode["connections"].append(parent)
    if "node" in inNode:
        if type(inNode["node"]) == list:
            for node in inNode["node"]:
                x = makeNode(retNode["id"], node, inputType)
                children.append(x)
                if type(x) == list:
                    retNode["connections"].append(x[-1]["id"])
                else:
                    retNode["connections"].append(x["id"])
        else:
            x = makeNode(retNode["id"], inNode["node"], inputType)
            children.append(x)
            if type(x) == list:
                retNode["connections"].append(x[-1]["id"])
            else:
                retNode["connections"].append(x["id"])
            
        children.append(retNode)
        return children
    else:
        return retNode

def untangleTree(node):
    if type(node) == list:
        for subNode in node:
            untangleTree(subNode)
    elif type(node) == dict:
        globals()["nodeList"].append(node)
        return