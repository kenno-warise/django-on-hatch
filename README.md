# django-on-hatch

[![PyPI - Version](https://img.shields.io/pypi/v/django-hatch.svg)](https://pypi.org/project/django-hatch)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-hatch.svg)](https://pypi.org/project/django-hatch)

このリポジトリは[Hatch](https://hatch.pypa.io/latest/)プロジェクトマネージャーを使ったDjangoのアプリ開発用テンプレートです。

Djangoの既存プロジェクトのディレクトリからDjangoのサブコマンドである「startapp」及び、オプションの「--template、--extension」を使用してDjangoアプリのカスタムテンプレートを読み込んでください。

無事にカスタムテンプレートが読み込まれると、Hatchプロジェクトマネージャーを使ったDjangoアプリの開発をスタートすることができます。

Hatchの使い方を知っているだけで、以下の事が容易に実行できます。

- CI/CD

-----

**目次**
- [インストール](#インストール)

- [設定（開発＆テスト）](#設定（開発＆テスト）)

- [Djangoプロジェクトに設定（開発）](#Djangoプロジェクトに設定（開発）)

- [Djangoプロジェクトに設定（テスト）](#Djangoプロジェクトに設定（テスト）)

- [License](#license)

## インストール

実行環境は「Windows Sybsystem for Linux 2」のUbuntuターミナルです。


Pythonの環境をセットアップします。

pyenvを使用してPython3.7の環境を作成した例。

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

...

[project]
...
# dynamic = ["version"]  # 動的のキーに対してコメントアウト
...
dependencies = ["Django"]  # 依存関係にDjangoを設定
```

「project」テーブルの「dynamic」キーと「dependencies」キーに対して変更を加えます。

Hatchコマンドを使ってDjangoプロジェクトを作成します。

```console
$ hatch run django-admin startproject config
```

次に「config」ディレクトリにDjangoアプリのカスタムテンプレートである「django-on-hatch」レポジトリを使ってDjangoアプリを作成します。

```console
$ hatch run django-admin startapp \
--template=https://github.com/kenno-warise/django-on-hatch/archive/main.zip \
--extension=py,toml,txt \
new_app \
config
```

「config」ディレクトリ内には「new_app」に適した開発環境が整えられています。

```
config
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

## 設定（開発＆テスト）

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

言語を設定します。

`myproject/settings.py`

```python
# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True
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
cov = "coverage run \
  --include=new_app/* \
  --omit=new_app/test*,new_app/__init__.py,new_app/migrations/* \
  manage.py test {args}"
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

## Djangoプロジェクトに設定（開発）

Djangoアプリを作成

```console
$ hatch run startapp app_2
```

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

## Djangoプロジェクトに設定（テスト）

アップロード済みのDjangoアプリを設定します。

`myproject/settings.py`

`new_app`の部分をDjangoアプリ名に当てはめます。

```python
INSTALLED_APPS = [
    ...,
    "new_app",
]
```

`myproject/urls.py`

`new_app`の部分をDjangoアプリ名に当てはめます。

```python
...
from django.urls import path, include

urlpatterns = [
    ...,
    path('', include('new_app.urls')),
]
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
