#!/bin/bash

python3 -m venv venv     
source venv/bin/activate  
pip3 install wheel setuptools twine
python3 setup.py develop