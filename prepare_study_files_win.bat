rm -r .\study_files


mkdir -p .\study_files\tic-tac-toe-ppl\
cp -r .\case-studies\tic-tac-toe\template-ppl\* .\study_files\tic-tac-toe-ppl\


python -m venv .\study_files\tic-tac-toe-ppl\venv\  
study_files\tic-tac-toe-ppl\venv\bin\activate
python setup.py install

cd .\study_files\
