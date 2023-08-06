.PHONY: test sdist bdist_wheel_linux bdist_windows

MIN_COVERAGE_PERCENTAGE=94

VENV_PATH=${PWD}/.py-env

clean:
	python setup.py clean

build:
	echo "TODO: build"

test:
	coverage erase
	coverage run -m unittest discover log_indented '*_test.py' --locals -v
	coverage report -m --fail-under $(MIN_COVERAGE_PERCENTAGE)

format:
	black log_indented --line-length 140 


lint:
	black --check log_indented --line-length 140
	mypy log_indented
	# stop the build if there are Python syntax errors or undefined names.
	flake8 log_indented --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings.
	flake8 log_indented --count --exit-zero --max-complexity=10 --max-line-length=140 --statistics
	# run pylint
	pylint -j 0 log_indented

env:
	@python3.9 -m venv $(VENV_PATH) --prompt "🟢"
	@source $(VENV_PATH)/bin/activate && \
		pip install -r requirements.txt
	@echo
	@echo "To activate your Python environment, run:"
	@echo "    source $(VENV_PATH)/bin/activate"

install-dependencies:
	source $(VENV_PATH)/bin/activate && \
	    pip-compile --output-file requirements.txt requirements.in && \
	    pip install -r requirements.txt


sdist:
	python setup.py sdist
