git fetch upstream

$skills = git ls-tree --name-only upstream/main skills/engineering/ | Where-Object { $_ -notmatch "README" }

foreach ($skillPath in $skills) {
    $skillName = Split-Path $skillPath -Leaf
    $dest = "$skillName\SKILL.md"
    $content = git show "upstream/main:$skillPath/SKILL.md" 2>$null
    if ($content) {
        New-Item -ItemType Directory -Path $skillName -Force | Out-Null
        $content | Out-File -FilePath $dest -Encoding utf8
        Write-Host "updated: $skillName"
    }
}
