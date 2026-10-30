# CAE ビルド起動スクリプト（恒久の仕組み）
# ------------------------------------------------------------------
# Build番号 = 1150 + コミット数 を自動計算し、必ず -f build_number として渡す。
# → run名は起動元の版とBuild番号、ジョブ名はApple事前確認で決定した実際の版を表示する。
# アプリ設定画面のビルド番号表示(src/buildInfo.ts)も、この番号でビルド時に埋め込まれる。
#
# 使い方(例):
#   pwsh tools/build_cae.ps1                       # 【既定=both】iOS+Android 両方(iOSはTestFlight/Androidは内部テスト)
#   pwsh tools/build_cae.ps1 -Platforms android    # 片方だけは明示指示があるときだけ(ユーザー厳命・feedback-build-both-os-always)
#   pwsh tools/build_cae.ps1 -AndroidTrack production -SubmitAndroid draft
#   pwsh tools/build_cae.ps1 -Ref codex/release-example # 専用ビルド枝も同じゲートを通す
# ------------------------------------------------------------------
# 【厳守】ビルドは必ず両OS(both)。片方だけ(iOS skipped含む)で終わらせない。
#   2026-10-09 既定を android→both に修正(Build1368をandroid単独で上げてiOSがTestFlightに出ず=重大違反)。
param(
  [ValidateSet('android', 'ios', 'both')][string]$Platforms = 'both',
  [ValidateSet('completed', 'draft', 'none')][string]$SubmitAndroid = 'completed',
  [ValidateSet('internal', 'alpha', 'beta', 'production')][string]$AndroidTrack = 'internal',
  [string]$Ref = 'main',
  [switch]$ForceIos
)
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo

# 起動対象のリモート版で番号・版・機械ゲートを確認する。作業フォルダの版を流用しない。
git fetch origin $Ref --quiet
if ($LASTEXITCODE -ne 0) { throw "起動対象のrefを取得できません: $Ref" }
$remoteHead = (git rev-parse FETCH_HEAD).Trim()
$workflow = git show "${remoteHead}:.github/workflows/build-cae.yml"
if ($LASTEXITCODE -ne 0 -or ($workflow -join "`n") -notmatch 'prepare-version:' -or ($workflow -join "`n") -notmatch 'tools/resolve_build_version.cjs') {
  throw "対象refにApple版確認ゲートがありません。新しいビルド処理を取り込んでから起動してください: $Ref"
}
git cat-file -e "${remoteHead}:tools/resolve_build_version.cjs"
if ($LASTEXITCODE -ne 0) { throw '版確認スクリプトが起動対象refにありません' }
git cat-file -e "${remoteHead}:tools/test_build_version.cjs"
if ($LASTEXITCODE -ne 0) { throw '版確認テストが起動対象refにありません' }
$commits = [int](git rev-list --count $remoteHead)
$build = 1150 + $commits

# 2) 起動元の版はリモートapp.jsonから取得。両OSの実際の版はCIの共有事前処理で決定する。
$appVersion = ((git show "${remoteHead}:app.json") -join "`n" | ConvertFrom-Json).expo.version
if ($LASTEXITCODE -ne 0 -or -not $appVersion) { throw '起動対象refのapp.jsonを取得できません' }

# 4) 予告表示 → dispatch
$runName = "CAE v$appVersion 以上 ($build) — $Platforms ビルド（Apple確認で版を自動決定）"
Write-Host "▶ 起動: $runName" -ForegroundColor Cyan
Write-Host "  submit_android=$SubmitAndroid  android_track=$AndroidTrack  force_ios=$([bool]$ForceIos)"

$ghArgs = @(
  'workflow', 'run', 'build-cae.yml', '--ref', $Ref,
  '-f', "platforms=$Platforms",
  '-f', "build_number=$build",
  '-f', "app_version=$appVersion",
  '-f', "submit_android=$SubmitAndroid",
  '-f', "android_track=$AndroidTrack"
)
if ($ForceIos) { $ghArgs += @('-f', 'force_ios=true') }

& gh @ghArgs
if ($LASTEXITCODE -ne 0) { throw "gh workflow run が失敗しました" }

Write-Host "`n起動を受け付けました。Build $build、実際の版は両OSのジョブ名に表示されます。" -ForegroundColor Green
