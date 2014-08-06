test: clean
	python2 Test*.py; make clean
	python3 Test*.py; make clean

clean:
	rm -rf *.pyc __pycache__
