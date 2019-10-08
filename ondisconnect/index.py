import json
import os
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
dbTable = dynamodb.Table(os.environ['TABLE_NAME'])

error_forbidden = { 'statusCode': '403', 'body': 'Forbidden' }
error_internal  = { 'statusCode': '500', 'body': 'Internal server error' }

def lambda_handler(event, context):
    logger.info("ondisconnect: %s" % event)

    requestContext = event.get('requestContext',{})
    connection_id = requestContext.get('connectionId')
    request_id     = requestContext.get('requestId')
    if (connection_id is None) or (request_id is None):
        logger.error('connection id is None')
        return error_forbidden

    result = dbTable.delete_item(Key={ 'id': connection_id })
    if result.get('ResponseMetadata',{}).get('HTTPStatusCode') != 200:
        logger.warning('db, delete_item failed: %s' % result)
        return error_internal
    return { 'statusCode': 200, 'body': 'ok' }
