# side-hobby-sunwheel-loop

個人的に作った、Pygame の小さなループアニメーションです。
朝日から夕日へ移り変わる空と、静かに回る光の輪を図形だけで描いています。

## Features

- 8秒で自然に一周する、キー入力なしの2Dアニメーション
- 画像素材なし、Pygameの図形描画だけで構成
- 背景の空色が朝日から昼、夕日、薄暮へなめらかに変化
- 元の輪の回り方を保った粒子リング
- リサージュ曲線の軌跡と、太陽の反射を重ねた穏やかな画面

## 実行方法

### いちばん簡単な方法

GitHubからZIPファイルをダウンロードして展開したら、フォルダ内の `run_sunwheel.bat` をダブルクリックしてください。

VS Codeを開く必要はありません。初回起動時だけ、プロジェクト内に `.venv` を作成して `pygame` をインストールします。2回目以降は、そのままアニメーションを再生します。

Python 3.12系が必要です。手元では Python 3.12.4 と pygame 2.6.1 の組み合わせで動作確認しています。

初回起動時はインターネット接続が必要です。`pygame` のインストールが終わった後は、同じPCでは基本的に再インストールなしで起動できます。

### 手動で実行する方法

このアプリは `pygame` を使います。特定の環境名、たとえば `base2` に依存させず、プロジェクト専用の仮想環境 `.venv` を作って動かす方法も使えます。

### 1. Python のバージョンを確認

Python 3.12系で動かす想定です。

```powershell
py -3.12 --version
```

または:

```powershell
python --version
```

`Python 3.12.x` のように表示されればOKです。

### 2. プロジェクトフォルダへ移動

```powershell
cd C:\Work\Development\mineGitHub\side-hobby-sunwheel-loop
```

### 3. 仮想環境を作成

```powershell
py -3.12 -m venv .venv
```

`py -3.12` が使えない場合は、Python 3.12系が既定の `python` として使える状態で次を実行してください。

```powershell
python -m venv .venv
```

### 4. 仮想環境を有効化

```powershell
.\.venv\Scripts\Activate.ps1
```

PowerShellで実行ポリシーのエラーが出る場合は、現在のユーザーだけ許可してからもう一度有効化します。

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

有効化できると、プロンプトの先頭に `(.venv)` が表示されます。

### 5. pygame をインストール

```powershell
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

インストール確認:

```powershell
python -c "import pygame; print(pygame.version.ver)"
```

### 6. アプリを起動

```powershell
python main.py
```

次回以降は、プロジェクトフォルダで仮想環境を有効化してから `python main.py` を実行すれば動かせます。
