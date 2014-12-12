.PHONY: test docs

docs:
	python setup.py build_sphinx

test:
	python setup.py test
