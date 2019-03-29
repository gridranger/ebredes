set filename=%1

IF NOT EXIST venv (
    call python.exe -m venv venv
    call venv\Scripts\activate
    call pip install unoconv
) ELSE (
    call venv\Scripts\activate
)

call python.exe venv\Scripts\unoconv -f pdf target\%filename%.odt
IF NOT '%ERRORLEVEL%' == '0' (
    pause
)

call deactivate
