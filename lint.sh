#!/bin/bash

# Formatar com Black
echo "Running Black..."
black .

# Ordenar imports
echo "Running isort..."
isort .

# Verificar com Flake8
echo "Running Flake8..."
flake8 .
