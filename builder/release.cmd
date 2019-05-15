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
Rem call ebook-convert "target\%filename%.epub" "target\%filename%.mobi"
call python.exe builder\docxconverter.py %filename%
call python.exe builder\odtconverter.py "%filename%"
REm call python.exe venv\Scripts\unoconv -f pdf "target/%filename%.odt"
IF NOT '%ERRORLEVEL%' == '0' (
    pause
)
Rem del "target\%filename%.odt"

call deactivate
