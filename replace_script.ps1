
$excludeDirs = 'node_modules|\.git|\.venv|__pycache__|dist|build|\.cursor'
$files = Get-ChildItem -Recurse -File -Include *.py,*.ts,*.tsx,*.json,*.md,*.html,*.yaml,*.yml,*.ini | Where-Object { $_.FullName -notmatch "\\($excludeDirs)\\" }
$modifiedCount = 0
foreach ($file in $files) {
    try {
        $content = [System.IO.File]::ReadAllText($file.FullName)
        $newContent = $content -creplace 'HarxitFlow', 'HarxitFlow'
        $newContent = $newContent -creplace 'harxitflow', 'harxitflow'
        $newContent = $newContent -creplace 'HARXITFLOW', 'HARXITFLOW'
        if ($newContent -ne $content) {
            [System.IO.File]::WriteAllText($file.FullName, $newContent)
            $modifiedCount++
        }
    } catch {
        # Ignore files that can't be read or written
    }
}
Write-Output "Total modified files: $modifiedCount"
