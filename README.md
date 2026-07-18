# 🛡️ AI-Powered Cybersecurity Dashboard

**Part 3 of the End-to-End Applied AI & ML Data Product Capstone Project**
**Phase 1: Project Setup**

An interactive Streamlit dashboard for visualizing cybersecurity incidents, exploring datasets, monitoring machine learning performance, and predicting incident severity using the trained classification model from Part 2.

---

## Project Overview

Part 1 answered *what happened* (descriptive analytics) and Part 2 answered *what's likely to happen* (predictive analytics). Part 3 brings both together into a single interactive web application, giving analysts a hands-on way to explore incident data, understand the trained model, and generate live severity predictions — no code required.

---

## Project Objectives

This dashboard enables users to:

- Explore the cybersecurity dataset interactively
- Perform visual data analysis
- View key performance indicators (KPIs)
- Predict incident severity using the trained ML model
- Understand feature importance
- Review model evaluation metrics
- Generate insights through an intuitive web interface

---

## Key Features

- Interactive Streamlit dashboard
- Dataset explorer
- Exploratory Data Analysis (EDA) views
- Machine learning prediction interface
- Feature importance visualization
- Model performance dashboard
- Downloadable prediction results
- Responsive user interface
- Production-ready architecture

---

## Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python 3.10+ |
| Web Framework | Streamlit |
| Data Processing | Pandas, NumPy |
| Data Visualization | Matplotlib, Plotly |
| Machine Learning | Scikit-learn, Joblib |
| Version Control | Git & GitHub |

---

## Repository Structure

```text
Part3-Cybersecurity-Dashboard/
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── CHANGELOG.md
├── .gitignore
│
├── config/
│   └── config.py
│
├── src/
│   ├── model_loader.py
│   ├── prediction.py
│   ├── preprocessing.py
│   ├── visualization.py
│   └── utils.py
│
├── pages/
│   ├── Home.py
│   ├── Dataset_Explorer.py
│   ├── EDA_Dashboard.py
│   ├── Prediction.py
│   ├── Feature_Importance.py
│   └── Model_Performance.py
│
├── assets/
│   ├── images/
│   └── styles/
│
├── data/
├── models/
├── outputs/
└── logs/
```

---

## System Requirements

Before running the project, ensure the following are installed:

- Python 3.10 or later
- Git
- pip (latest version)
- Streamlit

---

## Installation Guide

**1. Clone the repository**

```bash
git clone https://github.com/pramodj551-oss/Part3-Cybersecurity-Dashboard.git
cd Part3-Cybersecurity-Dashboard
```

**2. Create a virtual environment**

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install required packages**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**4. Verify required files exist**

Before launching the dashboard, confirm the following are present:

- `models/random_forest_model.pkl`
- `outputs/evaluation_report.csv`
- `outputs/feature_importance.csv`
- `data/cybersecurity_incidents.csv`

If any are missing, run the Part 2 ML pipeline to generate them.

**5. Run the dashboard**

```bash
streamlit run app.py
```

After the server starts, open the URL shown in the terminal (typically `http://localhost:8501`).

---

## Dashboard Modules

The application includes the following pages:

- Home
- Dataset Explorer
- EDA Dashboard
- Prediction
- Feature Importance
- Model Performance

---

## Streamlit Community Cloud Deployment

1. Push the project to GitHub.
2. Sign in to Streamlit Community Cloud.
3. Create a new app.
4. Select your repository.
5. Set:
   - **Repository:** your dashboard repository
   - **Branch:** `main`
   - **Main file:** `app.py`
6. Deploy the application.

---

## Troubleshooting

**Model file not found**
Cause: The trained model is missing.
Solution: Run the Part 2 training pipeline to generate `random_forest_model.pkl`.

**Missing Python packages**
Solution:
```bash
pip install -r requirements.txt
```

**CSV loading error**
Verify that:
- The uploaded file is a valid CSV.
- Column names match the format expected by the trained model.

**Prediction error**
Possible causes:
- Missing required features
- Incorrect feature order
- Different preprocessing than the training pipeline

Use the same preprocessing pipeline that was used during model training.

---

## Production Checklist

- [ ] Repository pushed to GitHub
- [ ] All dependencies installed
- [ ] Model file available
- [ ] Dataset available
- [ ] Dashboard launches successfully
- [ ] Prediction module working
- [ ] Feature importance displayed
- [ ] Evaluation report available
- [ ] README updated
- [ ] LICENSE included
- [ ] CHANGELOG updated

---

## Future Enhancements

- Docker support
- Authentication
- SHAP explainability
- REST API integration
- Cloud model storage
- Database integration
- User management
- Real-time monitoring

---

## Deliverables

By the end of Part 3, the repository will include:

- Interactive dashboard
- Model prediction interface
- Visual analytics
- Downloadable results
- Production-ready Streamlit application
- GitHub portfolio repository

---

## Project Metadata

| | |
|---|---|
| **Version** | 3.0 |
| **Project Type** | Interactive Machine Learning Dashboard |
| **Framework** | Streamlit |
| **Status** | Deployment Ready 🚀 |

**Deployment status by component:**

| Component | Status |
|---|---|
| Streamlit Application | ✅ Ready |
| Dashboard Pages | ✅ Ready |
| Prediction Module | ✅ Ready |
| Visualization | ✅ Ready |
| Deployment Guide | ✅ Ready |

---

## License

See [LICENSE](LICENSE) for details.
