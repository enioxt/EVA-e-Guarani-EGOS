# EVA & GUARANI SLOP Server Starter
# ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧

function Write-Rainbow {
    param([string]$Text)
    $colors = @("Blue", "Magenta", "Red", "Yellow", "Green", "Cyan")
    $colorIndex = 0
    foreach ($char in $Text.ToCharArray()) {
        Write-Host $char -NoNewline -ForegroundColor $colors[$colorIndex]
        $colorIndex = ($colorIndex + 1) % $colors.Length
    }
    Write-Host ""
}

function Show-Banner {
    Write-Host "`n"
    Write-Rainbow "✧༺❀༻∞ EVA & GUARANI SLOP Server ∞༺❀༻✧"
    Write-Host "`n"
    Write-Host "Environment Information:" -ForegroundColor Cyan
    Write-Host "• OS: Windows 11" -ForegroundColor Yellow
    Write-Host "• Shell: PowerShell" -ForegroundColor Yellow
    Write-Host "• IDE: Cursor" -ForegroundColor Yellow
    Write-Host "• Testing Tool: Postman" -ForegroundColor Yellow
    Write-Host "`nServer Configuration:" -ForegroundColor Cyan
    Write-Host "• Host: localhost" -ForegroundColor Green
    Write-Host "• Port: 3000" -ForegroundColor Green
    Write-Host "• Logs: C:\Eva Guarani EGOS\logs" -ForegroundColor Green
    Write-Host "`nAvailable Endpoints:" -ForegroundColor Cyan
    Write-Host "• POST /mycelium/connect - Mycelium Network Connection" -ForegroundColor Magenta
    Write-Host "• POST /atlas/visualize   - ATLAS Visualization" -ForegroundColor Magenta
    Write-Host "• POST /cronos/timeline   - CRONOS Timeline" -ForegroundColor Magenta
    Write-Host "• POST /nexus/analyze     - NEXUS Analysis" -ForegroundColor Magenta
    Write-Host "• POST /ethik/validate    - ETHIK Validation" -ForegroundColor Magenta
    Write-Host "`n"
}

# Create logs directory if it doesn't exist
$logsPath = "C:\Eva Guarani EGOS\logs"
if (-not (Test-Path $logsPath)) {
    New-Item -ItemType Directory -Path $logsPath -Force | Out-Null
    Write-Host "Created logs directory at $logsPath" -ForegroundColor Green
}

# Show the beautiful banner
Show-Banner

# Navigate to the correct directory
Set-Location "C:\Eva Guarani EGOS\QUANTUM_PROMPTS"

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
}

# Register key files in the Mycelium Network
function Register-MyceliumFiles {
    Write-Host "Registrando arquivos na Rede Micelial..." -ForegroundColor Cyan

    # Define a função para registrar arquivos
    function Register-File {
        param (
            [string]$fileId,
            [string]$filePath,
            [string]$fileType,
            [string[]]$connections
        )

        $body = @{
            fileId = $fileId
            filePath = $filePath
            fileType = $fileType
            connections = $connections
        } | ConvertTo-Json

        try {
            $response = Invoke-RestMethod -Uri "http://localhost:3000/mycelium/register-file" -Method POST -Body $body -ContentType "application/json"
            Write-Host "  ✓ Arquivo registrado: $fileId" -ForegroundColor Green
        }
        catch {
            Write-Host "  ✗ Erro ao registrar arquivo $fileId" -ForegroundColor Red
            Write-Host $_.Exception.Message -ForegroundColor Red
        }
    }

    # Registrar os principais arquivos
    $baseDir = "C:\Eva Guarani EGOS"
    $quantumPromptsDir = Join-Path -Path $baseDir -ChildPath "QUANTUM_PROMPTS"

    # Roadmap principal
    $roadmapPath = Join-Path -Path $quantumPromptsDir -ChildPath "MASTER\quantum_roadmap.md"

    # README principal
    $readmePath = Join-Path -Path $quantumPromptsDir -ChildPath "README.md"

    # Registrar Roadmap
    Register-File -fileId "roadmap-main" -filePath $roadmapPath -fileType "roadmap" -connections @("readme-main")

    # Registrar README
    Register-File -fileId "readme-main" -filePath $readmePath -fileType "readme" -connections @("roadmap-main")

    Write-Host "Rede Micelial inicializada com os arquivos principais." -ForegroundColor Cyan
}

# Start the server
Write-Host "Starting SLOP server with love and consciousness..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server`n" -ForegroundColor Yellow

# Start the server with enhanced logging
$env:DEBUG = "slop:*"
$serverProcess = Start-Process -FilePath "node" -ArgumentList "slop_server.js" -NoNewWindow -PassThru

# Wait a moment for the server to start
Start-Sleep -Seconds 3

# Register files in the Mycelium Network if the server started successfully
if ($serverProcess.HasExited -eq $false) {
    Register-MyceliumFiles

    # Keep the script running while the server is alive
    while ($serverProcess.HasExited -eq $false) {
        Start-Sleep -Seconds 1
    }
}
else {
    Write-Host "Server failed to start. Exit code: $($serverProcess.ExitCode)" -ForegroundColor Red
}
