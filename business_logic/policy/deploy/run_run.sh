#!/bin/bash -e

cd /Users/chenxinlu/Developer/MrWind-Dispatcher
. venv/bin/activate
export PYTHONPATH="/Users/chenxinlu/Developer/MrWind-Dispatcher"
env | grep PYTHONPATH
cd /Users/chenxinlu/Developer/MrWind-Dispatcher/business_logic_api/policy
uwsgi --chdir=/Users/chenxinlu/Developer/MrWind-Dispatcher/business_logic_api/policy --http 0.0.0.0:5009 --wsgi-file run_as_wsgi_app.py -M -p 1 --async 2000 --ugreen --enable-threads --disable-logging --die-on-term