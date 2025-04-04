# Start the metadata server
$ErrorActionPreference = "Stop"

try {
    # Get the script directory
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $rootDir = Split-Path -Parent (Split-Path -Parent $scriptDir)

    # Set environment variables
    $env:PYTHONPATH = $rootDir

    Write-Host "Starting metadata server..."
    Write-Host "Root directory: $rootDir"

    # Start the server
    python "$scriptDir/metadata_server.py"
}
catch {
    Write-Host "Error starting server: $_"
    exit 1
}
