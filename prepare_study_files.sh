rm -r ./study_files
mkdir -p ./study_files/chess-ppl/
mkdir -p ./study_files/chess-vanilla/
cp -r ./case-studies/chess/template-ppl/* ./study_files/chess-ppl/
cp -r ./case-studies/chess/template-vanilla/* ./study_files/chess-vanilla/
rm -r ./study_files/chess-ppl/__pycache__
rm -r ./study_files/chess-vanilla/__pycache__


python3 -m venv ./study_files/chess-ppl/venv/  
source ./study_files/chess-ppl/venv/bin/activate
python3 setup.py install


python3 -m venv ./study_files/chess-vanilla/venv/  
source ./study_files/chess-vanilla/venv/bin/activate
python3 setup.py install


mkdir -p ./study_files/tic-tac-toe-ppl/
mkdir -p ./study_files/tic-tac-toe-vanilla/


cp -r ./case-studies/tic-tac-toe/template-ppl/* ./study_files/tic-tac-toe-ppl/
cp -r ./case-studies/tic-tac-toe/template-vanilla/* ./study_files/tic-tac-toe-vanilla/


python3 -m venv ./study_files/tic-tac-toe-ppl/venv/  
source ./study_files/tic-tac-toe-ppl/venv/bin/activate
python3 setup.py install

python3 -m venv ./study_files/tic-tac-toe-vanilla/venv/  
source ./study_files/tic-tac-toe-vanilla/venv/bin/activate
python3 setup.py install


cd ./study_files/
zip -r ./tic_tac_toe-ppl.zip ./tic-tac-toe-ppl/
zip -r ./tic_tac_toe-vanilla.zip ./tic-tac-toe-vanilla/


zip -r ./chess-ppl.zip ./chess-ppl/
zip -r ./chess-vanilla.zip ./chess-vanilla/