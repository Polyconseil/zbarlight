.PHONY: test docs

update:
	pip install -e .

clean:
	find zbarlight "(" -name 'zbarlight*.so' -or -name '*.egg' -or -name '*.pyc' -or -name '*.pyo' ")" -delete
	find zbarlight -type d "(" -name build -or -name __pycache__ ")" -exec rm -r {} \;

docs:
	python setup.py build_sphinx

test:
	python setup.py test
