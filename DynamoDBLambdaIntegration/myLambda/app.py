import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

table_name = 'table-dynamodb-crud'
dynamoDB = boto3.resource('dynamodb')
table = dynamoDB.Table(table_name)

get = 'GET'
post = 'POST'
patch = 'PATCH'
delete = 'DELETE'

def lambda_handler(event,context):
    logger.info(event)
    httpMethod = event['httpMethod']
    requestBody = json.loads(event['body'])
    if httpMethod == get:
        response = getUserId(event['queryStringParameters']['userId'])
    elif httpMethod == post:
        response = saveUserId(json.loads(event['body']))
    elif httpMethod == patch:
        response = updateUserId(requestBody['userId'],requestBody['updateKey'],requestBody['updateValue'])
    elif httpMethod == delete:
        response = deleteUserId(requestBody['userId'])
    else:
        response = buildResponse(404,'Not Found')

    return response

def getUserId(userId):
    try:
        response = table.get_item(Key= {'userId':userId})
    if 'Item' in response:
        return bu


