#!/bin/bash
apt-get update && apt-get install -y wget curl gnupg
apt-get install -y libnss3 libatk-bridge2.0-0 libgtk-3-0 libxss1 libasound2
pip install playwright
python -m playwright install