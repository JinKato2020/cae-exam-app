# 問題をビルドなしで差し替える（EAS Update / OTA）手順

問題JSON（`content/questions/*.json`）はJSバンドルに含まれる。**EAS Update** を使うと、App Store審査を通さずにJSバンドル（＝問題データ・軽微なコード修正）を配信できる。ユーザーは次回起動時に自動でダウンロードする。

## 前提（この構成の要点）
- 本アプリは **EAS Build を使わず**、GitHub Actions 上で `npx expo prebuild` → `xcodebuild` でビルドしている（`ios/` はコミットせず毎回生成）。
- そのため OTA に必要な設定は **app.json 側**（`updates.url` / `runtimeVersion` / チャンネル）に入れる。prebuild がネイティブへ反映する。
- 済んでいること: `expo-updates` 導入、`app.json` に `runtimeVersion: "1.0.0"`（固定＝同じ土台に何度でもOTAできる）、`eas.json` の各プロファイルに `channel`。

## A. 一度だけの準備（あなたの作業・Expoアカウントが要る）
1. Expoアカウント作成（無料）: https://expo.dev/signup
2. ログイン: `npx eas login`
3. プロジェクト作成＆設定: `npx eas update:configure`
   - `app.json` に `updates.url`（`https://u.expo.dev/<プロジェクトID>`）と `extra.eas.projectId` が自動で入る。
   - `runtimeVersion` は **"1.0.0" のまま**にする（appVersion ポリシーに変えられたら "1.0.0" へ戻す）。
4. **チャンネルの固定（この構成では手動で1行）**: `app.json` の `expo.updates` に次を足す（EAS Build を使わないビルドはこれで受信チャンネルが決まる）:
   ```json
   "updates": {
     "url": "https://u.expo.dev/<プロジェクトID>",
     "requestHeaders": { "expo-channel-name": "production" }
   }
   ```
5. **一度だけ再ビルド**（expo-updates をバイナリに焼き込むため）: いつもの GitHub Actions ビルド → TestFlight 提出。以降、このビルドが OTA を受け取る。

## B. 問題を差し替える（毎回・審査なし）
1. `content/questions/*.json` を編集（作問パイプラインの品質ゲートを通す）。
2. 配信: `npx eas update --branch production -m "第◯章 修正"`
3. ユーザーは次回アプリ起動時に自動ダウンロード＝差し替え完了。

## C. 注意
- **問題差し替えだけ**なら `runtimeVersion` を触らない＝OTAで届く。
- **ネイティブが変わる変更**（新しいライブラリ追加＝今回の課金 `react-native-purchases` や `expo-updates` 自体、`app.json` のネイティブ設定変更など）は、最初の1回はストア用ビルドが必要。以降 `runtimeVersion` を上げたら、それに合う新ビルドを配ってから OTA する。
- **Apple 規約**: OTA はバグ修正・コンテンツ更新の範囲で使う（アプリの性質を大きく変える改造は不可）。
- `--branch preview` を使えば内部確認用チャンネルへ先に配信して検証できる（`eas.json` に `preview` チャンネル済み）。
