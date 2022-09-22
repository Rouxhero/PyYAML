@echo off
echo Installing dependency
pip install sismic 
pip install PyQt5    
echo @REM Auto created > run.bat
echo @echo off >> run.bat
echo  cd src/ >> run.bat
echo python main.py >> run.bat
