# -*- coding: utf-8 -*-
from flask import jsonify


class Tree():

    def __init__(self):
        self.tree = []
        self.index = {}
        self.parentIndex = {}
        self.cont = 0
        self.childProperty = "children"
        self.idProp = "id"
        self.klass = []

    #/**
    #*    This method inserts a node to the Tree, the child param may contain an
    #*    "id" property that will be use as a "key", if the child param doesn't contains
    #*    an "id" property a generated "key" is given to the node.
    #*
    #*    @child the node to insert
    #*    @parentKey(optional) The parent key where the node will be inserted, if null
    #*    the node is inserted in the root of the Tree
    #*/

    def addChild(self, child, parentKey=None):
        #child[self.idProp] = 'item_' + str(self.cont)
        key = child[self.idProp]
        child["leaf"] = True
        if child["klass"] not in self.klass:
            self.tree.append(child)
        self.klass.append(child["klass"])
        if self.containsKey(parentKey):
            # added to the existing node
            self.index[key] = child
            parent = self.index[parentKey]
            if self.childProperty in parent:
                childProp = parent[self.childProperty]
                childProp.update({key: child})
            else:
                parent["leaf"] = False
                parent[self.childProperty] = child

            self.index[parentKey] = parent

        else:
            # added to the root
            self.index[parentKey] = {self.childProperty: child}
        #print self.tree
        self.cont += 1

    def getNode(self, key):
        return self.index[key]

    def removeNode(self, key):
        pass

    def containsKey(self, parentKey):
        containsKey = False
        if parentKey is not None:
            if parentKey in self.index.keys():
                containsKey = True
                return containsKey
            else:
                self.index[parentKey] = {}
                return containsKey

    def toJson(self):
        return jsonify(tree=self.tree)

    def setChildProperty(self, prop):
        self.childProperty = prop

    def setIdProperty(self, idProp):
        self.idProp = idProp

    def getRoot(self):
        return self.tree
