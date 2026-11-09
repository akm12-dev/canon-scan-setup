@echo off
REM Compile Canon Scan Setup en un seul fichier CanonScanSetup.exe (dossier dist\)
cd /d "%~dp0"
py -3 -m pip install --upgrade pyinstaller || goto :err
py -3 -m PyInstaller --noconfirm --onefile --windowed --name CanonScanSetup CanonScanSetup.py || goto :err
echo.
echo  OK : dist\CanonScanSetup.exe
pause
exit /b 0
:err
echo  Echec de la compilation.
pause
exit /b 1
