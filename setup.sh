#!/bin/bash

# Read environment variables from secrets.toml
SPEECH_KEY=$(toml get secrets.toml env.SPEECH_KEY)
SERVICE_REGION=$(toml get secrets.toml env.SERVICE_REGION)

# Set environment variables
export SPEECH_KEY=$SPEECH_KEY
export SERVICE_REGION=$SERVICE_REGION

# Run the Streamlit app
streamlit run your_app.py
