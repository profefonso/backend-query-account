import os
import boto3
from flask import Flask, request, jsonify

app = Flask(__name__)

client = boto3.client('dynamodb', region_name='us-east-1')
tableName = 'clientMoneyTable'

#Index
@app.route("/")
def index():
    return "This is the app index"

#Add client and money
@app.route("/add")
def add_client():
    name=request.args.get('name')
    money=request.args.get('money')
    try:
        if not name or not money:
            return jsonify({'error': 'Please add name of client and Virtual money value'}), 400
        
        resp = client.put_item(
            TableName=tableName,
            Item = {
                'name': {'S': name },
                'money': {'S': money }
            }
        )

        return jsonify({
            'name': name,
            'money': money
        })
    except Exception as e:
	    return(str(e))

'''
#Get all clients
@app.route("/getall")
def get_all():
    change
    try:
        clients=Client.query.all()
        return  jsonify([e.serialize() for e in clients])
    except Exception as e:
	    return(str(e))

#Get client by ID
@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        client=Client.query.filter_by(id=id_).first()
        return jsonify(client.serialize())
    except Exception as e:
	    return(str(e))
'''
#Get client by Name
@app.route("/getn/<name_>")
def get_by_name(name_):
    try:
        resp = client.get_item(
            TableName=tableName,
            Key={
                'name': { 'S': name_ }
            }
        )
        item = resp.get('Item')
        if not item:
            return jsonify({'error': 'Client does not exist'}), 404

        return jsonify({
            'client': item.get('client').get('S'),
            'money': item.get('money').get('S')
        })
    except Exception as e:
	    return(str(e))

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000)
