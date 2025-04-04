# EVA & GUARANI - Translation Tools PowerShell Runner
# This script helps run the translation tools to convert Portuguese content to English
# For the entire EVA & GUARANI system, not just the sandbox
# Usage: .\translate_tools.ps1

# Set console encoding to UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Show-Header {
    Write-Host "`n========================================================================" -ForegroundColor Cyan
    Write-Host "                EVA & GUARANI - Translation Tools Runner                " -ForegroundColor Cyan
    Write-Host "             (For the entire EVA & GUARANI system, not just sandbox)    " -ForegroundColor Cyan
    Write-Host "========================================================================`n" -ForegroundColor Cyan
}

function Check-Prerequisites {
    Write-Host "Checking prerequisites..." -ForegroundColor Yellow

    # Check if Python is installed
    try {
        $pythonVersion = python --version
        Write-Host "✓ Python is installed: $pythonVersion" -ForegroundColor Green
    }
    catch {
        Write-Host "✗ Python is not installed or not in PATH" -ForegroundColor Red
        Write-Host "  Please install Python 3.8 or later from https://python.org" -ForegroundColor Red
        exit 1
    }

    # Check for required packages
    try {
        $openaiInstalled = python -c "import openai" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ OpenAI package is installed" -ForegroundColor Green
        }
        else {
            Write-Host "Installing OpenAI package..." -ForegroundColor Yellow
            python -m pip install openai
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ OpenAI package installed successfully" -ForegroundColor Green
            }
            else {
                Write-Host "✗ Failed to install OpenAI package" -ForegroundColor Red
                exit 1
            }
        }
    }
    catch {
        Write-Host "✗ Error checking for OpenAI package: $_" -ForegroundColor Red
        exit 1
    }

    Write-Host "All prerequisites met`n" -ForegroundColor Green
}

function Show-Menu {
    Write-Host "Choose an option:" -ForegroundColor Cyan
    Write-Host "1. Scan project for Portuguese files" -ForegroundColor White
    Write-Host "2. Translate a specific file using AI" -ForegroundColor White
    Write-Host "3. Batch translate files from a report" -ForegroundColor White
    Write-Host "4. Help & Documentation" -ForegroundColor White
    Write-Host "5. Exit" -ForegroundColor White
    Write-Host ""

    $choice = Read-Host "Enter your choice (1-5)"
    return $choice
}

function Scan-Project {
    Write-Host "`nScanning project for Portuguese files...`n" -ForegroundColor Yellow

    # Default to the main EVA & GUARANI system root directory
    $defaultRootDir = Resolve-Path -Path "C:\Eva & Guarani - EGOS"

    if (-not (Test-Path $defaultRootDir)) {
        $defaultRootDir = Resolve-Path -Path "..\.."
    }

    Write-Host "This will scan the entire EVA & GUARANI system for Portuguese content." -ForegroundColor Yellow
    Write-Host "The scan will focus on project files and exclude system directories." -ForegroundColor Yellow
    Write-Host "This may take a few minutes depending on the size of your project." -ForegroundColor Yellow

    $rootDir = Read-Host "Enter root directory to scan (default: $defaultRootDir)"

    if ([string]::IsNullOrWhiteSpace($rootDir)) {
        $rootDir = $defaultRootDir
    }

    Write-Host "`nRunning scanner...`n" -ForegroundColor Yellow
    python translate_to_english.py --root-dir "$rootDir"

    if ($LASTEXITCODE -eq 0) {
        Write-Host "`nScan complete. Check translation_report.md for results.`n" -ForegroundColor Green
    }
    else {
        Write-Host "`nScan failed with error code $LASTEXITCODE`n" -ForegroundColor Red
    }

    Write-Host "Press any key to continue..."
    [void][System.Console]::ReadKey($true)
}

