#!/usr/bin/env python3
# coding: utf-8

# WebSocketを受信する
# Copyright (c) 2019 Wataru KUNINO

################################################################################
# 下記のライブラリが必要です
# sudo pip3 install websocket-client

API_ID = '**********'                                   # AWS API Gatewayで取得
REGION = 'us-west-2'                                    # AWSのリージョン
STAGE  = 'Prod'                                         # デプロイ時のステージ名
keys = ['type','sockets','total','data','value','device','url']     # 受信項目名

import websocket                                        # WebSocketライブラリ
import datetime                                         # 日時ライブラリ
import urllib.request                                   # HTTP通信ライブラリ
import json                                             # JSON変換ライブラリ

if API_ID == '**********':                              # 設定値のダウンロード
    res = urllib.request.urlopen('https://bokunimo.net/iot/cq/test_ws_aws.json')
    res_dict = json.loads(res.read().decode().strip())  # 設定値を辞書型変数へ
    API_ID = res_dict.get('api_id')                     # AWS API GatewayのID
    REGION = res_dict.get('region')                     # AWSのリージョン
    STAGE  = res_dict.get('stage')                      # デプロイ時のステージ名
    res.close()                                         # HTTPリクエスト終了

print('WebSocket Logger')                               # タイトル表示
url = 'wss://' + API_ID + '.execute-api.' + REGION + '.amazonaws.com/' + STAGE
print('Listening,',url)                                 # URL表示

try:
    sock = websocket.create_connection(url)             # ソケットを作成
except Exception as e:                                  # 例外処理発生時
    print(e)                                            # エラー内容を表示
    exit()                                              # プログラムの終了
while sock:                                             # 作成に成功したとき
    try:
        payload = sock.recv().strip()                   # WebSocketを取得
    except websocket.WebSocketConnectionClosedException as e:
        sock.close()                                    # ソケットの切断
        break                                           # while sockを抜ける
    date = datetime.datetime.today()                    # 日付を取得
    print(date.strftime('%Y/%m/%d %H:%M'), end='')      # 日付を出力
    try:
        res_dict = json.loads(payload)                  # 辞書型変数へ代入
    except Exception:
        if len(payload) > 0 and payload.isprintable():
            print(',', payload)                         # 受信データを出力
        else:
            print(', (null)')
        continue                                        # whileの先頭に戻る
    key_F = False
    for key in keys:                                    # 受信項目を繰り返し処理
        val = res_dict.get(key)                         # 辞書型変数から索引検索
        if val is not None:                             # 指定項目がある時
            val = str(val).strip()                      # 文字列変換と両端処理
            print(',', key, '=', val, end='')           # 値を表示
            key_F = True
    if key_F:
        print()                                             # 改行
    else:
        print(', (null)')
