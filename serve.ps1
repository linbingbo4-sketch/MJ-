# Used by "Start (Windows).bat" when Python is not installed: the same local server, with byte ranges for the videos.
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$types = @{ '.html'='text/html; charset=utf-8'; '.js'='text/javascript'; '.css'='text/css'; '.json'='application/json'; '.md'='text/plain; charset=utf-8';
  '.jpg'='image/jpeg'; '.jpeg'='image/jpeg'; '.png'='image/png'; '.webp'='image/webp'; '.svg'='image/svg+xml';
  '.mp4'='video/mp4'; '.webm'='video/webm'; '.mp3'='audio/mpeg'; '.m4a'='audio/mp4'; '.ogg'='audio/ogg'; '.wav'='audio/wav' }
$listener = $null
foreach ($port in 8000..8019) {
  $l = New-Object System.Net.HttpListener
  $l.Prefixes.Add("http://localhost:$port/")
  try { $l.Start(); $listener = $l; break } catch { $l.Close() }
}
if (-not $listener) { Write-Host 'No free port between 8000 and 8019.'; Read-Host 'Press Enter to close'; exit 1 }
$url = "http://localhost:$port/index.html"
Write-Host "BEYOND THE SPOTLIGHT  ->  $url"
Write-Host 'Keep this window open while presenting. Close it to stop.'
Start-Process $url
while ($listener.IsListening) {
  $ctx = $listener.GetContext(); $req = $ctx.Request; $res = $ctx.Response
  try {
    $rel = [Uri]::UnescapeDataString($req.Url.AbsolutePath.TrimStart('/'))
    if ($rel -eq '') { $rel = 'index.html' }
    $path = [IO.Path]::GetFullPath((Join-Path $root $rel))
    if (-not $path.StartsWith($root) -or -not (Test-Path -LiteralPath $path -PathType Leaf)) { $res.StatusCode = 404; $res.Close(); continue }
    $ext = [IO.Path]::GetExtension($path).ToLower()
    $res.ContentType = $(if ($types.ContainsKey($ext)) { $types[$ext] } else { 'application/octet-stream' })
    $res.AddHeader('Accept-Ranges', 'bytes'); $res.AddHeader('Cache-Control', 'no-cache')
    $fs = [IO.File]::OpenRead($path); $size = $fs.Length; $start = 0; $end = $size - 1
    $range = $req.Headers['Range']
    if ($range -match '^bytes=(\d*)-(\d*)$') {
      if ($matches[1] -ne '') { $start = [int64]$matches[1]; if ($matches[2] -ne '') { $end = [Math]::Min([int64]$matches[2], $size - 1) } }
      elseif ($matches[2] -ne '') { $start = [Math]::Max(0, $size - [int64]$matches[2]) }
      if ($start -ge $size) { $res.StatusCode = 416; $res.AddHeader('Content-Range', "bytes */$size"); $fs.Close(); $res.Close(); continue }
      $res.StatusCode = 206; $res.AddHeader('Content-Range', "bytes $start-$end/$size")
    }
    $len = $end - $start + 1; $res.ContentLength64 = $len
    if ($req.HttpMethod -ne 'HEAD') {
      $fs.Seek($start, 'Begin') | Out-Null; $buf = New-Object byte[] 65536
      while ($len -gt 0) { $n = $fs.Read($buf, 0, [Math]::Min($buf.Length, $len)); if ($n -le 0) { break }; $res.OutputStream.Write($buf, 0, $n); $len -= $n }
    }
    $fs.Close()
  } catch { } finally { try { $res.Close() } catch { } }
}
