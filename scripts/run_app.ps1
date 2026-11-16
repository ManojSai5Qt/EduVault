$ErrorActionPreference = "Stop"

# Run from the repository root, regardless of the caller's current folder.
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python was not found on PATH. Install Python and enable the Python PATH option."
}

python -m streamlit run app.py
