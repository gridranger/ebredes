set filename=%~1

IF NOT EXIST venv (
    call python.exe -m venv venv
    call venv\Scripts\activate
    call pip install -r builder\requirements.txt
) ELSE (
    call venv\Scripts\activate
)

IF NOT EXIST target (
    call mkdir target
)

call python.exe builder\epubconverter.py "%filename%"
call ebook-convert "target\%filename%.epub" "target\%filename%.mobi"
call python.exe builder\odtconverter.py "%filename%"
call python.exe venv\Scripts\unoconv -f pdf "target/%filename%.odt"
IF NOT '%ERRORLEVEL%' == '0' (
    pause
)
del "target\%filename%.odt"

call deactivate
