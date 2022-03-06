
init:
	pip install -r requirements.txt

.PHONY: test
test:
    PYTHONPATH = . pytest


