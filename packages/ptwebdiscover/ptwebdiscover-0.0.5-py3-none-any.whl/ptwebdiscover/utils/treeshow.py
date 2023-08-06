import json
import string    
import random

from treelib import Node, Tree


def url_list_to_json_tree(urls):
    paths = []
    for item in urls:
        split = item.split('/')
        paths.append(split[2:-1])
        paths[-1].append(split[-1])

    root = {}
    for path in paths:
        branch = root.setdefault(path[0], [{}, []])
        for step in path[1:-1]:
            branch = branch[0].setdefault(step, [{}, []])
        branch[1].append(path[-1])
    deleter(root)
    return(root)

def walker(courls):
    if isinstance(courls, list):
        for item in courls:
            yield item
    if isinstance(courls, dict):
        for item in courls.values():
            yield item

def deleter(courls):
    for data in walker(courls):
        if data == [] or data == {}:
            courls.remove(data)
        deleter(data)

def createTree(parent, files):
    for key in files:
        if not parent:
            identifier = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)))
            tree.create_node(key, identifier)
        if not key:
            continue
        try:
            value = files[key]
            if parent:
                identifier = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)))
                tree.create_node(key, identifier, parent=parent)
            createTree(identifier, value)
        except:
            if type(key) == dict or type(key) == list:
                createTree(parent, key)
            else:
                identifier = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)))
                tree.create_node(key, identifier, parent=parent)
