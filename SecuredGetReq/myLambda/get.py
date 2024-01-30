import json

def lambda_handler(event,context):
    x = event['queryParameters']['x']
    y = event['queryParameters']['y']

    ans = add(x,y)
    print(f'sum of {x} and {y} is = {ans}')

    result = {}
    result['x'] = int(x)
    result['y'] = int(y)
    result['sum'] = ans


    #preparing the response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(result)

    return responseObject

def add(x,y):
    return int(x) + int(y)