# delete everything in dist
# UPDATE FILE VERSION
# python setup.py sdist
# python3 setup.py sdist bdist_wheel
# python -m twine upload dist/* --verbose
import importlib
from turtle import screensize
pg = importlib.import_module('pygame')

using = importlib.import_module('libaries.pygameClass')
pygame = using.pygame

using = importlib.import_module('libaries.variables.var')
var = using.main