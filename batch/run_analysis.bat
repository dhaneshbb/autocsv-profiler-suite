@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM ================== HARD-CODED PATHS ==================
set "project_root="
set "scripts_dir=%project_root%\src"
set "env_base="
set "env_profiling="
set "env_dataprep="

REM ================== PYTHON SCRIPTS ==================
set "scripts[1]=auto_csv_profiler.py"
set "scripts[2]=profile_ydata_profiling_report.py"
set "scripts[3]=profile_sweetviz_report.py"
set "scripts[4]=profile_dataprep_report.py"
set "scripts[5]=cerberus_validator_specific_columns.py"

set "envs[1]=%env_base%"
set "envs[2]=%env_profiling%"
set "envs[3]=%env_profiling%"
set "envs[4]=%env_dataprep%"
set "envs[5]=%env_base%"

REM ================== PROMPT USER INPUT ==================
set /p csvpath="Enter the full path to the CSV file: "

REM Remove quotes from CSV path if they exist
set "csvpath=%csvpath:"=%"

REM Extract filename and folder information
for %%F in ("%csvpath%") do set "filename_no_ext=%%~nF"
for %%F in ("%csvpath%") do set "filename=%%~nxF"
for %%F in ("%csvpath%") do set "csv_folder=%%~dpF"

REM Define the output directory inside the same directory as the CSV file with the filename (without extension)
set "final_output_dir=%csv_folder%\%filename_no_ext%"
if not exist "%final_output_dir%" mkdir "%final_output_dir%"

REM Copy the CSV file to the output directory
copy "%csvpath%" "%final_output_dir%\%filename%"

REM ================== DELIMITER DETECTION ==================
set /p activate_env="Activate environment for delimiter detection? (y/n): "
if /i "%activate_env%"=="y" (
    echo Activating environment for delimiter detection...
    call "%env_base%"
    IF ERRORLEVEL 1 (
        echo Failed to activate delimiter environment.
        pause
        exit /b 1
    )
    echo Running delimiter recognition script...
    python "%scripts_dir%\recognize_delimiter.py" "%final_output_dir%\%filename%"
    IF ERRORLEVEL 1 (
        echo Error occurred while running delimiter recognition.
        pause
        exit /b 1
    )
)

REM Ask user to confirm delimiter
set /p delimiter="Enter the delimiter used in the CSV file (e.g., , or ;): "

REM Strip any accidental double quotes from delimiter input
set "delimiter=%delimiter:"=%"

REM ================== SHOW STRUCTURED TABLE ==================
echo.
echo +-------+------------------------+--------------------------------------+
echo ^| Index ^| Environment            ^| Python Script                        ^|
echo +-------+------------------------+--------------------------------------+
echo ^|   1   ^| ds_ml                  ^| auto_csv_profiler.py                 ^|
echo ^|   2   ^| sweetz_ydata_profiler  ^| profile_ydata_profiling_report.py    ^|
echo ^|   3   ^| sweetz_ydata_profiler  ^| profile_sweetviz_report.py           ^|
echo ^|   4   ^| dataprep               ^| profile_dataprep_report.py           ^|
echo ^|   5   ^| ds_ml                  ^| cerberus_validator_specific_columns.py^|
echo +-------+------------------------+--------------------------------------+
echo.

REM ================== EXECUTE SCRIPTS ==================

REM Loop through scripts and execute each one in its own environment
for /L %%i in (1,1,5) do (
    set "script=!scripts[%%i]!"
    set "env=!envs[%%i]!"

    set /p run_script="Run !script! ? (y/n): "
    if /i "!run_script!"=="y" (
        echo Activating environment for !script!...
        call "!env!"
        IF ERRORLEVEL 1 (
            echo Failed to activate environment for !script!.
            pause
            exit /b 1
        )
        echo Running !script!...
        
        REM Pass CSV + Output Directory for auto_csv_profiler.py
        if "%%i"=="1" (
            python "%scripts_dir%\!script!" "%final_output_dir%\%filename%" "%final_output_dir%"
        ) else (
            python "%scripts_dir%\!script!" "%final_output_dir%\%filename%" "!delimiter!"
        )

        echo Finished processing !script!.
    )
)

REM Prevent automatic closure
echo All processes completed successfully. Reports saved in: %final_output_dir%
pause

ENDLOCAL
