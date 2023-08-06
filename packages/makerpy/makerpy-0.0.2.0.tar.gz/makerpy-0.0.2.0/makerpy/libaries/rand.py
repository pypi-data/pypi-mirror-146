import random

class private:
    saves = {}

class main:
    def random(mini=0, maxi=0): return random.randint(mini, maxi)
    def randomFloat(mini=0, maxi=0): return random.uniform(mini, maxi)
    def randomItem(inputList=[]): return random.choice(inputList)
    def randomWord(string): return random.choice(string.split(" "))

    def randomSaveSet(name="", mini="", maxi=""): private.saves[name] = main.random(mini, maxi)
    def randomSaveGet(name=""): return private.saves[name]