function Translate-File {
    Write-Host "`nTranslate a specific file using AI`n" -ForegroundColor Yellow

    $filePath = Read-Host "Enter the path to the file you want to translate"

    if (-not (Test-Path $filePath)) {
        Write-Host "`nFile does not exist: $filePath`n" -ForegroundColor Red
        Write-Host "Press any key to continue..."
        [void][System.Console]::ReadKey($true)
        return
    }

    # Default API key from the project
    $defaultApiKey = "REMOVED_API_KEY"

    $useDefaultKey = $true
    $apiKey = ""

    Write-Host "A default API key is available in the project." -ForegroundColor Green
    $useCustomKey = Read-Host "Do you want to use a different API key? (y/N)"

    if ($useCustomKey -eq "y" -or $useCustomKey -eq "Y") {
        $apiKey = Read-Host "Enter your OpenAI API key (or press Enter to use OPENAI_API_KEY environment variable)"
        $useDefaultKey = $false
    }

    $apiKeyParam = ""
    if ($apiKey) {
        $apiKeyParam = "--api-key `"$apiKey`""
    }
    elseif ($useDefaultKey) {
        # We'll use the default key integrated in the script
        $env:OPENAI_API_KEY = $defaultApiKey
    }

    $outputPath = Read-Host "Enter output file path (leave empty to replace original)"

    $outputParam = ""
    if ($outputPath) {
        $outputParam = "--output `"$outputPath`""
    }

    $dryRun = Read-Host "Do you want to perform a dry run (no changes will be made)? (y/N)"
    $dryRunParam = ""
    if ($dryRun -eq "y" -or $dryRun -eq "Y") {
        $dryRunParam = "--dry-run"
    }

    Write-Host "`nTranslating file..." -ForegroundColor Yellow

    $command = "python ai_translate_file.py --file `"$filePath`" $apiKeyParam $outputParam $dryRunParam"

    try {
        Invoke-Expression $command

        Write-Host "`nTranslation complete.`n" -ForegroundColor Green
    }
    catch {
        Write-Host "`nError during translation: $_`n" -ForegroundColor Red
    }

    Write-Host "Press any key to continue..."
    [void][System.Console]::ReadKey($true)
}

function Batch-Translate {
    Write-Host "`nBatch translate files from a translation report`n" -ForegroundColor Yellow

    $reportPath = Read-Host "Enter path to translation report (default: translation_report.md)"
    if ([string]::IsNullOrWhiteSpace($reportPath)) {
        $reportPath = "translation_report.md"
    }

    if (-not (Test-Path $reportPath)) {
        Write-Host "Report file not found: $reportPath`n" -ForegroundColor Red
        return
    }

    Write-Host "`nIMPORTANT: This requires an OpenAI API key." -ForegroundColor Magenta
    $apiKey = Read-Host "Enter your OpenAI API key (or press Enter to use OPENAI_API_KEY environment variable)"

    $apiKeyParam = ""
    if (-not [string]::IsNullOrWhiteSpace($apiKey)) {
        $apiKeyParam = "--api-key `"$apiKey`""
    }

    $priority = Read-Host "Process which priority files? (high/medium/low/all) (default: high)"
    if ([string]::IsNullOrWhiteSpace($priority)) {
        $priority = "high"
    }

    $dryRun = Read-Host "Run in dry-run mode (no changes will be made)? (y/n)"
    $dryRunParam = ""
    if ($dryRun -eq "y" -or $dryRun -eq "Y") {
        $dryRunParam = "--dry-run"
    }

    Write-Host "`nExtracting files from report...`n" -ForegroundColor Yellow

    # Read the markdown report and extract file paths
    $content = Get-Content -Path $reportPath -Raw
    $tableRegex = '(?s)\| File \| Type \| Size \| Priority \|\r?\n\|[^\r\n]*\r?\n(.*?)(?:\r?\n\r?\n|\z)'
    $rowRegex = '\| ([^\|]+) \| [^\|]+ \| [^\|]+ \| ([^\|]+) \|'

    $match = [regex]::Match($content, $tableRegex)
    if ($match.Success) {
        $table = $match.Groups[1].Value
        $rows = [regex]::Matches($table, $rowRegex)

        $filesToTranslate = @()
        foreach ($row in $rows) {
            $filePath = $row.Groups[1].Value.Trim()
            $filePriority = $row.Groups[2].Value.Trim().ToLower()

            if ($priority -eq "all" -or $filePriority -eq $priority) {
                $filesToTranslate += $filePath
            }
        }

        if ($filesToTranslate.Count -eq 0) {
            Write-Host "No files found matching priority: $priority" -ForegroundColor Red
            return
        }

        Write-Host "Found $($filesToTranslate.Count) files to translate with priority: $priority" -ForegroundColor Green

        $confirm = Read-Host "Proceed with translation? (y/n)"
        if ($confirm -ne "y" -and $confirm -ne "Y") {
            Write-Host "Translation cancelled." -ForegroundColor Yellow
            return
        }

        $successCount = 0
        $failCount = 0

        foreach ($file in $filesToTranslate) {
            $fullPath = Resolve-Path -Path (Join-Path -Path (Get-Location) -ChildPath "..\..") | Join-Path -ChildPath $file
            Write-Host "`nTranslating: $file" -ForegroundColor Cyan

            $command = "python ai_translate_file.py $apiKeyParam $dryRunParam `"$fullPath`""
            Invoke-Expression $command

            if ($LASTEXITCODE -eq 0) {
                $successCount++
            }
            else {
                $failCount++
            }
        }

        Write-Host "`nBatch translation complete." -ForegroundColor Green
        Write-Host "Successfully translated: $successCount files" -ForegroundColor Green
        Write-Host "Failed to translate: $failCount files" -ForegroundColor $(if ($failCount -gt 0) { "Red" } else { "Green" })
    }
    else {
        Write-Host "Could not find the files table in the report." -ForegroundColor Red
    }

    Write-Host "`nPress any key to continue..."
    [void][System.Console]::ReadKey($true)
}

