install:
	pip install --upgrade .

develop:
	python setup.py develop

test:
	python patois/commands.py init
	chmod -R 777 patois/utils/models
	python -m pytest tests/

models:
	python patois/commands.py init

documentation:
	$(MAKE) -C docs html
	open docs/build/html/index.html

docker-build:
	$(eval VERSION := `python -c "import patois; print patois.__version__;"`.test)
	docker build -t patois .
	docker tag patois patois:$(VERSION)

help:
	@echo "    install"
	@echo "        Install or update the package."
	@echo "    develop"
	@echo "        Install the package for development."
	@echo "    test"
	@echo "        Run tests with py.test and doctests."
	@echo "    documentation"
	@echo "        Generate documentation with Sphinx."
	@echo "    submit-coverage"
	@echo "        Submit new coverage report to code climate."
	@echo "    docker-build"
	@echo "        Build the patois docker image locally."