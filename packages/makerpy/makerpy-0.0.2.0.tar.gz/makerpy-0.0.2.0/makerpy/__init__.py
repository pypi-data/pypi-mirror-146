# delete everything in dist
# UPDATE FILE VERSION
# python setup.py sdist
# python3 setup.py sdist bdist_wheel
# python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/* --verbose
import importlib
pg = importlib.import_module('pygame')

using = importlib.import_module('libaries.pygameClass')
pygame = using.pygame

using = importlib.import_module('libaries.variables.var')
var = using.main

using = importlib.import_module('libaries.rand')
rand = using.main

using = importlib.import_module('libaries.jsonClass')
json = using.main