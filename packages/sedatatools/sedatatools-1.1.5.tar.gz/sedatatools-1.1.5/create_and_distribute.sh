rm -r ./dist/*
py setup.py sdist
py setup.py bdist_wheel
py -m twine upload dist/*
