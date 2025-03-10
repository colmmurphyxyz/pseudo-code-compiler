@echo on
setlocal enabledelayedexpansion

if "%VIRTUAL_ENV%"=="" (
    echo This script is being executed from a Python virtual environment.
)

if exist transpiled_pc_examples (
    echo transpiled_pc_examples already exists
    exit /b 1
) else (
    mkdir transpiled_pc_examples
)

for /r %%F in (pc_examples\*.pc) do (
    set "relative_path=%%F"
    set "relative_path=!relative_path:pc_examples\=!"
    set "output_dir=transpiled_pc_examples\!relative_path!"
    for %%I in (!output_dir!) do set "output_dir=%%~dpI"
    mkdir "!output_dir!" 2>nul
    for %%I in (%%F) do set "output_file=%%~nI.py"
    echo Transpiling %%F to !output_file!
    python ..\pcc\pcc.py --output-rendered-source 0 -o "!output_dir!!output_file!" "%%F"
)

echo Done
exit /b 0