function Show-Help {
    Write-Host "`nEVA & GUARANI Translation Tools Help`n" -ForegroundColor Cyan
    Write-Host "These tools help you standardize the EVA & GUARANI codebase to English."
    Write-Host ""
    Write-Host "Available Tools:" -ForegroundColor Yellow
    Write-Host "1. Portuguese File Scanner (translate_to_english.py)"
    Write-Host "   - Identifies files containing Portuguese content"
    Write-Host "   - Generates a report listing files that need translation"
    Write-Host ""
    Write-Host "2. AI-Assisted Translator (ai_translate_file.py)"
    Write-Host "   - Uses OpenAI API to translate files from Portuguese to English"
    Write-Host "   - Preserves code structure and functionality"
    Write-Host ""
    Write-Host "3. Batch Translation"
    Write-Host "   - Processes multiple files from a translation report"
    Write-Host "   - Prioritizes files based on importance"
    Write-Host ""
    Write-Host "Documentation:" -ForegroundColor Yellow
    Write-Host "For detailed instructions, see:"
    Write-Host "- Translation Guide: ../docs/TRANSLATION_GUIDE.md"
    Write-Host "- System Analysis: ../docs/SYSTEM_ANALYSIS.md"
    Write-Host "- Implementation Roadmap: ../docs/IMPLEMENTATION_ROADMAP.md"
    Write-Host ""
    Write-Host "Press any key to continue..."
    [void][System.Console]::ReadKey($true)
}

# Main script execution
try {
    # Set working directory to the script's directory
    Set-Location -Path $PSScriptRoot

    Show-Header
    Check-Prerequisites

    $exit = $false
    while (-not $exit) {
        Show-Header
        $choice = Show-Menu

        switch ($choice) {
            "1" { Scan-Project }
            "2" { Translate-File }
            "3" { Batch-Translate }
            "4" { Show-Help }
            "5" { $exit = $true }
            default {
                Write-Host "`nInvalid choice. Please try again.`n" -ForegroundColor Red
                Start-Sleep -Seconds 1
            }
        }
    }

    Write-Host "`nThank you for using EVA & GUARANI Translation Tools!`n" -ForegroundColor Cyan
}
catch {
    Write-Host "An error occurred: $_" -ForegroundColor Red
    exit 1
}
