APPLICATION_NAME = weapon_detector

install_linux: ##@Application Create Virtual Enviroment and Install Requirements on Linux
	pip cache purge && \
	python -m venv venv && \
	source venv/bin/activate && \
	pip install -Ur requirements.txt && \
	pip uninstall -y opencv-python && \
	pip install opencv-python-headless

install_windows: ##@Application Create Virtual Enviroment and Install Requirements on Windows
	
	python -m venv venv && \
	activate venv/bin/activate && \
	pip install -Ur requirements.txt && \
	pip uninstall -y opencv-python && \
	pip install opencv-python-headless

format:  ##@Code Reformat code with isort and flake8
	python3 -m flake8 $(APPLICATION_NAME) --config=./setup.cfg
	python3 -m isort $(APPLICATION_NAME) --settings-file=./setup.cfg

run:  ##@Application Run application
	python3 -m $(APPLICATION_NAME)

run_prod:   ##@Application Run build application
	./dist/$(APPLICATION_NAME)/$(APPLICATION_NAME)

convert:  ##@Code convert .ui files and .qrc files in .py
	cd ./$(APPLICATION_NAME)/qt && python auto_generate_files.py "../forms/" -i "resources"

build_linux:  ##@Code build in Application with Pyinstaller on Linux
	make install_linux && \
	sudo pyinstaller $(APPLICATION_NAME).spec && \
	cp -r ./venv/lib/python3.11/site-packages/ultralytics ./dist/$(APPLICATION_NAME)/

build_windows:  ##@Code build in Application with Pyinstaller on Windows
	make install_windows && \
	pyinstaller $(APPLICATION_NAME).spec && \
	cp -r ./venv/lib/python3.11/site-packages/ultralytics ./dist/$(APPLICATION_NAME)/

clean:  ##@Code Clean directory from garbage files
	rm -fr *.pyc *.egg-info dist build venv
