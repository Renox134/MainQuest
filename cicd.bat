@ECHO OFF

REM Check if the "c" flag is set
set "clearFlag="
set "testFlag="

REM Loop through the command line arguments
for %%a in (%*) do (
    if /I "%%a"=="c" set "clearFlag=1"
    if /I "%%a"=="t" set "testFlag=1"
)

REM If the "c" flag is set, clear the terminal
if defined clearFlag (
    cls
)

ECHO Starting the CI/CD-Process. Reminder: We should use Gitlab for that.\n\n
ECHO:
ECHO:
ECHO =========== Starting flake8 ===========
ECHO:
flake8 .
ECHO:
ECHO ============ Ending flake8 ============

ECHO ============ Starting mypy ============
ECHO:
mypy .\src
ECHO:
ECHO ============= Ending mypy =============

if defined testFlag (
    ECHO =========== Starting pytest ===========
    ECHO:
    where /q py
    IF ERRORLEVEL 1 (
        python -m pytest test
    ) ELSE (
        py -m pytest test
    )
    ECHO:
    ECHO ============ Ending pytest ============
)

