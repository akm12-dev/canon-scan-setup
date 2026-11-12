#!/bin/bash
# Compile Canon Scan Setup pour macOS : dist/Canon Scan Setup.app + dist/CanonScanSetup-<version>-macos.dmg
# Usage : bash build_mac.sh
#   - Python de python.org (« universal2 ») recommandé : l'application fonctionne alors sur Mac Intel et Apple Silicon.
#   - L'application est signée « ad hoc » (pas de compte Apple Developer) : Gatekeeper avertit au premier lancement.
set -e
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
APP="Canon Scan Setup"
VERSION=$("$PY" -c "import canonscan; print(canonscan.VERSION)")
ARCH="${TARGET_ARCH:-universal2}"

"$PY" -m pip install --upgrade pyinstaller

# Icône .icns à partir de assets/icon-256.png
ICONSET=build/icon.iconset
rm -rf "$ICONSET"; mkdir -p "$ICONSET"
for s in 16 32 128 256; do
  sips -z $s $s assets/icon-256.png --out "$ICONSET/icon_${s}x${s}.png" >/dev/null
  d=$((s * 2)); [ $d -le 256 ] && sips -z $d $d assets/icon-256.png --out "$ICONSET/icon_${s}x${s}@2x.png" >/dev/null
done
iconutil -c icns "$ICONSET" -o build/icon.icns

"$PY" -m PyInstaller --noconfirm --clean --windowed --name "$APP" \
  --osx-bundle-identifier com.akm12.canonscansetup --target-arch "$ARCH" \
  --icon build/icon.icns --add-data "assets/icon-256.png:assets" CanonScanSetup.py

PLIST="dist/$APP.app/Contents/Info.plist"
plutil -replace CFBundleShortVersionString -string "$VERSION" "$PLIST"
plutil -replace CFBundleVersion -string "$VERSION" "$PLIST"
plutil -replace NSHumanReadableCopyright -string "AKM12 - akm12.com" "$PLIST"
plutil -replace LSMinimumSystemVersion -string "11.0" "$PLIST"
plutil -replace NSLocalNetworkUsageDescription -string \
  "Canon Scan Setup communique avec l'imprimante Canon de votre réseau local (test de connexion, scan vers dossier et relais e-mail)." "$PLIST"
codesign --force --deep --sign - "dist/$APP.app"
codesign --verify --deep --strict "dist/$APP.app"

# Image disque : l'application + un raccourci vers le dossier Applications
DMG="dist/CanonScanSetup-$VERSION-macos.dmg"
STAGE=build/dmg
rm -rf "$STAGE" "$DMG"; mkdir -p "$STAGE"
cp -R "dist/$APP.app" "$STAGE/"
ln -s /Applications "$STAGE/Applications"
hdiutil create -volname "$APP $VERSION" -srcfolder "$STAGE" -ov -format UDZO "$DMG" >/dev/null
echo "OK : dist/$APP.app"
echo "OK : $DMG"
