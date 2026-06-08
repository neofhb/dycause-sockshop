param(
    [string]$MinikubeExe = "C:\Program Files\Kubernetes\Minikube\minikube.exe",
    [switch]$Soft
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

$minikube = Resolve-MinikubeCommand -PreferredPath $MinikubeExe

if ($Soft) {
    Write-Host "Soft stop: scaling Sock Shop deployments to 0..."
    Invoke-KubectlViaMinikube -MinikubeCmd $minikube -KubectlArguments @("scale", "deploy", "--all", "--replicas=0", "-n", "sock-shop")
    Write-Host ""
    Write-Host "Current deployment status:"
    Invoke-KubectlViaMinikube -MinikubeCmd $minikube -KubectlArguments @("get", "deploy", "-n", "sock-shop")
    Write-Host ""
    Write-Host "Soft stop completed. Cluster is still running."
}
else {
    Write-Host "Hard stop: stopping minikube..."
    Invoke-Minikube -MinikubeCmd $minikube -Arguments @("stop")
    Write-Host ""
    Write-Host "Minikube stopped successfully."
}
