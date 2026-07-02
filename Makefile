PYTHON_CMD = python3
MAIN_FILE = a_maze_ing.py
DEFAULT_CONFIG_FILE = ./mazegen/Resources/Config/default_config.txt
CONFIG_FILE = config.txt
REQUIREMENTS_FILE = requirements.txt

install:
	@$(PYTHON_CMD) -m pip install --upgrade pip > /dev/null 2>&1
	@$(PYTHON_CMD) -m pip install -r ${REQUIREMENTS_FILE}

build:
	@ ${PYTHON_CMD} -m build -q 
	@ cp dist/mazegen-*.whl .

run:
	@ if [ ! -f ./$(CONFIG_FILE) ]; then 						\
		echo "WARNING: not ./"$(CONFIG_FILE)" file found."; 	\
		echo "Generating default config file ./"$(CONFIG_FILE); \
		cp ${DEFAULT_CONFIG_FILE} ${CONFIG_FILE};				\
	fi
	@ ${PYTHON_CMD} ${MAIN_FILE} ${CONFIG_FILE}

debug: 
	@ if [ ! -f ./$(CONFIG_FILE) ]; then 						\
		echo "WARNING: not ./"$(CONFIG_FILE)" file found."; 	\
		echo "Generating default config file ./"$(CONFIG_FILE); \
		cp ${DEFAULT_CONFIG_FILE} ${CONFIG_FILE};				\
	fi
	@ $(PYTHON_CMD) -m pdb ${MAIN_FILE} ${CONFIG_FILE}

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@rm -rf build dist *.egg-info mazegen-*.whl mazegen-*.tar.gz maze_venv maze.txt

lint:
	@${PYTHON_CMD} -m flake8 .
	@$(PYTHON_CMD) -m mypy . --warn-return-any			\
							 --warn-unused-ignores 		\
							 --ignore-missing-imports	\
							 --disallow-untyped-defs	\
							 --check-untyped-defs		

lint-strict:	
	@${PYTHON_CMD} -m flake8 .
	@${PYTHON_CMD} -m mypy --strict .