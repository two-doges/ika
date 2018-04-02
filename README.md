# ika
a anonymous forum

## Pre run

use `pipenv install`

you must set up mysql, and then write a config.py  
look at [config sample](https://github.com/two-doges/ika/blob/master/config_sample.py) for more details.  
then run `pipenv run python init.py`

## how to run

for debug use, just `pipenv run python ika.py`

otherwise you need gunicorn (or something like that)
