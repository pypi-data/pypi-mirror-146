# delete everything in dist
# python setup.py sdist
# python3 setup.py sdist bdist_wheel
# python -m twine upload dist/* --verbose

import test

def main():
    test.main()