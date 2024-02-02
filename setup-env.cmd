@echo off
py -m venv .venv
.venv\Scripts\activate

py -m pip install --upgrade pip
py -m pip --version

py -m pip install -r requirements.txt