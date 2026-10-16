param(
    [string]$Url = "http://localhost:8000/api/health",
    [int]$Requests = 1000,
    [int]$Concurrency = 10
)

# Ensure System.Net.Http assembly is loaded
try {
    Add-Type -AssemblyName System.Net.Http -ErrorAction Stop
} catch {
    # already loaded or in modern .NET
}

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " StudyTrack Load Test (PowerShell)" -ForegroundColor Cyan
Write-Host " Target URL   : $Url" -ForegroundColor White
Write-Host " Total Reqs   : $Requests" -ForegroundColor White
Write-Host " Concurrency  : $Concurrency" -ForegroundColor White
Write-Host "==================================================" -ForegroundColor Cyan

$client = New-Object System.Net.Http.HttpClient

$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
$completed = 0
$errors = 0

$batchSize = $Concurrency
while ($completed -lt $Requests) {
    $remaining = $Requests - $completed
    $currentBatch = [Math]::Min($batchSize, $remaining)

    $tasks = @(1..$currentBatch | ForEach-Object {
        $client.GetAsync($Url)
    })

    try {
        [System.Threading.Tasks.Task]::WaitAll($tasks)
        foreach ($t in $tasks) {
            if ($t.Status -ne [System.Threading.Tasks.TaskStatus]::RanToCompletion) {
                $errors++
            }
        }
    } catch {
        $errors++
    }

    $completed += $currentBatch
    if (($completed % 100 -eq 0) -or ($completed -eq $Requests)) {
        Write-Host "Progress: $completed / $Requests requests completed..." -ForegroundColor Gray
    }
}

$client.Dispose()
$stopwatch.Stop()
$elapsedSec = [Math]::Max(0.01, $stopwatch.Elapsed.TotalSeconds)
$rps = [Math]::Round($Requests / $elapsedSec, 1)

Write-Host "==================================================" -ForegroundColor Green
Write-Host " Load test completed in $($stopwatch.Elapsed.TotalSeconds.ToString('F2'))s (~$rps req/sec)" -ForegroundColor Green
if ($errors -gt 0) {
    Write-Host " Errors encountered: $errors" -ForegroundColor Yellow
}
Write-Host " Check Prometheus / Grafana / HPA for metrics!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
