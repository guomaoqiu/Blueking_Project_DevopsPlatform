from flask import Flask
import json
app = Flask(__name__)
@app.route('/get_flask_content/',methods=['POST','GET'])
def get_flask_content():
  return json.dumps({
        "result" : True,
        "code": 0,
        "data": 'esb_test',
        "extmsg": '',
        "content": "I'm from flask api..."
    })
app.run(host='192.168.1.200')
