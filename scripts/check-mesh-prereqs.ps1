param(
    [string]$PythonExe = "python",
    [string]$IstioctlExe = "istioctl",
    [string]$Namespace = "sock-shop"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

function Test-Command {
    param([string]$Name)

    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($null -eq $cmd) {
        Write-Host "[FAIL] $Name not found in PATH" -ForegroundColor Red
        return $false
    }
    Write-Host "[ OK ] $Name -> $($cmd.Source)" -ForegroundColor Green
    return $true
}

function Test-CommandPath {
    param(
        [string]$Command,
        [string]$Name
    )

    if (Test-Path -LiteralPath $Command) {
        Write-Host "[ OK ] $Name -> $Command" -ForegroundColor Green
        return $true
    }
    return Test-Command $Command
}

function Invoke-Check {
    param(
        [string]$Name,
        [scriptblock]$Script
    )

    try {
        & $Script | Out-Host
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[FAIL] $Name failed (exit code $LASTEXITCODE)" -ForegroundColor Red
            return $false
        }
        Write-Host "[ OK ] $Name" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "[FAIL] $Name`: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

$allOk = $true

$allOk = (Test-Command "docker") -and $allOk
$allOk = (Test-Command "kubectl") -and $allOk
$allOk = (Test-Command "minikube") -and $allOk
$allOk = (Test-CommandPath -Command $IstioctlExe -Name "istioctl") -and $allOk

if (Test-Path -LiteralPath $PythonExe) {
    Write-Host "[ OK ] python -> $PythonExe" -ForegroundColor Green
}
else {
    $pyCmd = Get-Command $PythonExe -ErrorAction SilentlyContinue
    if ($null -eq $pyCmd) {
        Write-Host "[FAIL] Python executable not found: $PythonExe" -ForegroundColor Red
        $allOk = $false
    }
    else {
        Write-Host "[ OK ] python -> $($pyCmd.Source)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Docker daemon:"
$allOk = (Invoke-Check "docker version" { docker version }) -and $allOk

Write-Host ""
Write-Host "Kubernetes context:"
$allOk = (Invoke-Check "kubectl current-context" { kubectl config current-context }) -and $allOk
$allOk = (Invoke-Check "kubectl cluster-info" { kubectl cluster-info }) -and $allOk

Write-Host ""
Write-Host "SockShop namespace:"
$allOk = (Invoke-Check "namespace $Namespace" { kubectl get namespace $Namespace }) -and $allOk

Write-Host ""
Write-Host "Python packages:"
$allOk = (Invoke-Check "Python package imports" {
    & $PythonExe -c "import pandas, numpy, openpyxl; print('pandas/numpy/openpyxl OK')"
}) -and $allOk

Write-Host ""
if ($allOk) {
    Write-Host "All mesh prerequisites look ready." -ForegroundColor Green
    exit 0
}

Write-Host "One or more prerequisites are missing. Start Docker Desktop, restore kubectl context, install istioctl, then rerun this check." -ForegroundColor Yellow
exit 1
