from flask import Flask, request, jsonify
import json

import utils


app = Flask(__name__)


@app.route('/capture-payload', methods=['POST'])
def capture_payload():

    try:
        request_payload = request.get_json()
        response_payload = utils.invoke_lambda(request_payload)
        utils.save_payload(request_payload, response_payload)
        return jsonify({'success': True, 'request_payload': json.dumps(request_payload), 'response_payload': response_payload})

    except Exception as e:
        return jsonify({'success': False, 'request_payload': None, 'response_payload': None, 'message': str(e)})



if __name__ == '__main__':
    app.run()
