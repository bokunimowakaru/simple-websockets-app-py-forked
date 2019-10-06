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
