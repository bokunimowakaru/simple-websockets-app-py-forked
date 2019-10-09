import json
import os
import logging
import boto3
import botocore

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb = boto3.resource('dynamodb')
dbTable = dynamodb.Table(os.environ['TABLE_NAME'])

# WebSocket 応答・送信用
def ws_send(url, id, data):
    post_data = json.dumps(data).encode()
    logger.info('ws_send: %s' % post_data)
    apigw_management = boto3.client('apigatewaymanagementapi', endpoint_url=url)
    try:
        apigw_management.post_to_connection(ConnectionId = id, Data = post_data)
    except botocore.exceptions.ClientError as e:
        logger.warning('Exception, post_to_connection: %s' % e)
        ret = int(e.response.get('ResponseMetadata',{}).get('HTTPStatusCode'))
        return ret
    return 200

# WebSocket 受信用ハンドラ
def lambda_handler(event, context):
    logger.info("sendmessage: %s" % event)
    requestContext = event.get('requestContext',{})
    connection_id  = requestContext.get('connectionId')
    request_id     = requestContext.get('requestId')
    domain_name    = requestContext.get('domainName')
    stage          = requestContext.get('stage')
    url = 'https://' + domain_name + '/' + stage
    ok_dict ={'statusCode': 200}
    err_dict={"message":"Forbidden","connectionId":connection_id,"requestId":request_id}

    # 受信データbodyを辞書型に変換する
    body = str(event.get('body', '{}').strip())
    if (not body.isprintable()) or (domain_name is None) or (stage is None):
        logger.error('json, not printable, or no url')
        ws_send(url, connection_id, err_dict) # error_bad_request
        return ok_dict
    try:
        body = json.loads( body )
    except Exception as e:
        logger.error('Exception, json.loads: %s' % e)
        ws_send(url, connection_id, err_dict) # error_bad_request
        return ok_dict
        
    # 応答データ data_dict を作成する
    data_dict = {"type": "message"}
    data = body.get('data')
    if (type(data) is str) and (data.isprintable()):
        data_dict.update( {"data": data } )
    data = body.get('value')
    if (type(data) is float) or type(data) is int:
        data_dict.update( {"value": data } )
    data = body.get('device')
    if (type(data) is str) and (data.isprintable()):
        if len(data) == 7 and data[5] == '_':
            data_dict.update( {"device": data } )

    # WebSocket接続中の機器をDBから読み込み、全機器へメッセージを送信する
    items = dbTable.scan(ProjectionExpression='id').get('Items')
    if items is not None:
        for item in items:
            ret = ws_send(url,item['id'],data_dict)
            if ret == 410:
                dbTable.delete_item(Key={'id': item['id']})
                logger.warning('removed from dbTable: %s ' % item['id'])
    return ok_dict
