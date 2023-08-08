#!/bin/bash

python3 -m venv testenv

source testenv/bin/activate

pip3 install -r requirements.txt

# 執行pytest測試
pytest 

allure generate allure-results -o report --clean



