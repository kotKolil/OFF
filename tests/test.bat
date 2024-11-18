echo off
cls
echo starting testing app
del main.db
echo testing user class
pytest UserClassAllMethodstest.py -v
echo testing topic class
pytest TopicClassAllMethodstest.py -v
del main.db