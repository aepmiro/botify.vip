@echo off
setlocal

:: Define paths
set "VERSION_URL=https://raw.githubusercontent.com/aepmiro/botify.vip/main/version.txt"
set "LOCAL_VERSION_FILE=version.txt"

:: Fetch latest version from GitHub
echo Checking for updates...
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%VERSION_URL%', 'latest_version.txt')"

:: Read local and latest versions
set /p LOCAL_VERSION=<%LOCAL_VERSION_FILE%
set /p LATEST_VERSION=<latest_version.txt

:: Compare versions
if "%LOCAL_VERSION%"=="%LATEST_VERSION%" (
    echo Bot is up-to-date (version %LOCAL_VERSION%).
) else (
    echo Update available! Latest version: %LATEST_VERSION%
    echo Please update your bot manually.
)

:: Cleanup
del latest_version.txt
pause
exit