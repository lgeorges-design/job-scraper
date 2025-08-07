#!/bin/bash

echo "▶ Installation des dépendances système..."
apt-get update && apt-get install -y libnss3 libatk-bridge2.0-0 libxss1 libasound2 libxshmfence1 libgbm1 libgtk-3-0 libdrm2

echo "▶ Installation de Playwright..."
playwright install chromium

echo "✅ Build terminé"