# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except
# in compliance with the License. A copy of the License is located at
#
# https://aws.amazon.com/apache-2-0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
"The Flask application"
from flask import Flask, jsonify, render_template, request

import logic

application = Flask(__name__)

@application.route("/")
def home():
    "The home route"
    return render_template('main.html')

@application.route('/api/v1.0/get_challenge', methods=['GET'])
def get_challenge():
    "The get a set of questions"
    return jsonify(logic.get_challenge())

@application.route('/api/v1.0/get_route_miles', methods=['POST'])
def get_route_miles():
    "Get the display answer"
    data = request.get_json()
    data["1"]["Miles"] = logic.get_route_miles(data["1"]['Route'])
    data["2"]["Miles"] = logic.get_route_miles(data["2"]['Route'])
    return jsonify(data)

if __name__ == "__main__": # pragma: no cover
    application.run(debug=True, host='0.0.0.0', port=8080)
