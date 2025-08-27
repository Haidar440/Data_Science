from flask import Flask,request,jsonify
app = Flask(__name__)

@app.route('/abc',methods=['GET','POST'])
def test():
    if request.method == "POST":
        a = request.json['num1']
        b = request.json['num2']
        result = a + b
        return jsonify(result)
@app.route('/abc/haidar',methods=['POST'])
def test1():
    if request.method == "POST":
        a = request.json['num3']
        b = request.json['num4']
        result = a + b
        return jsonify(result)
@app.route('/abc/haidar/ali',methods=['POST'])
def test2():
    if request.method == "POST":
        a = request.json['num4']
        b = request.json['num5']
        result = a + b
        return jsonify(result)
@app.route('/abc/haidar/ali1',methods=['POST'])
def test3():
    if request.method == "POST":
        a = request.json['Haidar']
        b = request.json['Sunasara']
        result = a + b
        return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)