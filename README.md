# django-on-hatch

[![PyPI - Version](https://img.shields.io/pypi/v/django-hatch.svg)](https://pypi.org/project/django-hatch)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-hatch.svg)](https://pypi.org/project/django-hatch)

このリポジトリは[Hatch](https://hatch.pypa.io/latest/)プロジェクトマネージャーを使ったDjangoのアプリ開発用テンプレートです。

Djangoのサブコマンドである「django-admin startproject」及び、オプションの「--template、--extension」を使用してこのカスタムテンプレートを読みます。

無事にカスタムテンプレートが読み込まれると、Hatchプロジェクトマネージャーを使ったDjangoアプリの開発をスタートすることができます。

Hatchの使い方を知っているだけで、以下の事が容易に実行できます。

- 開発環境のセットアップ
- スピーディーなアプリ開発
- CI/CD

-----

**目次**
- [インストール](#インストール)
- [準備](#準備)
- [Djangoプロジェクト環境のセットアップ](#Djangoプロジェクト環境のセットアップ)
- [デプロイ](#デプロイ)
- [パッケージの組み込みテスト](#パッケージの組み込みテスト)
- [License](#license)

## インストール

実行環境は「Windows Sybsystem for Linux 2」のUbuntuです。

このカスタムテンプレートの仕様はPython3.7.0です。

```console
$ python3 --version
Python 3.7.0
```

仮想環境を作成して有効にし、`Hatch`をインストールします。

```console
$ python3 -m venv .venv && source .venv/bin/activate

$ pip install --upgrade pip

$ pip install hatch keyrings.alt
```

「keyrings.alt」はPyPIに公開する際に使います。

## 準備

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
dependencies = ["django<=*.*.*"]  # 依存関係にお好きなDjangoのバージョンを設定

# このプロジェクトでは必要無いのでコメントアウト
# [tool.hatch.version]
# path = "django_project/__about__.py"
```

「project」テーブルの「dynamic」キーと「dependencies」キー、そして「tool.hatch.version」テーブルに対して変更を加えます。

## Djangoのカスタムテンプレートの読み込み

「CI/CD」が必要な場合と必要ではない場合の読み込み方法を実行します。

「CI/CD」が有りの場合は、`git clone`コマンドで一度レポジトリを落として読み込みます。

```console
$ git clone

$ ls
django-on-hatch pyproject.toml
```

次に`django-admin startproject`コマンドのオプション、`--template`で「django-on-hatch」を指定し、`--extension`でプレースホルダーを設定している「py,txt,toml,html」を指定してプロジェクトを作成します。

```console
$ hatch run django-admin startproject \
    --template=django-on-hatch \
    --extension=py,txt,toml,html \
    sample
```

するとカレントディレクトリに「sample」というカスタムテンプレートを読み込んだDjangoプロジェクトが作成されます。

「django-on-hatch」ディレクトリの中から、「CI/CD」である「.github」ディレクトリを「sample」ディレクトリ内にコピーします。

```console
$ ls
django-on-hatch sample pyproject.toml

$ cp -r django-on-hatch/.github sample/.

$ tree sample -a
sample
├── .github
│   └── workflows
│       ├── publish.yml
│       └── test.yml
├── .gitignore
├── LICENSE.txt
├── README.md
├── config
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── pyproject.toml
├── requirements.txt
├── sample
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── static
│   │   └── sample
│   │       ├── css
│   │       │   └── style.css
│   │       ├── icon
│   │       │   └── favicon.png
│   │       └── js
│   │           └── style.js
│   ├── templates
│   │   └── sample
│   │       ├── base_index.html
│   │       └── index.html
│   ├── tests
│   │   ├── __init__.py
│   │   └── tests.py
│   ├── urls.py
│   └── views.py
└── templates
    └── base.html
```

「CI/CD」が無しでも構わない場合は、アーカイブから直接読み込んでしまいます。

```console
$ hatch run django-admin startproject \
    --template=https://github.com/kenno-warise/django-on-hatch/archive/main.zip \
    --extension=py,txt,toml,html \
    sample
```

するとカスタムテンプレートのDjangoプロジェクトが作成されます。

```cosole
$ tree sample -a
sample
├── .gitignore
├── LICENSE.txt
├── README.md
├── config
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── pyproject.toml
├── requirements.txt
├── sample
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── static
│   │   └── sample
│   │       ├── css
│   │       │   └── style.css
│   │       ├── icon
│   │       │   └── favicon.png
│   │       └── js
│   │           └── style.js
│   ├── templates
│   │   └── sample
│   │       ├── base_index.html
│   │       └── index.html
│   ├── tests
│   │   ├── __init__.py
│   │   └── tests.py
│   ├── urls.py
│   └── views.py
└── templates
    └── base.html
```

## Djangoプロジェクト環境のセットアップ

「sample」ディレクトリに移動し、「pyproject.toml」に設定済みのhatchコマンドをHatchの環境に作成します。

```console
$ cd sample

$ hatch env create

$ hatch env show
                      Standalone
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Name    ┃ Type    ┃ Dependencies  ┃ Scripts         ┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ default │ virtual │ coverage      │ cov             │
│         │         │               │ cov-report      │
│         │         │               │ createsuperuser │
│         │         │               │ makemigrations  │
│         │         │               │ migrate         │
│         │         │               │ runserver       │
│         │         │               │ shell           │
│         │         │               │ startapp        │
│         │         │               │ test            │
├─────────┼─────────┼───────────────┼─────────────────┤
│ lint    │ virtual │ black>=23.1.0 │ all             │
│         │         │ mypy>=1.0.0   │ style           │
│         │         │ ruff>=0.0.243 │ typing          │
└─────────┴─────────┴───────────────┴─────────────────┘
```

データベースの初期化、スーバーユーザーの作成、サーバーの起動は以下のように実行できます。

```console
$ hatch run migrate

$ hatch run createsuperuser

$ hatch run runserver
```

PyPIに公開されるパッケージの名前は「pyproject.toml」の「project」テーブルにある「name」キーとなります。

デフォルトではカスタムテンプレートを読み込んだ際の「アプリ名」になっています。PyPIにおいてパッケージの名前が被ってしまうと公開することができないので事前に確認しておきましょう。

```toml
# pyproject.toml

[project]
name = ["sample"]
# ...
```

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
django<=*.*.*
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

## デプロイ

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
include = ["sample/*"] # templatesとstaticも含まれます。
# exclude = ["sample/migrations/*"]
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

**作成中...**


## License

`django-on-hatch` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
