# Performix.AI — Predictive Workforce Intelligence

Hello everyone! This is a project that I built completely on my own from scratch. It's called **Performix.AI**, and it uses machine learning to predict employee performance. I created everything — the machine learning models, backend with Flask, and even designed the frontend using HTML and CSS.

## 🔍 What This Project Does

This project is made to help understand how employee performance can be predicted using their data. It gives insights that can be useful for HR teams, managers, or anyone handling people in an organization. It can help in:

- Understanding which employees are likely to perform well
- Identifying who might need training or upskilling
- Helping in better role assignment and project allocation
- Forecasting productivity for future planning
- Improving overall team efficiency and success

## 🛠️ Technologies Used

- **Python** (core language for backend and ML)
- **Flask** (web framework)
- **Pandas & NumPy** (data handling)
- **Scikit-learn** and **XGBoost** (for building and training models)
- **HTML & CSS** (to create the user interface)
- **Joblib** (to save and load ML models)
- **VS Code** (for development)

## 📁 Project Structure (Simple View)

```
performix-ai/
├── app.py              # Flask backend
├── model.pkl           # Trained machine learning model
├── templates/
│   └── index.html      # Main webpage
├── static/
│   └── style.css       # All the styles
├── requirements.txt    # Python libraries used
└── README.md           # This file
```

## 💻 How to Run Locally

1. Clone this repository:
```bash
git clone https://github.com/your-username/performix-ai.git
cd performix-ai
```

2. Install the required libraries:
```bash
pip install -r requirements.txt
```

3. Run the Flask app:
```bash
python app.py
```

4. Open your browser and go to: `http://127.0.0.1:5000`

## 🚀 Deployment on Render

This app is deployed using **Render** because GitHub does not provide permission to run backend Flask servers directly.

> ⚠️ **Note:** This project works on **Render** because GitHub does not allow running backend Flask applications directly through its interface.

To deploy on Render:
- Upload all your files
- Set `app.py` as the entry point
- Add the following build and start commands:
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `python app.py`
- Enable web service on port `5000`

✅ This setup works perfectly with Render and keeps your ML model live!

## ✨ Features

- Predicts employee performance using input values
- Clean UI design with all code written manually by me
- Works end-to-end — from taking input to displaying prediction
- Can be extended for other domains like education, healthcare, etc.
- Uses modern design with responsive layout
- No third-party templates or auto-generators used — built manually from scratch

## 🙋‍♂️ About Me & Why I Made This

I made this project completely on my own to practice and show what I can do with machine learning and web development. No team, no help — just me learning and building.

I wanted to combine my skills in Python, ML, and frontend to make something real. I chose employee performance prediction because it's a real-world use case that many companies care about.

I believe this project shows that with consistent learning and passion, one person can build full systems that actually work. I hope it inspires others too!

## 🌐 Future Scope

- Add login and role-based dashboard for HR and Admin
- Save predictions in database for analysis
- Add charts and visualizations for better insights
- Add feature importance view to explain ML predictions
- Connect to a real-time dataset/API in future
- Allow users to upload Excel or CSV files for bulk predictions
- Improve accuracy using deep learning or ensemble stacking techniques
- Add exportable reports (PDF/CSV)

## 🔗 Live Link

[https://employee-performance-site.onrender.com/](https://employee-performance-site.onrender.com/)

## 📜 License

This project is under the MIT License — you can use and modify it freely.

---

Thanks for visiting! ⭐ Feel free to share feedback or star the repository!

— *Made with dedication and full effort by a single developer.*

<img width="1857" height="1790" alt="image" src="https://github.com/user-attachments/assets/062c46ea-328f-4b40-9b99-6d6e386c4e89" />
