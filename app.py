# -------------------------
# Import required libraries
# -------------------------
from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
import os

# -------------------------
# Create Flask app instance
# -------------------------
app = Flask(__name__)

# -------------------------
# Load the trained model and column names
# -------------------------
MODEL_PATH = 'gwp.pkl'
COLUMNS_PATH = 'model_columns.pkl'

model = None
model_columns = []

if os.path.exists(MODEL_PATH) and os.path.exists(COLUMNS_PATH):
    try:
        with open(MODEL_PATH, 'rb') as model_file:
            model = pickle.load(model_file)
        with open(COLUMNS_PATH, 'rb') as cols_file:
            model_columns = pickle.load(cols_file)
        print("✅ Model and columns loaded successfully.")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
else:
    print("⚠️ Warning: Model or column files not found. Please train the model first.")

# -------------------------
# Define Routes
# -------------------------

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['GET'])
def predict():
    return render_template('predict.html')

@app.route('/submit', methods=['POST'])
def submit():
    if model is None or not model_columns:
        # If model not loaded, show 502.html
        return render_template('502.html'), 502

    try:
        form_data = request.form.to_dict()
        input_data_dict = {col: 0 for col in model_columns}

        input_data_dict['team'] = float(form_data['team'])
        input_data_dict['no_of_workers'] = float(form_data['no_of_workers'])
        input_data_dict['smv'] = float(form_data['smv'])
        input_data_dict['incentive'] = float(form_data['incentive'])
        input_data_dict['targeted_productivity'] = float(form_data['targeted_productivity'])
        input_data_dict['over_time'] = float(form_data['over_time'])

        # One-hot encoding handling
        department = form_data.get('department')
        if department:
            col_name = f"department_{department}"
            if col_name in input_data_dict:
                input_data_dict[col_name] = 1

        quarter = form_data.get('quarter')
        if quarter:
            col_name = f"quarter_{quarter}"
            if col_name in input_data_dict:
                input_data_dict[col_name] = 1

        day = form_data.get('day')
        if day:
            col_name = f"day_{day}"
            if col_name in input_data_dict:
                input_data_dict[col_name] = 1

        input_df = pd.DataFrame([input_data_dict])
        input_df = input_df[model_columns]
        prediction = model.predict(input_df)[0]
        prediction = max(0, min(1.5, prediction))

        percentage = prediction * 100
        formatted_prediction = f"{percentage:.1f}%"

        if prediction >= 0.9:
            remark = "Excellent projected productivity! Consider replicating these conditions."
        elif prediction >= 0.75:
            remark = "Good productivity. Minor adjustments may optimize further."
        elif prediction >= 0.6:
            remark = "Moderate productivity. Consider improvement strategies."
        else:
            remark = "Low productivity. Re-evaluate team, SMV, or incentives."

        summary_data = {
            'department': form_data.get('department'),
            'team': form_data.get('team'),
            'no_of_workers': form_data.get('no_of_workers'),
            'smv': form_data.get('smv'),
            'targeted_productivity': form_data.get('targeted_productivity'),
            'incentive': form_data.get('incentive'),
            'over_time': form_data.get('over_time')
        }

        return render_template('submit.html',
                               prediction=formatted_prediction,
                               remark=remark,
                               summary=summary_data)

    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return render_template('submit.html',
                               prediction="Error: Invalid input.",
                               remark="An error occurred. Please check your inputs.",
                               summary=None)

# -------------------------
# Error Handlers
# -------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(502)
def bad_gateway_error(e):
    return render_template('502.html'), 502

# -------------------------
# Run the Flask App
# -------------------------

if __name__ == '__main__':
    app.run(debug=True)
