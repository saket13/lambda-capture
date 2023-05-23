import json
import os
from core.aws import AWS_Utils

lambda_client = AWS_Utils(service_name='lambda').get_service_client_instance()
cloudwatch_logs_client = AWS_Utils(service_name='logs').get_service_client_instance()

def invoke_lambda(request_payload):
    function_name = os.getenv('TARGET_LAMBDA_FUNCTION_NAME')
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',
        Payload=json.dumps(request_payload)
    )
    response_payload = response['Payload'].read().decode('utf-8')
    return response_payload


def retrieve_lambda_logs(function_name):
    log_group_name = '/aws/lambda/' + function_name
    response = cloudwatch_logs_client.describe_log_streams(
        logGroupName=log_group_name
    )

    log_streams = response['logStreams']
    logs = []

    # Iterate over each log stream and retrieve its log events
    for stream in log_streams:
        log_stream_name = stream['logStreamName']
        response = cloudwatch_logs_client.get_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name
        )
        log_events = response['events']
        for event in log_events:
            log_message = event['message']
            if 'request-payload' not in log_message or 'response-payload' not in log_message:
                continue
            formatted_data = format_log_message(log_message)
            logs.append(formatted_data)
    return logs

def format_log_message(log_entry):
	json_start_index = log_entry.find("{")
	json_end_index = log_entry.rfind("}") + 1
	json_string = log_entry[json_start_index:json_end_index]
	
	# Parse the JSON string
	try:
		log_data = json.loads(json_string)
	except json.JSONDecodeError as e:
		print("Failed to parse JSON:", e)
		exit(1)
	
	# Format the data
	formatted_data = {
		'Request ID': log_data['request-id'],
		'Request Payload': json.loads(log_data['request-payload']),
		'Response Payload': log_data['response-payload'],
		'Time-Epoch': log_data['time-epoch']
	}
	return formatted_data


def save_payload(request_payload, response_payload):
    with open('payload.log', 'a') as f:
        f.write(f'Request Payload: {json.dumps(request_payload)}\n')
        f.write(f'Response Payload: {response_payload}\n')