from flask import Flask, request

app = Flask("my-app")


@app.route('/login', methods=['GET'])
def login():
    user = request.json['username']
    pwd = request.json['password']
    if user == 'admin' and pwd == 123456:
        code = 200
        message = 'Login success'
    else:
        code = 300
        message = 'Login failed'
    return {
        'code': code,
        'message': message,
        'data': {
            'token': '000000000000001',
            'user_name': 'admin',
            'login_type': 1,
            'authorization': '000000000000002'

        }
    }


@app.route('/add', methods=['POST'])
def add():
    header = request.headers
    authorization = request.json['authorization']
    value0 = request.json['value0']
    value1 = request.json['value1']
    if authorization == '000000000000002':
        code = 200
        message = 'add success'
        res = value0 + value1
    else:
        code = 201
        message = 'add failed'
        res = None
    return {
        'code': code,
        'message': message,
        'data': [{'interface': 'add'}, {'num': res}]
    }


@app.route('/less', methods=['POST'])
def less_niubi():
    header = request.headers
    authorization = request.json['authorization']
    print(authorization)
    value0 = request.json['value0']
    value1 = request.json['value1']
    if authorization == '000000000000002':
        code = 200
        message = 'less success'
        res = value0 - value1
    else:
        code = 201
        message = 'less failed'
        res = None
    return {
        'code': code,
        'message': message,
        'data': {'interface': 'less', 'result': res}
    }


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8100, debug=True)
