#!/bin/bash

echo "▶ Installation Playwright avec Chromium manuellement..."

# Installation Playwright (Python)
pip install playwright

# Installation manuelle de Chromium dans le bon chemin
python -m playwright install chromium

echo "✅ Installation Playwright + Chromium OK"