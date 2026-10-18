param(
    [string]$RepoName = 'rea-vm',
    [ValidateSet('private', 'public')]
    [string]$Visibility = 'private'
)

$ErrorActionPreference = 'Stop'

$gh = (Get-Command gh -ErrorAction SilentlyContinue).Source
if (-not $gh) {
    $portable = 'D:\Tools\gh\bin\gh.exe'
    if (Test-Path -LiteralPath $portable) {
        $gh = $portable
    } else {
        throw 'GitHub CLI not found. Install gh or add D:\Tools\gh\bin to PATH.'
    }
}

& $gh auth status
if ($LASTEXITCODE -ne 0) {
    throw 'Not authenticated. Run: gh auth login'
}

$name = git config user.name
$email = git config user.email
if (-not $name -or -not $email) {
    Write-Warning 'git user.name / user.email are not set globally; set them before publishing.'
}

git remote get-url origin 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    & $gh repo create $RepoName "--$Visibility" --source . --remote origin --push
} else {
    git push -u origin main
}
