# django-on-hatch

[![PyPI - Version](https://img.shields.io/pypi/v/django-hatch.svg)](https://pypi.org/project/django-hatch)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-hatch.svg)](https://pypi.org/project/django-hatch)

このリポジトリは[Hatch](https://hatch.pypa.io/latest/)プロジェクトマネージャーを使ったDjangoのアプリ開発用テンプレートです。

Djangoのサブコマンドである「django-admin startproject」及び、オプションの「--template、--extension」を使用してこのカを読み込んでください。

無事にカスタムテンプレートが読み込まれると、Hatchプロジェクトマネージャーを使ったDjangoアプリの開発をスタートすることができます。

Hatchの使い方を知っているだけで、以下の事が容易に実行できます。

- 開発環境のセットアップ
- スピーディーなアプリ開発
- CI/CD

-----

**目次**
- [インストール](#インストール)
- [設定](#設定)
- [開発](#開発)
- [パッケージの組み込みテスト](#パッケージの組み込みテスト)
- [License](#license)

## インストール

実行環境は「Windows Sybsystem for Linux 2」のUbuntuターミナルです。


Pythonの環境をセットアップします。

以下はpyenvを使用してPython3.7の環境を作成した例。

```console
$ pyenv local 3.7

$ python3 --version
Python 3.7.0
```

仮想環境を作成して有効にし、`Hatch`をインストールします。

```console
$ python3 -m venv .venv && . .venv/bin/activate

$ pip install --upgrade pip

$ pip install hatch keyrings.alt
```

「keyrings.alt」はPyPIに公開する際に使います。

次に、Hatchプロジェクトの初期化を実行し「pyproject.toml」を作成します。

```console
$ hatch new --init
Project name: Django project
Description []: Django開発のプロジェクト
Wrote: pyproject.toml

$ ls
pyproject.toml
```

「Project name」と「Description」を設定するとカレントディレクトリに「pyproject.toml」が作成されます。

エディターモードで「pyproject.toml」の一部を変更します。

```toml
# pyproject.toml

# ...

[project]
# ...
# dynamic = ["version"]  # 動的のキーに対してコメントアウト
# ...
dependencies = ["Django"]  # 依存関係にDjangoを設定
```

「project」テーブルの「dynamic」キーと「dependencies」キーに対して変更を加えます。

Hatchの「run」コマンドを使ってDjangoプロジェクトのカスタムテンプレートを解凍します。

```console
$ hatch run django-admin startproject \
    --template=https://github.com/kenno-warise/django-on-hatch/archive/main.zip \
    --extension=py,toml,txt,html,css \
    new_app
```

作成された「new_app」ディレクトリ内には既にアプリケーションに因んだ環境が整えられています。

```
new_app
├── LICENSE.txt
├── README.md
├── new_app
│   └── __init__.py
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── pyproject.toml
└── requirements.txt
```

「new_app」用に設定された「pyproject.toml」が配置されているディレクトリに移動し、hatchの環境を作成します。

```console
$ cd new_app

$ hatch env create

$ hatch env show

```

データベースを初期化してアプリを起動します。

```console
$ hatch run migrate

$ hatch run runserver
```

## 設定

Hatchが配置する仮想環境のディレクトリを決める。

デフォルト設定で配置されるディレクトリは以下のコマンドで参照できる。

```console
$ hatch config show | grep 'data'
data = "/home/user/.local/share/hatch"
```

デフォルト値を変更する場合は以下のコマンドを実行する。

```console
$ hatch config set dirs.data 配置するディレクトリ
```

Djangoのバージョンの変更をしたい場合は以下を編集してください。

`requirements.txt`

```
django==2.2.5
```

ショートカットとしてHatchの「run」コマンドで実行できるDjangoのコマンドは`pyproject.toml`の「tool.hatch.envs.default.scripts」テーブルによって登録しています。

```toml
[tool.hatch.envs.default.scripts]
migrate = "python3 manage.py migrate"
makemigrations = "python3 manage.py makemigrations {args}"
createsuperuser = "python3 manage.py createsuperuser"
runserver = "python3 manage.py runserver"
startapp = "python3 manage.py startapp {args}"
shell = "python3 manage.py shell"
test = "python3 manage.py test {args}"
cov = "coverage run --include=new_app/* --omit=new_app/test*,new_app/__init__.py,new_app/migrations/* manage.py test {args}"
cov-report = "coverage report -m"
```

データベースを作成する場合はマイグレートを実行します。

```consolw
$ hatch run migrate
```

Djangoを起動します。

```console
$ hatch run runserver
```

## 開発

バージョン情報の設定

Hatchの「version」コマンドでDjangoアプリのバージョン情報を確認できます。

```console
$ hatch version
0.0.1
```

DjangoアプリをパッケージングしてPyPIにアップロードする。

`pyproject.toml`に配布するファイルと配布しないファイルを設定できます。

```toml
[tool.hatch.build]
include = ["new_app/*"] # templatesとstaticも含まれます。
exclude = ["new_app/migrations/*"]
```

上記以外にあれば追記します。

バージョンを更新する場合は「version」コマンドを実行します。

```console
$ hatch version micro
Old: 0.0.1
New: 0.0.2
```

ビルドを実行します。

```console
$ hatch build
```

アーティファクトを公開します。

```console
$ hatch publish
```

## パッケージの組み込みテスト

プロジェクトはGitHub等に保存しておきます。

既存プロジェクトの「new_app」を削除すると他のディレクトリに移動します。

```console
$ ls

$ rm -rf new_app
```

「requirements.txt」にPyPIへアップロードした「new_app」を定義します。

```txt
new_app
```

必要であればマイグレートとスーパーユーザーを作成します。

```console
$ hatch run migrate

$ hatch run createsuperuser
```

サーバーを起動します。

```console
$ hatch run runserver
```


## License

`django-on-hatch` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
