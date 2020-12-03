@echo off 
title To launch myaccount.py

:: get the date
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "fullstamp=%YYYY%-%MM%-%DD%_%HH%-%Min%-%Sec%"

:: custimized var
set "ANACONDA_PATH=C:\Users\Acer\"
set "GITHUB_PATH=D:\GitHub\"

:: welcome msg
echo Welcome to use myaccount2p0!!
echo Today is "%fullstamp%"

:: activate anaconda3
call "%ANACONDA_PATH%anaconda3\Scripts\activate.bat"

:: exe
D:
cd %GITHUB_PATH%myaccount2p0\TRUNK\src
python myaccount.py

:: exit msg
echo Thanks for using myaccount2p0!!

pause
