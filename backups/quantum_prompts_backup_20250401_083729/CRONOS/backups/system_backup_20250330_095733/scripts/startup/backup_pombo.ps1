# EVA & GUARANI System Backup Script
# Backup name: POMBO
# Date: 2025-03-28

$date = Get-Date -Format "yyyy-MM-dd"
$backupName = "POMBO_$date"
$sourceDir = "C:\Eva Guarani EGOS"
$backupDir = "C:\Eva Guarani EGOS\Backups"
$backupFile = "$backupDir\$backupName.zip"

# Create backup directory if it doesn't exist
if (!(Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir | Out-Null
    Write-Host "Created backup directory: $backupDir"
}

# Create backup manifest
$manifestPath = "$backupDir\${backupName}_manifest.txt"
Write-Host "Creating backup manifest at $manifestPath..."
"EVA & GUARANI System Backup" | Out-File $manifestPath
"Backup Name: $backupName" | Out-File $manifestPath -Append
"Date: $date" | Out-File $manifestPath -Append
"=" * 50 | Out-File $manifestPath -Append
"System components backed up:" | Out-File $manifestPath -Append

# List of directories to backup
$dirsToBackup = @(
    "QUANTUM_PROMPTS",
    "BIOS-Q",
    "logs",
    "ATLAS",
    "CRONOS",
    "ETHIK",
    "NEXUS",
    "web_client",
    "deploy"
)

# Create temporary directory for selective backup
$tempDir = "$backupDir\temp_$backupName"
if (!(Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir | Out-Null
}

# Copy selected directories to temp
foreach ($dir in $dirsToBackup) {
    $sourcePath = Join-Path $sourceDir $dir
    if (Test-Path $sourcePath) {
        $destPath = Join-Path $tempDir $dir
        Write-Host "Copying $dir to temporary location..."
        Copy-Item -Path $sourcePath -Destination $destPath -Recurse -Force
        "- $dir" | Out-File $manifestPath -Append
    } else {
        "- $dir (not found)" | Out-File $manifestPath -Append
    }
}

# Copy key files from root
$filesToBackup = @(
    "README.md",
    "VERSION.md",
    "core_principles.md",
    "quantum_prompt.txt",
    "quantum_prompt_8.0.md",
    "slop_server.js",
    "mycelium_monitor.js",
    "slop_config.json",
    "package.json",
    "package-lock.json",
    "requirements.txt",
    "pytest.ini",
    "schedule_roadmap_update.js",
    "update_roadmap.js"
)

foreach ($file in $filesToBackup) {
    $sourcePath = Join-Path $sourceDir $file
    if (Test-Path $sourcePath) {
        $destPath = Join-Path $tempDir $file
        Write-Host "Copying $file to temporary location..."
        Copy-Item -Path $sourcePath -Destination $destPath -Force
        "- $file" | Out-File $manifestPath -Append
    } else {
        "- $file (not found)" | Out-File $manifestPath -Append
    }
}

# Specifically search for critical components mentioned in the requirements
$criticalComponents = @(
    "Ethik Core",
    "Core Principles",
    "Code of Conduct",
    "PDD",
    "AVA",
    "Ethik Blockchain",
    "Ethichain"
)

"=" * 50 | Out-File $manifestPath -Append
"Critical components status:" | Out-File $manifestPath -Append

foreach ($component in $criticalComponents) {
    # Search for files containing the component name
    $foundFiles = Get-ChildItem -Path $sourceDir -Recurse -File | 
                 Where-Object { $_.Name -like "*$component*" -or (Get-Content $_.FullName -ErrorAction SilentlyContinue | Select-String -Pattern $component -Quiet) }
    
    if ($foundFiles) {
        "- ${component} - Found in:" | Out-File $manifestPath -Append
        foreach ($file in $foundFiles) {
            "  * $($file.FullName.Replace($sourceDir, ''))" | Out-File $manifestPath -Append
            
            # If not already in backup, copy it
            $relativePath = $file.FullName.Replace($sourceDir, '').TrimStart('\')
            $destPath = Join-Path $tempDir $relativePath
            $destDir = [System.IO.Path]::GetDirectoryName($destPath)
            
            if (!(Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            
            if (!(Test-Path $destPath)) {
                Copy-Item -Path $file.FullName -Destination $destPath -Force
                Write-Host "Added critical component file: $relativePath"
            }
        }
    } else {
        "- ${component} - Not found in system" | Out-File $manifestPath -Append
    }
}

# Add manifest to temp dir
Copy-Item -Path $manifestPath -Destination $tempDir -Force

# Create zip archive
Write-Host "Creating backup archive $backupFile..."
Compress-Archive -Path "$tempDir\*" -DestinationPath $backupFile -Force

# Clean up temporary directory
Write-Host "Cleaning up temporary files..."
Remove-Item -Path $tempDir -Recurse -Force

Write-Host "Backup completed successfully!"
Write-Host "Backup location: $backupFile"
Write-Host "Manifest: $manifestPath"

# Create a system audit report
$auditReportPath = "$backupDir\${backupName}_system_audit.txt"
Write-Host "Creating system audit report at $auditReportPath..."

"EVA & GUARANI System Audit Report" | Out-File $auditReportPath
"Generated: $date" | Out-File $auditReportPath -Append
"=" * 50 | Out-File $auditReportPath -Append
"System Components Inventory:" | Out-File $auditReportPath -Append

# List all directories in the main system folders
$systemDirs = Get-ChildItem -Path $sourceDir -Directory | Select-Object -ExpandProperty Name
"Main System Directories:" | Out-File $auditReportPath -Append
foreach ($dir in $systemDirs) {
    "- $dir" | Out-File $auditReportPath -Append
}

"=" * 50 | Out-File $auditReportPath -Append
"Integration Status of Key Components:" | Out-File $auditReportPath -Append
Get-Content $manifestPath | Select-String "Critical components status:" -Context 0,20 | ForEach-Object { $_.Line; $_.Context.PostContext } | Out-File $auditReportPath -Append

Write-Host "System audit report created successfully!"
Write-Host "Audit report location: $auditReportPath" 