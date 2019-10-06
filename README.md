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
