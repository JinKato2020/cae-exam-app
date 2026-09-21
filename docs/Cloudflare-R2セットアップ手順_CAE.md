# CAE コンテンツOTA：Cloudflare R2 セットアップ手順（あなたの手作業ぶん）

これは「棚（＝ネット上の置き場所）」を用意する手順です。**1回やれば以降ずっと使えます**。
量産方針どおり、**1つの棚を全アプリで共有**し、アプリごとにフォルダ（`cae/` など）で分けます。
所要 15〜20分。すべて無料の範囲です。

---

## 全体像（何をするか）
1. Cloudflare に「棚（R2バケット）」を1つ作る
2. その棚に住所（`content.safa-lang.com`）を付ける
3. GitHub が棚に書き込むための「鍵（APIトークン）」を作る
4. GitHub にその鍵を登録する
5. 配信ボタンを押して、ブラウザで確認する

> ✅ JLPTと同じCloudflareアカウントを使います（`jlpt.safa-lang.com` が動いているアカウント）。

---

## 手順1：棚（R2バケット）を作る
1. https://dash.cloudflare.com を開く → 左メニュー **R2**
2. **Create bucket（バケットを作成）**
3. 名前：**`safa-content`**（全アプリ共有の棚。この名前を後で使います）
4. Location は自動でOK → **Create bucket**

## 手順2：棚に住所（カスタムドメイン）を付ける
1. いま作った `safa-content` を開く → 上部タブ **「設定」**
2. 左の細いメニューの **「カスタム ドメイン」** をクリック（※「パブリック開発 URL」ではない方）
3. **「ドメインを接続」** ボタン → 入力欄に **`content.safa-lang.com`** → **「続行」→「接続」**
   - `safa-lang.com` は既にCloudflareにあるので、DNSは自動で追加されます（数分で有効化）。
4. 状態が **「アクティブ」** になればOK。

> これで `https://content.safa-lang.com/` が `safa-content` の棚を指します。
> CAEのファイルは `content.safa-lang.com/cae/…` に置かれます（`cae/` は配信スクリプトが自動で付けます）。

## 手順3：書き込み用の鍵（R2 APIトークン）を作る
1. R2 のトップ画面右上 **Manage R2 API Tokens（API トークン）**
2. **Create API token**
3. 権限：**Object Read & Write**（読み書き）を選ぶ
4. 対象：**Apply to all buckets**（または `safa-content` のみでも可）
5. **Create** を押すと、次の3つが表示されます。**この画面でしか出ないので必ず控える**：
   - **Access Key ID**
   - **Secret Access Key**
   - **Endpoint**（`https://＜アカウントID＞.r2.cloudflarestorage.com` の形）
     - ※ もし Endpoint が表示されない場合は、R2トップ画面の「Account details」にある **S3 API** のURLがそれです。

## 手順4：GitHub に鍵を登録する
1. CAEのGitHubリポジトリ → **Settings → Secrets and variables → Actions**
2. **New repository secret** で次の**4つ**を登録（名前は下記そのまま）：

   | Secret 名 | 中身 |
   |---|---|
   | `R2_ACCESS_KEY_ID` | 手順3の Access Key ID |
   | `R2_SECRET_ACCESS_KEY` | 手順3の Secret Access Key |
   | `R2_ENDPOINT` | 手順3の Endpoint（`https://…r2.cloudflarestorage.com`）|
   | `R2_BUCKET` | **`safa-content`**（手順1の棚の名前）|

   > ⚠️ 貼り付け時に**前後の空白・改行を入れない**こと（特に Endpoint。JLPTで実害あり）。

## 手順5：配信して確認する
1. GitHub → **Actions** → **「CAE コンテンツ配信 (R2 / OTA)」** → **Run workflow**
2. 緑（成功）になったら、ブラウザで開いて確認：
   - https://content.safa-lang.com/cae/_manifest.json ← JSONが表示されればOK
   - 例：https://content.safa-lang.com/cae/figures/（任意の図名）.png ← 画像が出ればOK

---

## これ以降の運用（毎回やること）
- 問題・解説・図を直す → GitHubにpush → **Actionsで「CAE コンテンツ配信」をRun** するだけ。
- アプリは**次回起動時**に、変わった分だけ自動で受け取ります（ビルド不要）。
- ただし **最初の1回だけ「土台ビルド(P5)」が必要**です（`expo-file-system` を含めるため）。それ以降はビルド不要。

## 新しい資格アプリを足すとき（量産）
- 棚もドメインも鍵も**そのまま流用**。新アプリのリポジトリに同じ4つのsecretを入れ、配信スクリプトの `cae` を新アプリIDに変えるだけ。
- ファイルは `content.safa-lang.com/＜新アプリID＞/…` に分かれて置かれます。

---
CAE試験対策アプリ ／ 自前コンテンツOTA P4資料 ／ 2026-09-22
