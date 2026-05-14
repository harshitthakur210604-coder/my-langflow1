$targetStrings = @("Langflow", "langflow", "LANGFLOW")
$replacementStrings = @("HarxitFlow", "harxitflow", "HARXITFLOW")

# Find all files excluding .git, node_modules, .venv
$files = Get-ChildItem -Path D:\langflow -Recurse -File | Where-Object {
    $_.FullName -notlike "*.git*" -and
    $_.FullName -notlike "*node_modules*" -and
    $_.FullName -notlike "*.venv*" -and
    $_.Name -ne "replace_strings_v2.ps1" -and
    $_.Name -ne "replace_strings.ps1"
}

foreach ($file in $files) {
    # Skip potential binary files by checking extension or using a heuristic
    $binaryExtensions = @(".exe", ".dll", ".so", ".pyc", ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".tar", ".gz", ".7z", ".pyo", ".pyd", ".db", ".sqlite")
    if ($binaryExtensions -contains $file.Extension.ToLower()) {
        continue
    }

    try {
        $content = [System.IO.File]::ReadAllText($file.FullName)
        $modified = $false
        $newContent = $content

        for ($i = 0; $i -lt $targetStrings.Count; $i++) {
            if ($newContent.Contains($targetStrings[$i])) {
                $newContent = $newContent.Replace($targetStrings[$i], $replacementStrings[$i])
                $modified = $true
            }
        }

        if ($modified) {
            Write-Host "Updating $($file.FullName)"
            [System.IO.File]::WriteAllText($file.FullName, $newContent)
        }
    } catch {
        # Likely a binary file or encoding issue, skip
        Write-Warning "Skipping $($file.FullName): $($_.Exception.Message)"
    }
}
