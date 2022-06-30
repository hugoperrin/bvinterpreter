lint:
	echo using source folder: $(srcfolder)
	python -m black ${srcfolder} tests; python3 -m isort --multi-line 3 --trailing-comma --force-grid-wrap 0 --use-parentheses --skip __init__.py  --line-width 88 -rc ${srcfolder} tests

flake8:
	python -m flake8 --exclude=tests/bdd/features/steps,${srcfolder}/externals ${srcfolder} tests

mypy_setup:
	echo "you need to run mypy at least once before"
	mypy --install-types

mypy:
	python -m mypy ${srcfolder} --explicit-package-bases --namespace-packages --ignore-missing-imports
