param(
    [string]$ConfigPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "config\workflow.yml"),
    [string]$LocalConfigPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "config\workflow.local.yml")
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

function Get-PreferredExecutable {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return $null
    }

    $match = Select-String -LiteralPath $Path -Pattern '^\s*preferred_executable:\s*(.+?)\s*$' | Select-Object -First 1
    if (-not $match) {
        return $null
    }

    $value = $match.Matches[0].Groups[1].Value.Trim()
    if (
        $value.Length -ge 2 -and
        (($value.StartsWith('"') -and $value.EndsWith('"')) -or
        ($value.StartsWith("'") -and $value.EndsWith("'")))
    ) {
        $value = $value.Substring(1, $value.Length - 2)
    }
    return $value
}

try {
    if (-not (Test-Path -LiteralPath $ConfigPath -PathType Leaf)) {
        throw "Workflow config not found: $ConfigPath"
    }

    $workflowPython = Get-PreferredExecutable -Path $LocalConfigPath
    if (-not $workflowPython) {
        $workflowPython = Get-PreferredExecutable -Path $ConfigPath
    }
    if (-not $workflowPython -or $workflowPython -match '^<[^>]+>$') {
        throw "Python is not configured. Copy config\workflow.local.example.yml to config\workflow.local.yml and set python.preferred_executable to an absolute path."
    }
    if (-not [System.IO.Path]::IsPathRooted($workflowPython)) {
        throw "Configured Python path must be absolute: $workflowPython"
    }
    if (-not (Test-Path -LiteralPath $workflowPython -PathType Leaf)) {
        throw "Preferred Python does not exist: $workflowPython. No network installation was attempted."
    }

    (Resolve-Path -LiteralPath $workflowPython).Path
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}
