#!/bin/bash
# Compile Canon Scan Setup en application macOS (dist/CanonScanSetup.app)
# Usage : bash build_mac.sh   (avec le Python de python.org)
set -e
cd "$(dirname "$0")"
python3 -m pip install --upgrade pyinstaller
python3 -m PyInstaller --noconfirm --windowed --name CanonScanSetup \
  --osx-bundle-identifier com.canonscansetup.app CanonScanSetup.py
echo "OK : dist/CanonScanSetup.app"
