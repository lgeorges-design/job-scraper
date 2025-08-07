#!/bin/bash

echo "▶ Installation Playwright..."

# Force l'installation du binaire Chromium dans un environnement compatible Render
npx playwright install chromium

echo "✅ Chromium installé"
