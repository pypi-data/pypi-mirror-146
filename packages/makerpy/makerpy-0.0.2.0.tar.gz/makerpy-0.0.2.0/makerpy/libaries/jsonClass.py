import json

class main:
    def openFile(name):
        f = open(name, "r")
        out = json.load(f)
        f.close()
        return out