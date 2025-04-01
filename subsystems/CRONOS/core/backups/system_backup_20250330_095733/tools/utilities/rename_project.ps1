powershell
# Script to rename the project directory and update references
# Setting encoding to UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

# Setting up log
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$logFile = "logs/rename_project.log"

function Write-LogMessage {
    param(
        [string]$message,
        [string]$type = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "$timestamp [$type] $message"
    Write-Host $logMessage
    Add-Content -Path $logFile -Value $logMessage -Encoding UTF8
}

# Check if the logs directory exists, if not, create it
if (-not (Test-Path "logs")) {
    New-Item -Path "logs" -ItemType Directory | Out-Null
    Write-LogMessage "Logs directory created successfully" "OK"
}

# Old and new paths
$oldPath = "C:\Eva & Guarani - EGOS"
$newPath = "C:\Eva e Guarani - EGOS"

Write-LogMessage "Starting project renaming process" "INFO"
Write-LogMessage "Old name: $oldPath" "INFO"
Write-LogMessage "New name: $newPath" "INFO"

# Check if the destination directory already exists
if (Test-Path $newPath) {
    Write-LogMessage "The destination directory '$newPath' already exists. Aborting." "ERROR"
    exit 1
}

# Get all code files
$fileExtensions = @("*.py", "*.ps1", "*.md", "*.txt", "*.json", "*.yaml", "*.yml", "*.cfg", "*.ini")
$files = @()

foreach ($ext in $fileExtensions) {
    $files += Get-ChildItem -Path "." -Filter $ext -Recurse -File
}

Write-LogMessage "Found $($files.Count) files to process" "INFO"

# Counters for the report
$filesUpdated = 0
$occurrencesReplaced = 0

# Update references in all files
foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    $oldPathEscaped = [regex]::Escape($oldPath)
    $newContent = $content -replace $oldPathEscaped, $newPath
    
    # Also replace versions with backslash escape
    $oldPathWithBackslashes = $oldPath -replace "\\", "\\"
    $newPathWithBackslashes = $newPath -replace "\\", "\\"
    $newContent = $newContent -replace $oldPathWithBackslashes, $newPathWithBackslashes
    
    # Replace versions with normal slash escape for URL use
    $oldPathForUrl = $oldPath -replace "\\", "/"
    $newPathForUrl = $newPath -replace "\\", "/"
    $newContent = $newContent -replace $oldPathForUrl, $newPathForUrl
    
    # Check if there were changes
    if ($content -ne $newContent) {
        Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8
        $replacements = (Select-String -InputObject $content -Pattern $oldPath -AllMatches).Matches.Count
        $replacements += (Select-String -InputObject $content -Pattern $oldPathWithBackslashes -AllMatches).Matches.Count
        $replacements += (Select-String -InputObject $content -Pattern $oldPathForUrl -AllMatches).Matches.Count
        
        Write-LogMessage "File updated: $($file.FullName) - $replacements occurrences" "OK"
        $filesUpdated++
        $occurrencesReplaced += $replacements
    }
}

Write-LogMessage "Total of $filesUpdated files updated with $occurrencesReplaced occurrences replaced" "INFO"

# Create a batch file to execute the renaming after the script finishes
$batchContent = @"
@echo off
echo Renaming project directory...
timeout /t 2 /nobreak
ren "$oldPath" "Eva e Guarani - EGOS"
echo Renaming completed! 
echo Please reopen the project in the new directory: $newPath
pause
"@

$batchPath = "rename_directory.bat"
Set-Content -Path $batchPath -Value $batchContent -Encoding ASCII

Write-LogMessage "Renaming script prepared: $batchPath" "OK"
Write-LogMessage "IMPORTANT INSTRUCTIONS:" "INFO"
Write-LogMessage "1. Close this terminal and all IDE/editor instances accessing this project" "INFO"
Write-LogMessage "2. Run the 'rename_directory.bat' file as administrator" "INFO"
Write-LogMessage "3. After renaming, open the project in the new directory: $newPath" "INFO"
Write-LogMessage "4. Update any external references to the project (shortcuts, etc.)" "INFO"

Write-LogMessage "Preparation process completed successfully!" "OK"