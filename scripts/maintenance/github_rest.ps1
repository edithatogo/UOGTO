[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateSet('GET', 'POST', 'PATCH', 'PUT', 'DELETE')]
    [string]$Method,

    [Parameter(Mandatory)]
    [string]$Path,

    [Parameter()]
    [object]$Body
)

$ErrorActionPreference = 'Stop'
$token = gh auth token --hostname github.com
if (-not $token) {
    throw 'No GitHub token is available through gh auth.'
}

$uri = if ($Path -match '^https://') { $Path } else { "https://api.github.com/$($Path.TrimStart('/'))" }
$headers = @(
    '-H', "Authorization: Bearer $token",
    '-H', 'Accept: application/vnd.github+json',
    '-H', 'X-GitHub-Api-Version: 2022-11-28'
)
$args = @('-sS', '--fail-with-body', '--connect-timeout', '15', '--max-time', '60', '-X', $Method) + $headers
if ($null -ne $Body) {
    $json = if ($Body -is [string]) { $Body } else { $Body | ConvertTo-Json -Depth 20 -Compress }
    $args += @('-H', 'Content-Type: application/json', '--data-raw', $json)
}
$result = & curl.exe @args $uri
if ($LASTEXITCODE -ne 0) {
    throw "GitHub REST request failed with exit code $LASTEXITCODE"
}
$result
