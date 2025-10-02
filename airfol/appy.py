import pickle
import flask
from flask import Flask, request,app,jsonify,render_template
from flask_cors import CORS
import numpy as np
import pandas as pd

app = Flask(__name__)
model = pickle.load(open('model_1.pkl','rb'))

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/predict_api",methods=["POST"])
def predict_api():
    data  = request.form.values()
    print(request.json['data'])
    newData = [list(data.values())]
    print(newData)
    output = model.predict(newData)[0]
    # return jsonify(output)

@app.route("/predict",methods=["POST"])
def predict():
    data=[float(x) for x in request.form.values()]
    final_features = [np.array(data)]
    print(data)
    output=model.predict(final_features)[0]
    print(output)
    #output = round(prediction[0], 2)
    return render_template('home.html', prediction_text="Airfoil pressure is  {}".format(output))
if __name__ == "__main__":
    app.run(debug=True)