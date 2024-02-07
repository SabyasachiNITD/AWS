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
        response = getUser(event['queryStringParameters']['userId'])
    elif httpMethod == post:
        response = saveUser(json.loads(event['body']))
    elif httpMethod == patch:
        response = updateUser(requestBody['userId'],requestBody['updateKey'],requestBody['updateValue'])
    elif httpMethod == delete:
        response = deleteUser(requestBody['userId'])
    else:
        response = buildResponse(404,'Not Found')

    return response

def getUser(userId):
    try:
        response = table.get_item(Key= {'userId':userId})
        if 'Item' in response:
            return buildResponse(200,response['Item'])
        else:
            return buildResponse(404,{'message' : 'userId %s not found'} %userId)
    except:
        logger.exception("Unknown error while fetching")

def saveUser(requestBody):
    try:
        table.put_item(Item=requestBody)
        body = {
            'Operation' : 'CREATE',
            'Message' : 'SUCCESS',
            'Item' : requestBody
        }
        return buildResponse(200,body)
    except:
        logger.exception("Unknown error while creating item")

def updateUser(userId,updateKey,updateValue):
    try:
        response = table.update_item(
            Key = {
                'userId' : userId
            },
            UpdateExpression = 'SET %s = :val1' %updateKey,
            ExpressionAttributeValues = {
                ':val1' : updateValue
            },
            ReturnValues = 'UPDATED_NEW'
        )
        body = {
            'Operation' : 'UPDATE',
            'Message' : 'SUCCESS',
            'UpdatedAttributes' : response
        }
        return buildResponse(200,body)
    except:
        logger.exception('Unknown Error while Updating')

def deleteUser(userId):
    try:
        response = table.delete_item(
            Key = {
                'userId' : userId
            },
            ReturnValues = 'ALL_OLD'
        )
        body = {
            'Operation': 'UPDATE',
            'Message': 'SUCCESS',
            'UpdatedAttributes': response
        }

        return buildResponse(200,body)
    except:
        logger.exception("Unknown error while deleting")
def buildResponse(statusCode,body=None):
    response = {
        'statusCode' : statusCode,
        'headers' : {
            'Content-Type' : 'application/json',
            'Access-Control-Allow-Origin' : '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body)
    return response



