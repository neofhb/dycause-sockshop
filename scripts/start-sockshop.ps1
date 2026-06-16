param(
    [string]$MinikubeExe = "C:\Program Files\Kubernetes\Minikube\minikube.exe",
    [string]$Namespace = "sock-shop",
    [string]$Driver = "docker",
    [int]$Cpus = 4,
    [int]$Memory = 7168,
    [switch]$ShowServiceUrl
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

Write-Host "Starting minikube..."
Invoke-Minikube -MinikubeCmd $minikube -Arguments @(
    "start",
    "--driver=$Driver",
    "--cpus=$Cpus",
    "--memory=$Memory"
)

Write-Host "Updating kubectl context..."
Invoke-Minikube -MinikubeCmd $minikube -Arguments @("update-context")

try {
    Invoke-KubectlViaMinikube -MinikubeCmd $minikube -KubectlArguments @("get", "namespace", $Namespace, "-o", "name") | Out-Null
}
catch {
    throw "Namespace '$Namespace' does not exist. Deploy Sock Shop first, then rerun this script."
}

Write-Host "Scaling deployments in namespace '$Namespace' to 1..."
Invoke-KubectlViaMinikube -MinikubeCmd $minikube -KubectlArguments @("scale", "deploy", "--all", "--replicas=1", "-n", $Namespace)

Write-Host "Waiting for deployments to become available (timeout 5 minutes)..."
try {
    Invoke-KubectlViaMinikube -MinikubeCmd $minikube -KubectlArguments @("wait", "--for=condition=Available", "--timeout=300s", "deploy", "--all", "-n", $Namespace)
}
catch {
    Write-Warning "Some deployments are still not Available. Showing current status."
}

Write-Host ""
Write-Host "Deployment status:"
Invoke-KubectlViaMinikube -MinikubeCmd $minikube -KubectlArguments @("get", "deploy", "-n", $Namespace)

Write-Host ""
Write-Host "Pod status:"
Invoke-KubectlViaMinikube -MinikubeCmd $minikube -KubectlArguments @("get", "pods", "-n", $Namespace)

Write-Host ""
if ($ShowServiceUrl) {
    Write-Host "Front-end URL (keep this terminal open on Windows Docker driver):"
    Invoke-Minikube -MinikubeCmd $minikube -Arguments @("service", "front-end", "-n", $Namespace, "--url")
}
else {
    Write-Host "To get front-end URL run:"
    Write-Host "`"$minikube`" service front-end -n $Namespace --url"
}

Write-Host ""
Write-Host "Sock Shop startup script completed."
