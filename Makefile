.PHONY: test docs

update:
	pip install -r requirements-dev.txt
	python setup.py build_ext --inplace
	pip install -e .

clean:
	find zbarlight "(" -name 'zbarlight*.so' -or -name '*.egg' -or -name '*.pyc' -or -name '*.pyo' ")" -delete
	find zbarlight -type d "(" -name build -or -name __pycache__ ")" -exec rm -r {} \;

docs:
	python setup.py build_sphinx

test:
	py.test
