# CAE ビルド起動スクリプト（恒久の仕組み）
# ------------------------------------------------------------------
# Build番号 = 1150 + コミット数 を自動計算し、必ず -f build_number として渡す。
# → GitHub Actions の run 名が必ず「CAE v<version> (<番号>) — <platforms> ビルド」になる。
# アプリ設定画面のビルド番号表示(src/buildInfo.ts)も、この番号でビルド時に埋め込まれる。
#
# 使い方(例):
#   pwsh tools/build_cae.ps1                       # 【既定=both】iOS+Android 両方(iOSはTestFlight/Androidは内部テスト)
#   pwsh tools/build_cae.ps1 -Platforms android    # 片方だけは明示指示があるときだけ(ユーザー厳命・feedback-build-both-os-always)
#   pwsh tools/build_cae.ps1 -AndroidTrack production -SubmitAndroid draft
# ------------------------------------------------------------------
# 【厳守】ビルドは必ず両OS(both)。片方だけ(iOS skipped含む)で終わらせない。
#   2026-10-09 既定を android→both に修正(Build1368をandroid単独で上げてiOSがTestFlightに出ず=重大違反)。
param(
  [ValidateSet('android', 'ios', 'both')][string]$Platforms = 'both',
  [ValidateSet('completed', 'draft', 'none')][string]$SubmitAndroid = 'completed',
  [ValidateSet('internal', 'alpha', 'beta', 'production')][string]$AndroidTrack = 'internal',
  [switch]$ForceIos
)
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo

# 1) ビルド番号 = 1150 + コミット数
$commits = [int](git rev-list --count HEAD)
$build = 1150 + $commits

# 2) アプリ版は app.json から取得(ベタ書きしない)
$appVersion = (Get-Content app.json -Raw | ConvertFrom-Json).expo.version

# 3) CI はリモート main を checkout するので、未push だと番号(コミット数)がズレる → 事前チェック
git fetch origin main --quiet 2>$null
$localHead = (git rev-parse HEAD).Trim()
$remoteHead = (git rev-parse origin/main 2>$null)
if ($remoteHead) { $remoteHead = $remoteHead.Trim() }
if ($localHead -ne $remoteHead) {
  Write-Host "⚠ ローカル HEAD と origin/main が不一致です。先に git push してください（未pushだとCIの番号がズレます）。" -ForegroundColor Yellow
  Write-Host "  local=$localHead  remote=$remoteHead"
  $ans = Read-Host "このまま起動しますか? (y/N)"
  if ($ans -ne 'y') { Write-Host "中止しました。"; exit 1 }
}

# 4) 予告表示 → dispatch
$runName = "CAE v$appVersion ($build) — $Platforms ビルド"
Write-Host "▶ 起動: $runName" -ForegroundColor Cyan
Write-Host "  submit_android=$SubmitAndroid  android_track=$AndroidTrack  force_ios=$([bool]$ForceIos)"

$ghArgs = @(
  'workflow', 'run', 'build-cae.yml', '--ref', 'main',
  '-f', "platforms=$Platforms",
  '-f', "build_number=$build",
  '-f', "app_version=$appVersion",
  '-f', "submit_android=$SubmitAndroid",
  '-f', "android_track=$AndroidTrack"
)
if ($ForceIos) { $ghArgs += @('-f', 'force_ios=true') }

& gh @ghArgs
if ($LASTEXITCODE -ne 0) { throw "gh workflow run が失敗しました" }

Start-Sleep -Seconds 3
Write-Host "`n最新の実行:" -ForegroundColor Cyan
gh run list --workflow=build-cae.yml -L 1
Write-Host "`n✅ 起動しました。run名に v$appVersion ($build) が入ります。" -ForegroundColor Green
