echo "Installing dependency"
pip install sismic 
pip install PyQt5 
echo "
#Auto created
cd src/
python3 main.py 
" > run.sh
chmod +x run.sh
