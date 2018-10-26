from flask import Flask
from flask import request
import os
import socket
import sys
import json
import redis

import pprint
from functools import wraps

print("Test")
# Flask setup
app = Flask(__name__)

# Redis setup
redis_server = os.environ['REDIS']
try:
    if "REDIS_PWD" in os.environ:
        r = redis.StrictRedis(host=redis_server,
                        port=6379, 
                        password=os.environ['REDIS_PWD'])
    else:
        r = redis.Redis(redis_server)
    r.ping()
except redis.ConnectionError:
    exit('Failed to connect to Redis, terminating.')

# Prettyprint setup
pp = pprint.PrettyPrinter(depth = 4, indent=4)

# Flask decorators
def context(func):
    """Extact context header and pass to wrapped function"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        context = request.headers['draft-context']        
        if context == None:
            return "No context found"
        kwargs['context'] = context
        return func(*args, **kwargs)
    return decorated_function

@app.route('/')
def hello():
    return 'hello'

@app.route('/vote', methods=['POST', 'GET'])
@context
def vote(context):

    if request.method == 'POST':
        vote = request.get_json().get('vote')
        r.hincrby(context, vote)
        return "{}: {}".format(context, vote)
    else:
        return json.dumps({k.decode('utf-8'): v.decode('utf-8') for k,v in r.hgetall(context).items()})

@app.route('/clear', methods=['POST'])
@context
def clear(context):
    r.delete(context)
    return "Cleared: {}".format(context)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
