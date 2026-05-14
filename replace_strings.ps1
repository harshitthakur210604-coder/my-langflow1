$extensions = @("*.py", "*.toml", "*.md", "*.mdx", "*.ts", "*.tsx", "*.json", "*.yml", "*.yaml", "*.txt", "*.js", "*.html", "*.css", "*.sh", "*.ps1")
$files = Get-ChildItem -Path D:\harxitflow -Include $extensions -Recurse | Where-Object { 
    $_.FullName -notlike "*.git*" -and 
    $_.FullName -notlike "*node_modules*" -and 
    $_.FullName -notlike "*.venv*" 
}

foreach ($file in $files) {
    try {
        $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
        if ($null -eq $content) { continue }
        
        $newContent = $content.Replace("HarxitFlow", "HarxitFlow")
        $newContent = $newContent.Replace("harxitflow", "harxitflow")
        $newContent = $newContent.Replace("HARXITFLOW", "HARXITFLOW")
        
        if ($content -ne $newContent) {
            Write-Host "Updating $($file.FullName)"
            Set-Content $file.FullName $newContent -NoNewline
        }
    } catch {
        Write-Warning "Failed to process $($file.FullName): $($_.Exception.Message)"
    }
}
