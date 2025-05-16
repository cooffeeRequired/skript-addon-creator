#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install it first."
    exit 1
fi

# Check if required packages are installed
python3 -c "import requests, inquirer, colorama" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required packages..."
    pip3 install requests inquirer colorama
fi

# Run the script
python3 src/main.py 