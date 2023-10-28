set APPLICATION_NAME=weapon_detector

goto %1

:install
  python -m venv venv
  call "venv/Scripts/activate.bat"
  pip install --no-binary opencv-python opencv-python
  pip install -Ur requirements.txt
  pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu
  pip install ultralytics
goto end
  
:build
  call "venv/Scripts/activate.bat"
  pyinstaller %APPLICATION_NAME%.spec
  cp -r ./venv/Lib/site-packages/ultralytics ./dist/%APPLICATION_NAME%/%APPLICATION_NAME%
goto end

:end
