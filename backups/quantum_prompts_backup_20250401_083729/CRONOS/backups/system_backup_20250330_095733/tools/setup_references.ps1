# EVA & GUARANI - Reference Setup Script for Windows
# This script must be run with administrator privileges
# Right-click and select "Run as Administrator"

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "Error: This script must be run as Administrator. Right-click and select 'Run as Administrator'." -ForegroundColor Red
    exit
}

# Create reference directories
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
$refsDir = Join-Path (Split-Path -Parent $projectRoot) "EVA_REFS"

Write-Host "`n--------------------------------------------------------------------------------" -ForegroundColor Cyan
Write-Host "EVA & GUARANI - Reference Setup Script" -ForegroundColor Cyan
Write-Host "Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host "--------------------------------------------------------------------------------`n" -ForegroundColor Cyan

# Create main reference directory
if (-not (Test-Path $refsDir)) {
    Write-Host "Creating reference directory: $refsDir" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $refsDir | Out-Null
}

# Create subdirectories
$docsDir = Join-Path $refsDir "docs"
$appsDir = Join-Path $refsDir "apps"
$archivesDir = Join-Path $refsDir "archives"

foreach ($dir in @($docsDir, $appsDir, $archivesDir)) {
    if (-not (Test-Path $dir)) {
        Write-Host "Creating directory: $dir" -ForegroundColor Yellow
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
}

Write-Host "✓ Reference directories created successfully" -ForegroundColor Green

# Handle large directories
$largeDirs = @(
    @{Name = "docs"; Type = "docs" },
    @{Name = "eva-atendimento"; Type = "apps" }
)

foreach ($dir in $largeDirs) {
    $sourcePath = Join-Path $projectRoot $dir.Name
    $targetParentPath = Join-Path $refsDir $dir.Type
    $targetPath = Join-Path $targetParentPath $dir.Name

    if (Test-Path $sourcePath) {
        Write-Host "`nLarge directory found: $($dir.Name)" -ForegroundColor Yellow

        $choice = Read-Host "Do you want to move $($dir.Name) to $targetParentPath and create a symlink? (y/n)"
        if ($choice -eq "y") {
            # Check if target already exists
            if (Test-Path $targetPath) {
                $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
                $targetPath = "$targetPath`_$timestamp"
            }

            # Move directory
            Write-Host "Moving $($dir.Name) to $targetPath..." -ForegroundColor Yellow
            try {
                # Create backup first (rename)
                $backupPath = "$sourcePath.backup"
                if (Test-Path $backupPath) {
                    Remove-Item -Path $backupPath -Recurse -Force
                }
                Rename-Item -Path $sourcePath -NewName "$($dir.Name).backup"

                # Move the backup to target
                if (-not (Test-Path $targetParentPath)) {
                    New-Item -ItemType Directory -Path $targetParentPath | Out-Null
                }
                Move-Item -Path "$sourcePath.backup" -Destination $targetPath

                # Create symbolic link
                Write-Host "Creating symbolic link..." -ForegroundColor Yellow
                cmd /c mklink /D $sourcePath $targetPath

                Write-Host "✓ Successfully moved $($dir.Name) and created symlink" -ForegroundColor Green
            }
            catch {
                Write-Host "Error: $_" -ForegroundColor Red
            }
        }
    }
}

Write-Host "`nSetup complete. Your large directories have been moved to the reference"
Write-Host "location and symbolic links have been created. This will significantly"
Write-Host "improve indexing performance in VSCode/Cursor."
Write-Host "`nYou can now open the workspace using the file:" -ForegroundColor Cyan
Write-Host "eva_guarani.code-workspace" -ForegroundColor White

Write-Host "`n--------------------------------------------------------------------------------" -ForegroundColor Cyan
Write-Host "`nPress any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
