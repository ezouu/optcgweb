#!/bin/bash

# Ensure that Node.js is installed
if ! command -v node &> /dev/null
then
    echo "Node.js is not installed. Please install Node.js to proceed."
    exit 1
fi

# Ensure the required Node.js modules are installed
if [ ! -d "node_modules" ]; then
    echo "Installing necessary packages..."
    npm install playwright
fi

# Run the polscrape2.js script
echo "Running polscrape2.js..."
node polscrape2.js
