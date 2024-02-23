from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl','rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')
standard_to = StandardScaler()
@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        Year=int(request.form['Year'])
        present_price=float(request.form['Present_price'])
        kms_driven=int(request.form['kms_Driven'])
        kms_driven2=np.log(kms_driven)
        owner=int(request.form['owner'])
        Fuel_type=request.form['Fuel']
        if Fuel_type=='Petrol':
            Fuel_type_petrol=1
            Fuel_type_diesle=0
        elif Fuel_type=='Diesel':
            Fuel_type_petrol=0
            Fuel_type_diesle=1
        else:
            Fuel_type_petrol=0
            Fuel_type_diesle=0
        currentYear = datetime.now().year
        Year=currentYear-Year
        seller_type_Individual=request.form['Seller_type']
        if seller_type_Individual=='Individual':
            seller_type_Individual=1
        else:
            seller_type_Individual=0
        Transmission_type_manual=request.form['Transmission_mannual']
        if Transmission_type_manual=='Mannual':
            Transmission_type_manual=1
        else:
            Transmission_type_manual=0
        prediction=model.predict([[present_price,kms_driven2,owner,Year,Fuel_type_diesle,Fuel_type_petrol,seller_type_Individual,Transmission_type_manual]])
        output=round(prediction[0],2)
        if(output<0):
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_texts="You can sell this car at {} lakhs".format(output))
    else:
        return render_template('index.html')
    
if __name__=="__main__":
    app.run(debug=True)
    


