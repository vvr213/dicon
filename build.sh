#!/usr/bin/env bash
#エラーが起きたら即停止する設定
set -o errexit

#1.ライブラリのインストール
pip install -r requirements.txt

#2.静的ファイルの収集（css等をstaticfiles フォルダに集める）
python manage.py collectstatic --no-input

#3.データベースのマイグレーション（本番DBにテーブル作成）
python manage.py migrate