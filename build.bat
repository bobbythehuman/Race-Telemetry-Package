@echo off
setlocal enabledelayedexpansion

echo ============================================
echo   Python Package Build ^& Upload Script
echo ============================================
echo.

REM ---------------------------------------------
REM 1. Ask whether this is a test build or a real release
REM ---------------------------------------------
set TARGET=
:ask_target
echo Is this build for TESTING (TestPyPI) or LIVE (PyPI)?
set /p CHOICE="Type T for TestPyPI or L for Live PyPI: "

if /i "%CHOICE%"=="T" (
    set TARGET=testpypi
    set TARGET_NAME=TestPyPI
) else if /i "%CHOICE%"=="L" (
    set TARGET=pypi
    set TARGET_NAME=PyPI ^(LIVE^)
) else (
    echo Invalid choice, please type T or L.
    echo.
    goto ask_target
)

echo.
echo Selected target: %TARGET_NAME%
echo.

REM ---------------------------------------------
REM 2. Delete old build artefacts
REM ---------------------------------------------
echo Cleaning old build folders...

if exist dist (
    rmdir /s /q dist
    echo   - Removed dist\
)
if exist build (
    rmdir /s /q build
    echo   - Removed build\
)

REM Remove any *.egg-info folders (name varies per project)
for /d %%D in (*.egg-info) do (
    rmdir /s /q "%%D"
    echo   - Removed %%D
)
for /d %%D in (src\*.egg-info) do (
    rmdir /s /q "%%D"
    echo   - Removed %%D
)

echo Clean complete.
echo.

REM ---------------------------------------------
REM 3. Run tests before building
REM ---------------------------------------------
echo Running pytest checks...
pytest .\tests\test_main.py .\tests\test_digestion.py --disable-warnings

if errorlevel 1 (
    echo.
    echo Pytest failed. Build aborted.
    pause
    exit /b 1
)

echo Pytest checks passed.
echo.

REM ---------------------------------------------
REM 4. Build the package
REM ---------------------------------------------
echo Building package...
python -m build

if errorlevel 1 (
    echo.
    echo Build failed. Aborting - nothing will be uploaded.
    pause
    exit /b 1
)

echo.
echo Build succeeded. Files in dist\:
dir /b dist
echo.

REM ---------------------------------------------
REM 5. Wait for user confirmation before uploading
REM ---------------------------------------------
echo You are about to upload to: %TARGET_NAME%
set /p CONFIRM="Proceed with upload? (Y/N): "

if /i not "%CONFIRM%"=="Y" (
    echo.
    echo Upload cancelled by user. Build files remain in dist\.
    pause
    exit /b 0
)

echo.
echo Uploading to %TARGET_NAME%...

if "%TARGET%"=="testpypi" (
    python -m twine upload --repository testpypi dist/*
) else (
    python -m twine upload dist/*
)

if errorlevel 1 (
    echo.
    echo Upload failed. Check the error above.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Upload to %TARGET_NAME% complete.
echo ============================================
pause