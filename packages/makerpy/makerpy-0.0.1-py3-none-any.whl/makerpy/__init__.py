# python setup.py sdist
# python3 setup.py sdist bdist_wheel

# python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

import test

def main():
    test.main()