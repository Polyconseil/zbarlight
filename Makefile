.PHONY: test docs

update:
	pip install -r requirements-dev.txt

clean:
	find . "(" -name 'zbarlight*.so' -or -name '*.egg' -or -name '*.pyc' -or -name '*.pyo' ")" -delete
	find -type d "(" -name build -or -name __pycache__ ")" -delete

docs:
	python setup.py build_sphinx

test:
	python setup.py test
