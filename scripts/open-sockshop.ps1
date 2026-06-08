param(
    [string]$MinikubeExe = "C:\Program Files\Kubernetes\Minikube\minikube.exe",
    [string]$Namespace = "sock-shop",
    [string]$ServiceName = "front-end"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-MinikubeCommand {
    param([string]$PreferredPath)

    if (Test-Path -LiteralPath $PreferredPath) {
        return $PreferredPath
    }

    $fromPath = Get-Command minikube -ErrorAction SilentlyContinue
    if ($null -ne $fromPath) {
        return $fromPath.Source
    }

    throw "Cannot find minikube. Install it or pass -MinikubeExe <path>."
}

function Invoke-Minikube {
    param(
        [string]$MinikubeCmd,
        [string[]]$Arguments
    )

    & $MinikubeCmd @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed: minikube $($Arguments -join ' ') (exit code $LASTEXITCODE)"
    }
}

function Invoke-KubectlViaMinikube {
    param(
        [string]$MinikubeCmd,
        [string[]]$KubectlArguments
    )

    $arguments = @("kubectl", "--") + $KubectlArguments
    & $MinikubeCmd @arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed: minikube kubectl -- $($KubectlArguments -join ' ') (exit code $LASTEXITCODE)"
    }
}

function Get-FirstUrl {
    param([string]$Text)

    if ([string]::IsNullOrWhiteSpace($Text)) {
        return $null
    }

    $match = [regex]::Match($Text, 'https?://[^\s]+')
    if ($match.Success) {
        return $match.Value
    }

    return $null
}

$minikube = Resolve-MinikubeCommand -PreferredPath $MinikubeExe

Write-Host "Checking minikube status..."
& $minikube status | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Minikube is not running, starting it now..."
    Invoke-Minikube -MinikubeCmd $minikube -Arguments @("start")
}

Invoke-Minikube -MinikubeCmd $minikube -Arguments @("update-context")
Invoke-KubectlViaMinikube -MinikubeCmd $minikube -KubectlArguments @("get", "svc", $ServiceName, "-n", $Namespace, "-o", "name") | Out-Null

$stdoutFile = [System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), "sockshop-service-url-$PID.out.log")
$stderrFile = [System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), "sockshop-service-url-$PID.err.log")

Write-Host "Starting local access tunnel for $ServiceName..."
$serviceProc = Start-Process -FilePath $minikube -ArgumentList @("service", $ServiceName, "-n", $Namespace, "--url") -NoNewWindow -PassThru -RedirectStandardOutput $stdoutFile -RedirectStandardError $stderrFile

$url = $null
$deadline = (Get-Date).AddSeconds(60)
while ((Get-Date) -lt $deadline -and $null -eq $url -and -not $serviceProc.HasExited) {
    Start-Sleep -Milliseconds 400
    if (Test-Path -LiteralPath $stdoutFile) {
        $url = Get-FirstUrl -Text (Get-Content -LiteralPath $stdoutFile -Raw -ErrorAction SilentlyContinue)
    }
    if ($null -eq $url -and (Test-Path -LiteralPath $stderrFile)) {
        $url = Get-FirstUrl -Text (Get-Content -LiteralPath $stderrFile -Raw -ErrorAction SilentlyContinue)
    }
}

if ($null -eq $url) {
    if (-not $serviceProc.HasExited) {
        Stop-Process -Id $serviceProc.Id -Force
    }
    $errText = ""
    if (Test-Path -LiteralPath $stderrFile) {
        $errText = Get-Content -LiteralPath $stderrFile -Raw -ErrorAction SilentlyContinue
    }
    if ([string]::IsNullOrWhiteSpace($errText)) {
        $errText = "No detail output."
    }
    throw "Failed to get front-end URL from minikube service. Detail: $errText"
}

Write-Host ""
Write-Host "Front-end URL: $url"
Start-Process $url | Out-Null
Write-Host "Browser opened. Keep this window open while using Sock Shop."
Write-Host "Press Enter to close the local access tunnel..."
[void](Read-Host)

if (-not $serviceProc.HasExited) {
    Stop-Process -Id $serviceProc.Id -Force
}

if (Test-Path -LiteralPath $stdoutFile) {
    Remove-Item -LiteralPath $stdoutFile -Force -ErrorAction SilentlyContinue
}
if (Test-Path -LiteralPath $stderrFile) {
    Remove-Item -LiteralPath $stderrFile -Force -ErrorAction SilentlyContinue
}

Write-Host "Access tunnel closed."
