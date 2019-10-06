# forked "simple-websockets-app-py"

## �{�v���O�����ɂ���

### ���L����R�s�[�������̂���ɋ@�\�ǉ����܂����i2019/10/06�j

<https://github.com/kumapo/simple-websockets-app-py>	

#### �ǉ��@�\
- �C���X�g�[�����̃��[�g�����ݒ�Ɗ֘A�t��
- �g���K�p�f�[�^�i��M�j��value��ǉ�	
	���� `{"action":"sendmessage", "value":36.5}`
- �v�b�V���ʒm�f�[�^�i���M�j��JSON��

#### ���s����
		wscat -c wss://**********.execute-api.us-west-2.amazonaws.com/prod	
		connected (press CTRL+C to quit)	
		
		> {"action":"sendmessage", "data":"hello world!"}	
		< {"type": "message", "data": "hello world!"}	
		
		> {"action":"sendmessage", "value":36.5}	
		< {"type": "message", "value": 36.5}	

### �g�p���@�Ȃǂ̏ڍׂ͌���ҁikumapo�l�j�����J���Ă��鉺�L�̏����Q�Ƃ�������

websocket APIs with API Gateway and Lambda running on Python3	
<https://qiita.com/kumapo/items/6b65b468b9d3d6884cbb>	
	
## ���C�Z���X

�����Ƃ��� MIT���C�Z���X�Ƃ��܂����A���C�Z���X�`�Ԃ��܂߁A�⏞�͂���܂���B	

		JavaScript�ŁF	
		modified MIT License	
		Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.	
		https://github.com/aws-samples/simple-websockets-chat-app
		
		Python��(fork��)�F	
		���C�Z���X�\���Ȃ�	
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

�ȏ� forked by Wataru KUNINO	
	
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
