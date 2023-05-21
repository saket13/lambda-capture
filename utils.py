import boto3
import json
import os

def invoke_lambda(request_payload):
    lambda_client = boto3.client('lambda')
    function_name = os.getenv('TARGET_LAMBDA_FUNCTION_NAME')
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',
        Payload=json.dumps(request_payload)
    )
    response_payload = response['Payload'].read().decode('utf-8')
    return response_payload


def save_payload(request_payload, response_payload):
    with open('payload.log', 'a') as f:
        f.write(f'Request Payload: {json.dumps(request_payload)}\n')
        f.write(f'Response Payload: {response_payload}\n')