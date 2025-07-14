# -------------------------
# Import required libraries
# -------------------------
from flask import Flask, render_template, request  # Flask for web app
import pickle                                      # To load the saved model
import numpy as np                                 # For number operations (optional)
import pandas as pd                                # To handle form data as DataFrame
import os                                          # For file existence checks

# -------------------------
# Create Flask app instance
# -------------------------
app = Flask(__name__)

# -------------------------
# Load the trained model and column names
# -------------------------
MODEL_PATH = 'gwp.pkl'                 # Path to saved model file
COLUMNS_PATH = 'model_columns.pkl'     # Path to saved feature columns

model = None           # Placeholder for the loaded model
model_columns = []     # Placeholder for feature column names

# Try loading the model and column names from files
if os.path.exists(MODEL_PATH) and os.path.exists(COLUMNS_PATH):
    try:
        with open(MODEL_PATH, 'rb') as model_file:
            model = pickle.load(model_file)  # Load trained model
        with open(COLUMNS_PATH, 'rb') as cols_file:
            model_columns = pickle.load(cols_file)  # Load column names
        print(" Model and columns loaded successfully.")
    except Exception as e:
        print(f" Error loading model: {e}")
else:
    print("⚠️ Warning: Model or column files not found. Please train the model first.")

# -------------------------
# Define App Routes
# -------------------------

# Home Page Route
@app.route('/')
def home():
    # Renders the home.html template for the home page.
    return render_template('home.html')

# About Page Route
@app.route('/about')
def about():
    # Renders the about.html template for the about page.
    return render_template('about.html')

# Prediction Page Route (GET only, to display the form)
@app.route('/predict', methods=['GET'])
def predict():
    # If user visits /predict directly (GET request), show the prediction form.
    return render_template('predict.html')

# Submit Prediction Route (POST only, to process form data)
@app.route('/submit', methods=['POST'])
def submit():
    # Handles POST requests from the prediction form.
    
    # Check if the model is properly loaded before proceeding with prediction.
    if model is None or not model_columns:
        # If the model or columns are not loaded, display an error message on the submit page.
        return render_template('submit.html', prediction="❌ Model not loaded. Please ensure the model and column files exist and are correctly loaded.")

    try:
        # Get all form inputs as a dictionary from the request.
        form_data = request.form.to_dict()

        # Initialize a dictionary with all expected model columns, setting their default value to 0.
        # This is crucial for one-hot encoded features that might not be present in every form submission.
        input_data_dict = {col: 0 for col in model_columns}

        # Fill numeric inputs from the form data.
        # Convert values to float as expected by the model.
        input_data_dict['team'] = float(form_data['team'])
        input_data_dict['no_of_workers'] = float(form_data['no_of_workers'])
        # Note: 'no_of_style_change' and 'month' are in the provided app.py but not in predict.html.
        # Assuming these will be added to the form or have default handling.
        # For now, if they are not in form_data, they will remain 0 from the initialization.
        # If they are critical and always expected, you might need to add them to the form or provide default values.
        input_data_dict['smv'] = float(form_data['smv'])
        input_data_dict['incentive'] = float(form_data['incentive'])
        input_data_dict['targeted_productivity'] = float(form_data['targeted_productivity'])
        input_data_dict['over_time'] = float(form_data['over_time']) # Added over_time from predict.html

        # Handle one-hot encoded categorical inputs.
        # For 'department', 'quarter', and 'day', set the corresponding column to 1 if it exists in the model columns.
        # This assumes the form values directly map to the one-hot encoded column names (e.g., "department_Sewing").
        
        # Department
        department_value = form_data.get('department')
        if department_value:
            department_col = f"department_{department_value}"
            if department_col in input_data_dict:
                input_data_dict[department_col] = 1

        # Quarter (assuming quarter input is available, if not, it will remain 0)
        # The provided predict.html does not have a 'quarter' input. 
        # If 'quarter' is a required feature, it needs to be added to the form.
        # For demonstration, keeping the logic as it was in the original app.py.
        quarter_value = form_data.get('quarter')
        if quarter_value:
            quarter_col = f"quarter_{quarter_value}"
            if quarter_col in input_data_dict:
                input_data_dict[quarter_col] = 1

        # Day (assuming day input is available, if not, it will remain 0)
        # The provided predict.html does not have a 'day' input.
        # If 'day' is a required feature, it needs to be added to the form.
        # For demonstration, keeping the logic as it was in the original app.py.
        day_value = form_data.get('day')
        if day_value:
            day_col = f"day_{day_value}"
            if day_col in input_data_dict:
                input_data_dict[day_col] = 1
        
        # Convert the input data dictionary to a Pandas DataFrame.
        # Ensure the DataFrame columns are in the same order as the model's training columns.
        input_df = pd.DataFrame([input_data_dict])
        input_df = input_df[model_columns]

        # Make a prediction using the loaded machine learning model.
        prediction = model.predict(input_df)[0]

        # Limit predictions between 0 and 1.5 to ensure realistic output.
        prediction = max(0, min(1.5, prediction))

        # Format the prediction result as a percentage.
        percentage = prediction * 100
        formatted_prediction = f"{percentage:.1f}%"

        # Generate a remark based on the prediction for strategic analysis.
        remark = ""
        if prediction >= 0.9:
            remark = "Excellent projected productivity! This scenario suggests highly efficient operations. Consider replicating these conditions."
        elif prediction >= 0.75:
            remark = "Good projected productivity. The team is expected to perform well. Minor adjustments might further optimize output."
        elif prediction >= 0.6:
            remark = "Moderate projected productivity. There might be opportunities for improvement. Review team composition, task complexity, or incentive structures."
        else:
            remark = "Lower projected productivity. This scenario indicates potential challenges. It's advisable to re-evaluate parameters like team size, SMV, or incentive to boost performance."

        # Prepare a summary of the input parameters to display on the submit page.
        summary_data = {
            'department': form_data.get('department'),
            'team': form_data.get('team'),
            'no_of_workers': form_data.get('no_of_workers'),
            'smv': form_data.get('smv'),
            'targeted_productivity': form_data.get('targeted_productivity'),
            'incentive': form_data.get('incentive'),
            'over_time': form_data.get('over_time')
        }

        # Render the submit.html template, passing the prediction, remark, and input summary.
        return render_template('submit.html', 
                               prediction=formatted_prediction, 
                               remark=remark,
                               summary=summary_data)

    except Exception as e:
        # Catch any errors during prediction or data processing and display an error message.
        print(f" Prediction error: {e}")
        return render_template('submit.html', prediction="Error: Invalid input values. Please try again.", remark="An error occurred during prediction. Please check your inputs.", summary=None)

# -------------------------
# Error Handlers
# -------------------------
@app.errorhandler(404)
def page_not_found(error):
    # Renders the 404.html template for a 404 Not Found error.
    # The second return value (404) sets the HTTP status code.
    return render_template('404.html'), 404

# -------------------------
# Run the Flask app
# -------------------------
if __name__ == '__main__':
    # Run the Flask application.
    # Set debug=True for development to get detailed error logs.
    app.run(debug=True)
