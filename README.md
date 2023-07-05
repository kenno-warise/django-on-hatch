# django-on-hatch

[![PyPI - Version](https://img.shields.io/pypi/v/django-hatch.svg)](https://pypi.org/project/django-hatch)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-hatch.svg)](https://pypi.org/project/django-hatch)

-----

**目次**

- [詳細](#詳細)
- [インストール](#インストール)
- [設定（開発＆テスト）](#設定)
- [Djangoプロジェクトに設定（開発）](#Djangoプロジェクトに設定（開発）)
- [Djangoプロジェクトに設定（テスト）](#Djangoプロジェクトに設定（テスト）)
- [実行](#実行)
- [License](#license)

## 詳細

このリポジトリは[Hatch](https://hatch.pypa.io/latest/)プロジェクトマネージャーを使ったDjangoプロジェクトの開発またはテスト（お試し）ツールです。

配布用としてDjangoアプリをアップロードする環境を自動構築または配布用としてアップロードされたDjangoアプリをこのDjangoプロジェクトに組み込んでテストすることができます。

使用方法は以下からご覧ください。

## インストール

実行環境は「Windows Sybsystem for Linux 2」のUbuntuです。

Pythonの環境は任意です。

私はpyenvを使用してPython3.10の環境を設定しています。

```console
$ pyenv local 3.10

$ python3 --version
Python 3.10.0
```

仮想環境を作成して有効にし、`Hatch`をインストールします。

```console
$ python3 -m venv .venv && . .venv/bin/activate

$ pip install --upgrade pip

$ pip install hatch
```

リポジトリを落とします。

```console
$ git clone https://github.com/kenno-warise/django-on-hatch.git

$ cd django-on-hatch
```

## 設定（開発＆テスト）

Hatchの仮想環境名を作成する。

```console
$ hatch new --init 仮想環境名（プロジェクト名）
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

Hatch仮想環境にインストールされるDjangoは設定されていますが、バージョンを指定したい場合は以下を編集してください。

`pyproject.toml`

```toml
# デフォルト環境の依存パッケージ
[tool.hatch.envs.default]
dependencies = ["django == 4.2.2"]
```

Djangoプロジェクトを作成

```console
$ hatch run django-admin startproject myproject .
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
$ hatch run python3 manage.py startapp app_1
```

バージョン情報の設定

`pyproject.toml`

```toml
[tool.hatch.version]
path = "app_1/__init__.py"
```

`app_1/__init__.py`

```python
__version__ = "0.0.1"
```

Hatchの「version」コマンドでDjangoアプリのバージョン情報を確認できます。

```console
$ hatch version
0.0.1
```

DjangoアプリをパッケージングしてPyPIにアップロードする。

`pyproject.toml`に配布するファイルと配布しないファイルを設定。

```toml
[tool.hatch.build]
include = ["app_1/*"] # templatesとstaticも含まれます。
exclude = ["app_1/migrations/*"]
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

`app_1`の部分をDjangoアプリ名に当てはめます。

```python
INSTALLED_APPS = [
    ...,
    "app_1",
]
```

`myproject/urls.py`

`app_1`の部分をDjangoアプリ名に当てはめます。

```python
...
from django.urls import path, include

urlpatterns = [
    ...,
    path('', include('app_1.urls')),
]
```

`pyproject.toml`

`app_1`の部分をDjangoアプリ名に当てはめます。

```toml
# デフォルト環境の依存パッケージ
[tool.hatch.envs.default]
dependencies = ["django", "app_1"]
```

Djangoのコマンドは「tool.hatch.envs.default.scripts」テーブルによって登録しています。

```toml
[tool.hatch.envs.default.scripts]
makemigrations = "python3 manage.py makemigrations {args}"
migrate = "python3 manage.py migrate"
createsuperuser = "python3 manage.py createsuperuser"
runserver = "python3 manage.py runserver"
startapp = "python3 manage.py startapp {args}"
test = "python3 manage.py test {args}"
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
