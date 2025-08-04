@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM ================== CONDA ENVIRONMENT SETUP ==================
REM Initialize conda for batch script
call conda info >nul 2>&1
if ERRORLEVEL 1 (
    echo Error: Conda is not available or not properly initialized.
    echo Please ensure Anaconda/Miniconda is installed and added to PATH.
    pause
    exit /b 1
)

REM ================== HARD-CODED PATHS ==================
set "project_root=%~dp0"
set "scripts_dir=%project_root%src"

REM ================== CONDA ENVIRONMENTS ==================
set "env_main=csv-profiler-main"
set "env_profiling=csv-profiler-profiling"
set "env_dataprep=csv-profiler-dataprep"

REM ================== PYTHON SCRIPTS ==================
set "scripts[1]=auto_csv_profiler.py"
set "scripts[2]=profile_ydata_profiling_report.py"
set "scripts[3]=profile_sweetviz_report.py"
set "scripts[4]=profile_dataprep_report.py"

set "envs[1]=%env_main%"
set "envs[2]=%env_profiling%"
set "envs[3]=%env_profiling%"
set "envs[4]=%env_dataprep%"

REM ================== VERIFY ENVIRONMENTS EXIST ==================
echo Checking conda environments...
for %%e in (%env_main% %env_profiling% %env_dataprep%) do (
    conda env list | findstr /C:"%%e" >nul
    if ERRORLEVEL 1 (
        echo Error: Conda environment '%%e' not found.
        echo Please run setup_environments.ps1 first to create the required environments.
        pause
        exit /b 1
    ) else (
        echo [OK] Found environment: %%e
    )
)

cls

REM ================== PROMPT USER INPUT ==================
set /p csvpath="Enter the full path to the CSV file: "

REM Remove quotes from CSV path if they exist
set "csvpath=%csvpath:"=%"

REM Validate CSV file exists
if not exist "%csvpath%" (
    echo Error: CSV file not found at "%csvpath%"
    pause
    exit /b 1
)

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
    echo Activating environment %env_main% for delimiter detection...
    call conda activate %env_main%
    IF ERRORLEVEL 1 (
        echo Failed to activate conda environment %env_main%.
        pause
        exit /b 1
    )
    echo Running delimiter recognition script...
    python "%scripts_dir%\recognize_delimiter.py" "%final_output_dir%\%filename%"
    IF ERRORLEVEL 1 (
        echo Error occurred while running delimiter recognition.
        call conda deactivate
        pause
        exit /b 1
    )
    call conda deactivate
    
REM Ask user to confirm delimiter
set /p delimiter="Enter the delimiter used in the CSV file (e.g., , or ;): "

REM Strip any accidental double quotes from delimiter input
set "delimiter=%delimiter:"=%"

REM ================== SHOW STRUCTURED TABLE ==================
echo.
echo +-------+------------------------+--------------------------------------+
echo ^| Index ^| Environment            ^| Python Script                        ^|
echo +-------+------------------------+--------------------------------------+
echo ^|   1   ^| csv-profiler-main      ^| auto_csv_profiler.py                 ^|
echo ^|   2   ^| csv-profiler-profiling ^| profile_ydata_profiling_report.py    ^|
echo ^|   3   ^| csv-profiler-profiling ^| profile_sweetviz_report.py           ^|
echo ^|   4   ^| csv-profiler-dataprep  ^| profile_dataprep_report.py           ^|
echo +-------+------------------------+--------------------------------------+
echo.

REM ================== EXECUTE SCRIPTS ==================

REM Loop through scripts and execute each one in its own conda environment
for /L %%i in (1,1,4) do (
    set "script=!scripts[%%i]!"
    set "env=!envs[%%i]!"

    set /p run_script="Run !script! ? (y/n): "
    if /i "!run_script!"=="y" (
        echo.
        echo Activating conda environment: !env!
        call conda activate !env!
        IF ERRORLEVEL 1 (
            echo Failed to activate conda environment !env!.
            pause
            exit /b 1
        )
        
        echo Running !script! in environment !env!...
        
        REM Pass CSV + Output Directory for auto_csv_profiler.py
        if "%%i"=="1" (
            python "%scripts_dir%\!script!" "%final_output_dir%\%filename%" "%final_output_dir%"
        ) else (
            python "%scripts_dir%\!script!" "%final_output_dir%\%filename%" "!delimiter!"
        )
        
        if ERRORLEVEL 1 (
            echo Error occurred while running !script!
            call conda deactivate
            pause
            exit /b 1
        )
        
        echo [OK] Finished processing !script!
        call conda deactivate
        echo.
    )
)

REM ================== COMPLETION ==================
echo.
echo ================== ANALYSIS COMPLETE ==================
echo All processes completed successfully!
echo Reports saved in: %final_output_dir%
echo.
echo You can now open the output directory to view the generated reports.
pause

ENDLOCAL