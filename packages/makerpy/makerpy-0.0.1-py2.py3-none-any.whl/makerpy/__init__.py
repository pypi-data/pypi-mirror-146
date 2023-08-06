# python setup.py sdist
# python3 setup.py bdist_wheel --universal
# python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

import test

def main():
    test.main()