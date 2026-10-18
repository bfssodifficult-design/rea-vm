param(
    [string]$Config
)

$python = (Get-Command python -ErrorAction Stop).Source
$script = Join-Path $PSScriptRoot 'preflight_check.py'

$args = @($script, '--json')
if ($Config) {
    $args += @('--config', $Config)
}

& $python @args
