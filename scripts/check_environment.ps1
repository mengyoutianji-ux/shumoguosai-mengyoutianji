param(
    [string]$ConfigPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "config\workflow.yml"),
    [string]$LocalConfigPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "config\workflow.local.yml")
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

try {
    $Resolver = Join-Path $PSScriptRoot "get_workflow_python.ps1"
    $WorkflowPython = & $Resolver -ConfigPath $ConfigPath -LocalConfigPath $LocalConfigPath
}
catch {
    Write-Error $_.Exception.Message
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
