from flask import Flask, request, jsonify
import json

import utils
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv('.env')


@app.route('/capture-payload', methods=['POST'])
def capture_payload():

    try:
        request_payload = request.get_json()
        response_payload = utils.invoke_lambda(request_payload)
        utils.save_payload(request_payload, response_payload)
        return jsonify({'success': True, 'request_payload': json.dumps(request_payload), 'response_payload': response_payload})

    except Exception as e:
        return jsonify({'success': False, 'request_payload': None, 'response_payload': None, 'message': str(e)})
    

@app.route('/logs/<function_name>', methods=['GET'])
def get_lambda_logs(function_name):
    try:
        logs = utils.retrieve_lambda_logs(function_name)
        return jsonify({'success': True, 'logs': logs})
    except Exception as e:
        return jsonify({'success': True, 'logs': None, 'message': str(e)})



if __name__ == '__main__':
    app.run()
