.PHONY: test docs

update:
	pip install -r requirements-dev.txt
	python setup.py build_ext --inplace
	pip install -e .

clean:
	find src "(" -name '*.so' -or -name '*.egg' -or -name '*.pyc' -or -name '*.pyo' ")" -delete
	find src -type d -name __pycache__ -exec rm -r {} \;

docs:
	python setup.py build_sphinx

test:
	py.test
