lint:
	python -m isort -c -rc scoreboard/
	python -m black --check scoreboard/
	python -m flake8 --select F --per-file-ignores="__init__.py:F401" scoreboard/
	python -m mypy scoreboard/

format:
	python -m isort -rc scoreboard/
	python -m black scoreboard/

test:
	pip install .
	coverage run -m pytest
	coverage report -m
