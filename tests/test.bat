echo off
cls
echo starting testing app
del main.db
pytest UserClassAllMethodstest.py -v
