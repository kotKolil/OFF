@echo off

setlocal enabledelayedexpansion

rem Loop through all files in the current directory
for %%f in (*) do (
    rem Check if the file extension is not .bat, .sh, or .py
    if /i not "%%~xf"==".bat" (
        if /i not "%%~xf"==".sh" (
            if /i not "%%~xf"==".py" (
                del "%%f"
            )
        )
    )
)

endlocal

@echo on

pytest -vv

@echo off

setlocal enabledelayedexpansion

rem Loop through all files in the current directory
for %%f in (*) do (
    rem Check if the file extension is not .bat, .sh, or .py
    if /i not "%%~xf"==".bat" (
        if /i not "%%~xf"==".sh" (
            if /i not "%%~xf"==".py" (
                del "%%f"
            )
        )
    )
)

endlocal