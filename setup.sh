#!/bin/bash

# Check if the .env file exists
if [ ! -f .env ]; then
  echo "Creating a new .env file"
  touch .env
fi

# Add or update Azure Speech environment variables in .env file
echo "AZURE_SPEECH_KEY=8ada5b541bcb4f5ebbcb0d80eb332903" >> .env
echo "AZURE_SERVICE_REGION=eastus" >> .env

# Install dependencies
pip install -r requirements.txt
