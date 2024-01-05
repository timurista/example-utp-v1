#!/bin/bash

# Define the path for the virtual environment
VENV_PATH="venv"

# Define the Python version
PYTHON_VERSION="python3.9"

# Check if the virtual environment already exists
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating a virtual environment with $PYTHON_VERSION"
    # Create a virtual environment
    $PYTHON_VERSION -m venv $VENV_PATH
fi

# Activate the virtual environment
source $VENV_PATH/bin/activate

# Check if requirements.txt exists and install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt"
    pip install -r requirements.txt
else
    echo "No requirements.txt found, skipping dependency installation"
fi

echo "Virtual environment is ready and dependencies are installed."