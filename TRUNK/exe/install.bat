@echo off 
title To install myaccount.py

:: get the date
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "fullstamp=%YYYY%-%MM%-%DD%_%HH%-%Min%-%Sec%"

:: custimized var
set "ANACONDA_PATH=C:\Users\Acer\"
set "GITHUB_PATH=D:\GitHub\"
set "TOP_MODULE_NAME=myaccount"
set "CONDA_ENV=env_myaccount2p0_v1.0"
set "RELEASE_VER=v1.0"

:: welcome msg
echo Welcome to install myaccount2p0!!
echo Today is "%fullstamp%"

:: activate anaconda3
call %ANACONDA_PATH%anaconda3\Scripts\activate.bat
call conda activate %CONDA_ENV%

if %errorlevel% == 0 (
    goto :gen_dist
) else (
    goto :error
)

:: to gen distrubute
:gen_dist
    cd %~d0
    cd ..\release
    call pip install -r .\%RELEASE_VER%\requirements.txt
    cd ..\distrubute
    attrib +R readme :: change file to read only
    rd /s /q build :: remove dir named build
    del /q * :: remove all file excep RO, /q is no confirm
    call pyinstaller -F -p ..\src\ --distpath . ..\src\%TOP_MODULE_NAME%.py
    cd ..\exe
    mklink "%TOP_MODULE_NAME%.exe" "..\distrubute\%TOP_MODULE_NAME%.exe"
    goto :exit

:error
    echo [ERROR] No %CONDA_ENV% in conda env!!
    call conda env list
    goto :exit

:exit
    :: exit msg
	echo^ ^/__^ ^ ^ ^\^ ^|__^ ^ ^ __^ _^ _^ __^ ^|^ ^|^ _____^ ^ ^ ^/^ ^\^/^ ^\
	echo^ ^ ^ ^/^ ^/^\^/^ ^'_^ ^\^ ^/^ _^`^ ^|^ ^'_^ ^\^|^ ^|^/^ ^/^ __^|^ ^/^ ^ ^/^ ^ ^/
	echo^ ^ ^/^ ^/^ ^ ^|^ ^|^ ^|^ ^|^ ^(_^|^ ^|^ ^|^ ^|^ ^|^ ^ ^ ^<^\__^ ^\^/^\_^/^\_^/^ 
	echo^ ^ ^\^/^ ^ ^ ^|_^|^ ^|_^|^\__^,_^|_^|^ ^|_^|_^|^\_^\___^/^\^/^ ^\^/^ ^ ^ 
	echo^ ^ _____^ ___^ ^ _^ ^ ___^ ^ ^ __
	echo^ ^|_^ ^ ^ _^/^ _^ ^\^|^ ^\^|^ ^\^ ^\^ ^/^ ^/
	echo^ ^ ^ ^|^ ^|^|^ ^(_^)^ ^|^ ^.^`^ ^|^\^ V^ ^/^ 
	echo^ ^ ^ ^|_^|^ ^\___^/^|_^|^\_^|^ ^|_^|^ ^ 

pause
