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

## Installation Guide

**1. Clone the repository**

```bash
git clone https://github.com/pramodj551-oss/Part3-Cybersecurity-Dashboard.git
cd Part3-Cybersecurity-Dashboard
```

**2. Create a virtual environment**

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Linux / macOS:
```bash
source venv/bin/activate
```

**3. Install required packages**

```bash
pip install -r requirements.txt
```

**4. Run the dashboard**

```bash
streamlit run app.py
```

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
| **Status** | Phase 1 Started 🚀 |

---

## License

See [LICENSE](LICENSE) for details.
