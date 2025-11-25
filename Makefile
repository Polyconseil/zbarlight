.PHONY: update docs quality Quality tests clean

update:
	pip install -r requirements-dev.txt
	python setup.py build_ext --inplace
	pip install -e .

docs:
	sphinx-build -W -n -b html docs ./build/sphinx/html

quality:
	isort --check-only --diff .
	pylint --reports=no --score=no setup.py src tests
	python setup.py check --strict --metadata --restructuredtext
	check-manifest

Quality:  # not used in tests
	vulture --exclude=build/ src tests setup.py

tests:
	pytest tests/

clean:
	-find src "(" -name '*.so' -or -name '*.egg' -or -name '*.pyc' -or -name '*.pyo' ")" -delete
	-find src -type d -name __pycache__ -exec rm -r {} \;
	-rm -rf .tox .cache build dist
