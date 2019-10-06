# forked "simple-websockets-app-py"

## 本プログラムについて

### 下記からコピーしたものを基に機能追加しました（2019/10/06）

<https://github.com/kumapo/simple-websockets-app-py>	

#### 追加機能
- インストール時のルート自動設定と関連付け
- トリガ用データ（受信）にvalueを追加	
	入力 `{"action":"sendmessage", "value":36.5}`
- プッシュ通知データ（送信）のJSON化

#### 実行結果
		wscat -c wss://**********.execute-api.us-west-2.amazonaws.com/prod	
		connected (press CTRL+C to quit)	
		
		> {"action":"sendmessage", "data":"hello world!"}	
		< {"type": "message", "data": "hello world!"}	
		
		> {"action":"sendmessage", "value":36.5}	
		< {"type": "message", "value": 36.5}	

### 使用方法などの詳細は原作者（kumapo様）が公開している下記の情報を参照ください

websocket APIs with API Gateway and Lambda running on Python3	
<https://qiita.com/kumapo/items/6b65b468b9d3d6884cbb>	
	
## ライセンス

原則として MITライセンスとしますが、ライセンス形態を含め、補償はありません。	

		JavaScript版：	
		modified MIT License	
		Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.	
		https://github.com/aws-samples/simple-websockets-chat-app
		
		Python版(fork元)：	
		ライセンス表示なし	
		https://github.com/kumapo/simple-websockets-app-py

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

以上 forked by Wataru KUNINO	
	
--------------------------------------------------------------------------------
## Deployment

- Install python packages
- `aws s3 mb s3://simple-websockets-app-py`
- `sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket s3://simple-websockets-app-py`
- `aws cloudformation deploy --template-file packaged.yaml --stack-name simple-websockets-app-py --capabilities CAPABILITY_IAM`
- ~~Ensure that each lambda is tied to the corresponding route for API Gateway~~
- Deploy the APIs for `prod`
- Press 'Save Changes' on the stage prod page

## Connecting via websocket

- Install node modules
- `wscat -c wss://{API-ID}.execute-api.{REGION}.amazonaws.com/prod`
- Type `{"action":"sendmessage", "data":"hello world!"}`

added by Wataru
- Type `{"action":"sendmessage", "value":36.5}`
