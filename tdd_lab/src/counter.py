
"""
Counter API Implementation
"""
# from flask import Flask
from flask import Flask, jsonify
from . import status

app = Flask(__name__)


from flask import Flask, jsonify
from . import status  # Notice the dot for relative import
"""
Counter API Implementation
"""
from flask import Flask

app = Flask(__name__) 

COUNTERS = {}

def counter_exists(name):
  """Check if counter exists"""
  return name in COUNTERS

@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
  """Create a counter"""
  if counter_exists(name):
      return jsonify({"error": f"Counter {name} already exists"}), status.HTTP_409_CONFLICT
  COUNTERS[name] = 0

  return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED

  return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED

# ===========================
# Feature: Increment Counter (PUT/counter/<name>) / Check if non-existent
# Author: Ashley Arellano / Charles Ballesteros
# Date: 2025-02-03
# Description: Increments the value of a given counter, checks 
# and marks HTTP response as 404 (method not found) if
# the counter does not exist. Otherwise, it marks HTTP response as 200 (OK).
# ===========================
@app.route('/counters/<name>', methods=['PUT'])
def increment_counter(name):
  #Checks if the counter to be incremented exists
  if not counter_exists(name):
    #Counter does not exist, HTTP response is 405
    return jsonify({"error": f"Counter {name} does not exist. Unable to increment."}), status.HTTP_404_NOT_FOUND
  #Counter exists, increment counter and return 200 as HTTP response
  COUNTERS[name] += 1
  return jsonify({name: COUNTERS[name]}),status.HTTP_200_OK

# TODO 3: i will do this later 
# - i will do this later 
# ===========================
# Test: Retrieve an existing counter
# Author: [Abdulrahman Alharbi]
# Date: [02.03.2025]
# Description: i will do this later 
# ===========================
@app.route('/counters/<name>', methods=['GET'])
def get_counter(name):
    """Retrieve an existing counter"""
    if name in COUNTERS:
        return jsonify({name: COUNTERS[name]}), 200
    return jsonify({"error": "Counter not found"}), 404



@app.route('/counters/<name>', methods=['DELETE'])
def delete_counter(name):
  """Delete a counter"""
  if not counter_exists(name):
      return jsonify({"error": f"Counter {name} not found"}), status.HTTP_404_NOT_FOUND
  del COUNTERS[name]
  return '', status.HTTP_204_NO_CONTENT

