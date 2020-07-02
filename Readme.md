# NANE
Various Function Application(開発環境)

# DEMO
ss画像

# Features
ECとSNSの機能をもつアプリです。
## 機能一覧
EC
・商品の出品
・商品の購入（今すぐ購入orカートに入れて購入）
・商品の平均評価の表示
・自身が出品した商品が購入されたらメールでお知らせ
・購入履歴の表示

SNS
・一般記事の投稿
・商品評価記事の投稿（購入済みの商品に対して数値+文字）
・商品評価記事のリンクから対象商品が購入された時、商品の値段の１％を記事投稿者に付与

共通
・ユーザー登録（ログイン機能）
・パスワードの再設定
・郵便番号で住所検索
・検索（文字で絞り込み、友人で絞り込み）
・お気に入り登録
・他ユーザーを友人登録
・連続ログインでポイント付与（連続ログイン日数×100point、連続ログインが途切れた場合一日目からスタート）
・ポイント増減の履歴を表示
・アンケート（このアプリの評価を数値と文字列で入力し、送信　→　開発者のメールアドレスに届く）

その他
・djangorestframeworkを用いて商品情報と記事情報をAPIで公開
・上記APIを用いてVue.jsで非同期処理（お気に入りのON,OFF、商品評価値の表示など）
・レスポンシブデザイン

# Requirement
* python 3.6.8
* django 2.2.12
* nginx 1.16
* uwsgi 2.0.18 
* mysql 5.7
* mysqlclient 1.4.6
* django-bootstrap4 1.1.1
* django-cleanup 3.2.0
* django-filter 2.2.0
* djangorestframework 3.11.0
* pillow 7.0.0
* requests 2.23.0

# Usage
‵$ clone‵
‵$ docker-compose build‵
‵$ docker-compose run python ./manage.py migrate‵
‵$ docker-compose run python ./manage.py collectstatic‵
‵$ docker-compose up -d‵
http://localhost:8000


# Note
CDNを利用しているので、ネット環境がない場合デザインが崩れます。

# Author
* 稲見駿太郎
* juntailangdaojian4@gmail.com

# License
