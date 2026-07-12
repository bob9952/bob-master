@echo off
REM ============================================================
REM  build.bat -- MATF master thesis (pdflatex + bibtex)
REM
REM  xelatex is not installed, so we build with pdflatex, which
REM  matfmaster.sty fully supports (babel + fontenc[T1,T2A] branch).
REM  -enable-installer lets MiKTeX auto-fetch any missing packages.
REM
REM  Usage:
REM     build.bat            -> builds matfmaster-primer.tex
REM     build.bat <name>     -> builds <name>.tex  (no extension)
REM ============================================================
setlocal
cd /d "%~dp0"

set "JOB=%~1"
if "%JOB%"=="" set "JOB=matfmaster-primer"

if not exist "%JOB%.tex" (
  echo ERROR: "%JOB%.tex" not found in "%~dp0"
  exit /b 2
)

echo Building "%JOB%" with pdflatex + bibtex ...
echo(

echo [1/4] pdflatex (pass 1)
pdflatex -enable-installer -interaction=nonstopmode -halt-on-error "%JOB%.tex" > "%JOB%.build.log" 2>&1
echo       exit code = %errorlevel%

echo [2/4] bibtex
bibtex "%JOB%" >> "%JOB%.build.log" 2>&1
echo       exit code = %errorlevel%

echo [3/4] pdflatex (pass 2)
pdflatex -enable-installer -interaction=nonstopmode -halt-on-error "%JOB%.tex" >> "%JOB%.build.log" 2>&1
echo       exit code = %errorlevel%

echo [4/4] pdflatex (pass 3)
pdflatex -enable-installer -interaction=nonstopmode -halt-on-error "%JOB%.tex" >> "%JOB%.build.log" 2>&1
echo       exit code = %errorlevel%

echo(
if exist "%JOB%.pdf" (
  echo === SUCCESS: %JOB%.pdf ===
) else (
  echo === FAILED: %JOB%.pdf was not produced. See "%JOB%.log" for the LaTeX error. ===
  exit /b 1
)

endlocal
