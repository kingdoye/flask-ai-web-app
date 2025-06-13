#!/usr/bin/env bash

echo "⏳ Installing Python 3.10.13 via pyenv..."
pyenv install 3.10.13
pyenv global 3.10.13
python --version

echo "⬆️  Upgrading pip..."
pip install --upgrade pip

echo "📦 Installing dependencies..."
pip install -r requirements.txt
