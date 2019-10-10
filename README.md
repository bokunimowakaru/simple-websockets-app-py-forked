# forked "simple-websockets-app-py"

## 本プログラムについて

AWS上で動作するWebSocketサーバのサンプル・プログラムです。		
遠隔地のIoTセンサが送信したセンサ値を、別宅でリアルタイムに受信するときなどに使用することが出来ます。		

### 下記からコピーしたものを基に機能追加しました（2019/10/06）

<https://github.com/kumapo/simple-websockets-app-py>	

#### 追加機能
- インストール時のルート自動設定と関連付け	
- トリガ用データ（受信）にvalue、deviceを追加	
	- 入力 `{"action":"sendmessage", "value":3.14}`	
	- 入力 `{"action":"sendmessage", "value":-273.15, "device":"sensr_0"}`	
- プッシュ通知データ（送信）のJSON化	

#### 実行結果
		wscat -c wss://**********.execute-api.us-west-2.amazonaws.com/prod	
		connected (press CTRL+C to quit)	
		
		> {"action":"sendmessage", "data":"hello world!"}	
		< {"type": "message", "data": "hello world!"}	
		
		> {"action":"sendmessage", "value":3.14}	
		< {"type": "message", "value": 3.14}	

		> {"action":"sendmessage", "value":365}	
		< {"type": "message", "value": 365}	

		> {"action":"sendmessage", "device":"sensr_0"}	
		< {"type": "message", "device": "sensr_0"}	

		> {"action":"sendmessage", "data":"mixed", "value":-273.15, "device":"sensr_0"}
		< {"type": "message", "data": "mixed", "value": -273.15, "device": "sensr_0"}

### 使用方法

本README内の「デプロイ方法 Deployment」および、「WebSocket接続方法 Connecting via websocket」に概要を説明しています。  
下記のサイトも参照の上、ご利用ください。

- Raspberry PiへAWS SAM CLIをインストールする方法：		
<https://bokunimo.net/blog/raspberry-pi/596/>		

- WebSocket Chat (JavaScript版)をインストールする方法：		
<https://bokunimo.net/blog/raspberry-pi/605/>		

- 原作者（kumapo様）が公開している情報：  	
websocket APIs with API Gateway and Lambda running on Python3		
<https://qiita.com/kumapo/items/6b65b468b9d3d6884cbb>		
	
## その他の参考情報

AWS Documentationの中には、最新（2019/07/29版）のサンプル・コードがあり、本格的に始めたい場合に参考になると思います。ただし、コード量が多いので、実験や試用の段階では、本ブランチ等のサンプルの方が手軽です。

<https://docs.aws.amazon.com/ja_jp/code-samples/latest/catalog/code-catalog-python-example_code-apigateway-websocket.html>

### システム応用例
簡単な応用例として、IoT向け通知メッセージ受信の確認用サンプル ws_aws_example.py を作成しました。  
本スクリプト実行すると、以下の処理を行います。  

- サンプルのWebSocketサーバに接続情報を、筆者のウェブサイトからHTTP GETで取得します。
- 受信したapi_id、region、stageを使ってWebSocket接続を行います。
- WebSocketサーバから受信した以下のようなデータを表示します。
	- 2分間隔で送られてくる、keepalive信号を表示します
	- 20分間隔で送られてくる遠隔地の室温をデータ（value = xx.x）を表示します
	- 同サーバに誰かが接続したときに現在のWebSocket接続数（sockets = x）を表示します

- 2時間後に停止します。[Ctrl]＋[C]の操作で停止させることも出来ます

		2019/10/06 08:32, type = keepalive, sockets = 1	
		2019/10/06 08:34, type = keepalive, sockets = 1	
		2019/10/06 08:36, type = keepalive, sockets = 1	
		2019/10/06 08:37, type = notify, sockets = 2, total = 81	
		2019/10/06 08:38, type = keepalive, sockets = 2	
		2019/10/06 08:40, type = keepalive, sockets = 2	
		2019/10/06 08:40, type = message, value = 29.5	

- ご注意とお願い	
		自動でWebSocket接続を繰り返したり、複数の接続を行うことを禁止します。  
		目的をご理解の上、節度を持ってご利用ください。  

- サンプル・ソフトウェア（クライアント側）		
<https://github.com/bokunimowakaru/simple-websockets-app-py-forked/blob/master/ws_aws_example.py>		

--------------------------------------------------------------------------------
## デプロイ方法 Deployment

- Install python packages
- `aws s3 mb s3://simple-websockets-app-py`
- `sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket s3://simple-websockets-app-py`
- `aws cloudformation deploy --template-file packaged.yaml --stack-name simple-websockets-app-py --capabilities CAPABILITY_IAM`
- ~~Ensure that each lambda is tied to the corresponding route for API Gateway~~
- Deploy the APIs for `prod`
- Press 'Save Changes' on the stage prod page

## WebSocket接続方法 Connecting via websocket

- Install node modules
- `wscat -c wss://{API-ID}.execute-api.{REGION}.amazonaws.com/prod`
- Type `{"action":"sendmessage", "data":"hello world!"}`
- Type `{"action":"sendmessage", "value":365}` (追加機能)

--------------------------------------------------------------------------------
## ライセンス

原則として MITライセンスとしますが、fork元のライセンスが明記されていません。JavaScript版がMITライセンスを基にしているので、同ライセンスを引き継いでいるものと考えられます。		
※ライセンス形態を含め、一切の補償をいたしません。	

		本バージョン	
		下記のライセンスからの変更点については国野亘が著作権を保有します	
		ライセンス形態はMITライセンスを基本としますが、下記の作成物の	
		権利については、それぞれのライセンスにしたがって下さい。	
		
		Python版(fork元)：	
		ライセンス表示なし	
		https://github.com/kumapo/simple-websockets-app-py
		
		JavaScript版：	
		modified MIT License	
		Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.	
		https://github.com/aws-samples/simple-websockets-chat-app
		
Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

