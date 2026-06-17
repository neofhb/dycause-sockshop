param(
    [string]$Namespace = "sock-shop",
    [string]$IstioctlExe = "istioctl",
    [string]$Profile = "minimal",
    [string[]]$NoSidecarDeployments = @(
        "carts-db",
        "catalogue-db",
        "orders-db",
        "queue-master",
        "rabbitmq",
        "session-db",
        "user-db"
    ),
    [switch]$SkipInstall,
    [switch]$SkipRestart
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-CommandPath {
    param(
        [string]$Command,
        [string]$FriendlyName
    )

    if (Test-Path -LiteralPath $Command) {
        return $Command
    }

    $fromPath = Get-Command $Command -ErrorAction SilentlyContinue
    if ($null -ne $fromPath) {
        return $fromPath.Source
    }

    throw "Cannot find $FriendlyName. Install it or pass the executable path."
}

function Invoke-Checked {
    param(
        [string]$Command,
        [string[]]$Arguments
    )

    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed: $Command $($Arguments -join ' ') (exit code $LASTEXITCODE)"
    }
}

$kubectl = Resolve-CommandPath -Command "kubectl" -FriendlyName "kubectl"
$istioctl = Resolve-CommandPath -Command $IstioctlExe -FriendlyName "istioctl"

Write-Host "Checking Kubernetes context..."
Invoke-Checked -Command $kubectl -Arguments @("get", "namespace", $Namespace)

if (-not $SkipInstall) {
    Write-Host "Installing Istio '$Profile' profile with Prometheus metrics merging enabled..."
    Invoke-Checked -Command $istioctl -Arguments @(
        "install",
        "--set", "profile=$Profile",
        "--set", "meshConfig.enablePrometheusMerge=true",
        "-y"
    )
}
else {
    Write-Host "Skipping Istio install."
}

Write-Host "Enabling automatic sidecar injection for namespace '$Namespace'..."
Invoke-Checked -Command $kubectl -Arguments @(
    "label", "namespace", $Namespace, "istio-injection=enabled", "--overwrite"
)

if ($NoSidecarDeployments.Count -gt 0) {
    Write-Host "Disabling sidecar injection for non-HTTP/non-experiment deployments..."
    $patchFile = New-TemporaryFile
    Set-Content -LiteralPath $patchFile -Value '{"spec":{"template":{"metadata":{"annotations":{"sidecar.istio.io/inject":"false"}}}}}' -NoNewline -Encoding UTF8
    foreach ($deployment in $NoSidecarDeployments) {
        try {
            Invoke-Checked -Command $kubectl -Arguments @(
                "patch",
                "deployment",
                $deployment,
                "-n",
                $Namespace,
                "--type=merge",
                "--patch-file",
                $patchFile
            )
        }
        finally {
            if ($deployment -eq $NoSidecarDeployments[-1]) {
                Remove-Item -LiteralPath $patchFile -Force -ErrorAction SilentlyContinue
            }
        }
    }
}

if (-not $SkipRestart) {
    Write-Host "Restarting SockShop deployments so new pods receive istio-proxy sidecars..."
    Invoke-Checked -Command $kubectl -Arguments @("rollout", "restart", "deployment", "-n", $Namespace)
    $deployments = & $kubectl get deployment -n $Namespace -o name
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to list deployments in namespace '$Namespace'."
    }
    foreach ($deployment in $deployments) {
        if ([string]::IsNullOrWhiteSpace($deployment)) {
            continue
        }
        Invoke-Checked -Command $kubectl -Arguments @("rollout", "status", $deployment, "-n", $Namespace, "--timeout=600s")
    }
}
else {
    Write-Host "Skipping rollout restart. Existing pods will not be injected until recreated."
}

Write-Host ""
Write-Host "Istio system pods:"
Invoke-Checked -Command $kubectl -Arguments @("get", "pods", "-n", "istio-system")

Write-Host ""
Write-Host "SockShop pods. Application pods should usually show 2/2 READY after injection:"
Invoke-Checked -Command $kubectl -Arguments @("get", "pods", "-n", $Namespace)

Write-Host ""
Write-Host "Checking whether Prometheus can see Istio request metrics..."
$query = [System.Uri]::EscapeDataString("count(istio_requests_total)")
$url = "http://localhost:9090/api/v1/query?query=$query"
& $kubectl exec -n monitoring deploy/prometheus-deployment -- wget -qO- $url
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Prometheus query failed. Verify monitoring is deployed and scraping pod annotations."
}

Write-Host ""
Write-Host "Istio enablement completed."
