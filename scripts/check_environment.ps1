param(
    [string]$ConfigPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "config\workflow.yml")
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

if (-not (Test-Path -LiteralPath $ConfigPath -PathType Leaf)) {
    Write-Error "Workflow config not found: $ConfigPath"
    exit 1
}

$ConfigMatch = Select-String -LiteralPath $ConfigPath -Pattern '^\s*preferred_executable:\s*(.+?)\s*$' | Select-Object -First 1
if (-not $ConfigMatch) {
    Write-Error "Workflow config does not define preferred_executable."
    exit 1
}

$WorkflowPython = $ConfigMatch.Matches[0].Groups[1].Value
if (-not (Test-Path -LiteralPath $WorkflowPython -PathType Leaf)) {
    Write-Error "Preferred Python does not exist: $WorkflowPython. Update config/workflow.yml explicitly. No network installation was attempted."
    exit 1
}

$PythonVersion = & $WorkflowPython --version 2>&1
$GitCommand = Get-Command git.exe -ErrorAction SilentlyContinue
if (-not $GitCommand) {
    Write-Error "git.exe was not found."
    exit 1
}

$GitVersion = & $GitCommand.Source --version
Write-Host "Python: $PythonVersion"
Write-Host "Path: $WorkflowPython"
Write-Host "Git: $GitVersion"
Write-Host "Environment check passed."
