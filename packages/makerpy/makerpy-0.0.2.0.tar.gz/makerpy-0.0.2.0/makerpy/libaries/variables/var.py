import json

f = open("makerpy/libaries/variables/variables.json", "r")
var = json.load(f)
f.close()

def save():
    global var
    f = open("makerpy/libaries/variables/variables.json", "w")
    json.dump(var, f, indent=4)
    f.close()

class main:
    def set(name, value):
        global var
        var[name] = value
        save()
    def get(name):
        global var
        return var[name]
    def reset():
        global var
        var = {}
        save()
    def kill(name):
        global var
        del var[name]
        save()
    def sum(name, sum):
        global var
        var[name] = eval(str(var[name]) + str(sum))
        save()
    def close():
        global var
        var = {}
    def open():
        global var
        f = open("makerpy/libaries/variables/variables.json", "r")
        var = json.load(f)
        f.close()