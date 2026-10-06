@echo off
setlocal
chcp 65001 >nul

set "SYNC_SCRIPT=%~dp0src\ml_project\mlp_experiment_state.py"
set "PYTHON_EXE="
if defined CONDA_PREFIX if exist "%CONDA_PREFIX%\python.exe" set "PYTHON_EXE=%CONDA_PREFIX%\python.exe"
if not defined PYTHON_EXE if exist "C:\ML_Progs\Runtimes\Miniforge3\envs\titanik-ml\python.exe" set "PYTHON_EXE=C:\ML_Progs\Runtimes\Miniforge3\envs\titanik-ml\python.exe"
if not defined PYTHON_EXE for %%I in (python.exe) do set "PYTHON_EXE=%%~$PATH:I"
if not defined PYTHON_EXE (
    echo Python was not found. Activate titanik-ml first.
    exit /b 1
)

set "PYTHONUTF8=1"
rem Sync is a lightweight Markdown/CSV operation. Imported scientific libraries
rem must not allocate one large BLAS workspace per logical CPU.
set "OPENBLAS_NUM_THREADS=1"
set "OMP_NUM_THREADS=1"
set "OMP_THREAD_LIMIT=1"
set "MKL_NUM_THREADS=1"
set "NUMEXPR_NUM_THREADS=1"
set "BLIS_NUM_THREADS=1"
"%PYTHON_EXE%" "%SYNC_SCRIPT%" --project-root "%~dp0."
set "EXIT_CODE=%ERRORLEVEL%"
endlocal & exit /b %EXIT_CODE%
