import json
import os
import logging
import boto3
import botocore

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
dbTable = dynamodb.Table(os.environ['TABLE_NAME'])

def ws_send(url, id, data):
    post_data = None
    apigw_management = boto3.client('apigatewaymanagementapi', endpoint_url=url)
    if type(data) is dict:
        post_data = json.dumps(data)
    if type(data) is str:
        post_data = data
    if post_data is None:
        logger.warning('ws_send, invalid data: %s' % type(data))
        return 500
    logger.info('ws_send: %s' % post_data)
    try:
        _ = apigw_management.post_to_connection(ConnectionId = id, Data = post_data)
    except botocore.exceptions.ClientError as e:
        logger.warning('Exception, post_to_connection: %s' % e)
        return int(e.response.get('ResponseMetadata',{}).get('HTTPStatusCode'))
    return 200

def lambda_handler(event, context):
    logger.info("sendmessage: %s" % event)

    requestContext = event.get('requestContext',{})
    connection_id  = requestContext.get('connectionId')
    request_id     = requestContext.get('requestId')
    domain_name    = requestContext.get('domainName')
    stage          = requestContext.get('stage')

    url = 'https://' + domain_name + '/' + stage
    ok_dict = { 'statusCode': 200 }
    error_s = '{"message": "Forbidden", "connectionId":"' + connection_id + '", "requestId":"' + request_id + '"}'
    err_i_s = '{"message": "Internal server error", "connectionId":"' + connection_id + '", "requestId":"' + request_id + '"}'

    try:
        body = json.loads( event.get('body', '{}') )
    except Exception as e:
        logger.error('Exception, json.loads: %s' % e)
        ws_send(url, connection_id, error_s) # error_bad_request
        return ok_dict

    if body is None:
        logger.error('json.loads, body is None')
        ws_send(url, connection_id, error_s) # error_bad_request
        return ok_dict
        
    data_dict = {"type": "message"}

    data = body.get('data')
    if (type(data) is str) and (data.isprintable()):
        data_dict.update( {"data": data } )

    data = body.get('value')
    if type(data) is float:
        data_dict.update( {"value": data } )
    if type(data) is int:
        data_dict.update( {"value": data } )

    data = body.get('device')
    if (type(data) is str) and (data.isprintable()):
        if len(data) == 7 and data[5] == '_':
            data_dict.update( {"device": data } )

    if len(data_dict) < 2:
        logger.error('json.loads, no valied keys')
        ws_send(url, connection_id, error_s) # error_bad_request
        return ok_dict

    if (domain_name is None) or (stage is None):
        logger.error('"domain name" or "stage" is None ')
        ws_send(url, connection_id, error_s) # error_bad_request
        return ok_dict

    items = dbTable.scan(ProjectionExpression='id').get('Items')
    if items is None:
        logger.error('no dbTable')
        ws_send(url, connection_id, err_i_s) # error_internal
        return ok_dict

    for item in items:
        ret = ws_send(url,item['id'],data_dict)
        if ret != 200:
            if ret == 410:
                dbTable.delete_item(Key={'id': item['id']})
                logger.warning('post_to_connection skipped: %s removed from dbTable' % item['id'])
            else:
                logger.warning('post_to_connection failed: %d' % ret)
    return ok_dict
