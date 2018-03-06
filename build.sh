#!/bin/bash

# create venv
virtualenv reimbursement
virtualenv -p python3 reimbursement

alias python='reimbursement/bin/python3'
alias pip='reimbursement/bin/pip3'

pip install -U googlemaps
pip install requests

