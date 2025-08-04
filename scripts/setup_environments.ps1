# CSV Data Profiler Environment Manager - Simplified

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Write-Header {
    param([string]$Title)
    Write-Host ""
    Write-Host ("=" * 50) -ForegroundColor Cyan
    Write-Host $Title -ForegroundColor Yellow
    Write-Host ("=" * 50) -ForegroundColor Cyan
}

# Check conda availability
function Test-CondaAvailable {
    try {
        $condaVersion = conda --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✓ Conda found: $condaVersion" "Green"
            return $true
        }
    }
    catch {
        Write-ColorOutput "✗ Conda not found. Install Anaconda/Miniconda first." "Red"
        return $false
    }
}

# Environment definitions
function Get-Environments {
    return @{
        1 = @{ Name = "csv-profiler-main"; File = "environments/environment-main.yml" }
        2 = @{ Name = "csv-profiler-profiling"; File = "environments/environment-profiling.yml" }
        3 = @{ Name = "csv-profiler-dataprep"; File = "environments/environment-dataprep.yml" }
    }
}

# Check if environment exists
function Test-EnvironmentExists {
    param([string]$EnvName)
    $envList = conda env list 2>$null
    return $envList -match "^$EnvName\s+"
}

# Show environment status
function Show-EnvironmentStatus {
    $environments = Get-Environments
    Write-Host "`nEnvironment Status:" -ForegroundColor Cyan
    
    foreach ($key in 1..3) {
        $env = $environments[$key]
        $status = if (Test-EnvironmentExists -EnvName $env.Name) { "✓ Installed" } else { "✗ Missing" }
        $color = if (Test-EnvironmentExists -EnvName $env.Name) { "Green" } else { "Red" }
        Write-ColorOutput "$key. $($env.Name) - $status" $color
    }
}

# Install/Update environment
function Manage-Environment {
    param([string]$EnvName, [string]$YmlFile, [bool]$IsUpdate = $false)
    
    if (-not (Test-Path $YmlFile)) {
        Write-ColorOutput "✗ File not found: $YmlFile" "Red"
        return $false
    }
    
    $exists = Test-EnvironmentExists -EnvName $EnvName
    
    try {
        if ($exists -and $IsUpdate) {
            Write-ColorOutput "Updating $EnvName..." "Yellow"
            conda env update -f $YmlFile --prune
        }
        elseif (-not $exists) {
            Write-ColorOutput "Installing $EnvName..." "Green"
            conda env create -f $YmlFile
        }
        else {
            Write-ColorOutput "$EnvName already exists. Use update option." "Yellow"
            return $false
        }
        
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✓ $EnvName completed successfully" "Green"
            return $true
        }
        else {
            Write-ColorOutput "✗ Failed to setup $EnvName" "Red"
            return $false
        }
    }
    catch {
        Write-ColorOutput "✗ Error: $($_.Exception.Message)" "Red"
        return $false
    }
}

# Remove environment
function Remove-Environment {
    param([string]$EnvName)
    
    if (-not (Test-EnvironmentExists -EnvName $EnvName)) {
        Write-ColorOutput "✗ $EnvName not installed" "Yellow"
        return
    }
    
    $confirm = Read-Host "Remove $EnvName? (y/N)"
    if ($confirm -eq 'y') {
        conda env remove -n $EnvName
        Write-ColorOutput "✓ $EnvName removed" "Green"
    }
}

# Main menu
function Show-Menu {
    Write-Host "`nOptions:" -ForegroundColor Cyan
    Write-Host "1. Install All"
    Write-Host "2. Update All" 
    Write-Host "3. Remove All"
    Write-Host "4. Install Single"
    Write-Host "5. Remove Single"
    Write-Host "0. Exit"
}

# Main function
function Main {
    Clear-Host
    Write-Header "CSV Profiler Environment Manager"
    
    if (-not (Test-CondaAvailable)) {
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    $environments = Get-Environments
    
    do {
        Show-EnvironmentStatus
        Show-Menu
        $choice = Read-Host "`nSelect option"
        
        switch ($choice) {
            '1' {
                # Install All
                foreach ($key in 1..3) {
                    $env = $environments[$key]
                    Manage-Environment -EnvName $env.Name -YmlFile $env.File
                }
            }
            '2' {
                # Update All
                foreach ($key in 1..3) {
                    $env = $environments[$key]
                    Manage-Environment -EnvName $env.Name -YmlFile $env.File -IsUpdate $true
                }
            }
            '3' {
                # Remove All
                $confirm = Read-Host "Remove ALL environments? (y/N)"
                if ($confirm -eq 'y') {
                    foreach ($key in 1..3) {
                        $env = $environments[$key]
                        if (Test-EnvironmentExists -EnvName $env.Name) {
                            conda env remove -n $env.Name
                        }
                    }
                    Write-ColorOutput "✓ All environments removed" "Green"
                }
            }
            '4' {
                # Install Single
                $envChoice = Read-Host "Select environment (1-3)"
                if ($envChoice -in 1..3) {
                    $env = $environments[[int]$envChoice]
                    Manage-Environment -EnvName $env.Name -YmlFile $env.File
                }
            }
            '5' {
                # Remove Single
                $envChoice = Read-Host "Select environment (1-3)"
                if ($envChoice -in 1..3) {
                    $env = $environments[[int]$envChoice]
                    Remove-Environment -EnvName $env.Name
                }
            }
            '0' {
                Write-ColorOutput "`nExiting..." "Yellow"
                break
            }
            default {
                Write-ColorOutput "Invalid option" "Red"
            }
        }
        
        if ($choice -ne '0') {
            Read-Host "`nPress Enter to continue"
            Clear-Host
            Write-Header "CSV Profiler Environment Manager"
        }
        
    } while ($choice -ne '0')
}

Main