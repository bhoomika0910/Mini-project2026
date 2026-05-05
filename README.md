# 🏛️ AI-Driven Smart Heritage Site Preservation & Monitoring System
### *Intelligent Cultural Heritage Monitoring Platform using AI and IoT*

---

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Machine Learning](https://img.shields.io/badge/AI-Machine%20Learning-purple)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

# 📌 Project Overview

Heritage monuments are constantly affected by **environmental conditions, pollution, climate change, and human activities**. Traditional monitoring methods rely heavily on **manual inspections**, which are slow and often detect damage too late.

This project introduces a **Smart Heritage Monitoring System** that uses **IoT-based environmental sensing, machine learning models, and a monitoring dashboard** to track monument health in real time.

The system collects environmental data, analyzes it using AI models, and visualizes the results through a **real-time monitoring dashboard**. It also generates alerts when potential risks are detected.

The goal is to help conservation authorities move from **reactive restoration to predictive preservation**.

---

# 🌍 Industry Relevance

This system can support organizations such as:

- Archaeological Survey Departments  
- Cultural Heritage Preservation Agencies  
- UNESCO Heritage Conservation Programs  
- Smart City Infrastructure Projects  
- Cultural Heritage Research Institutions  

---

# 🎯 Project Objectives

- Monitor environmental conditions affecting heritage structures  
- Predict deterioration risks using machine learning models  
- Detect abnormal activities that may indicate vandalism  
- Generate alerts for conservation authorities  
- Provide an interactive monitoring dashboard  
- Support data-driven heritage preservation planning  

---

# ⚙️ Key System Features

## 📡 Environmental Monitoring (IoT Simulation)

Environmental sensors collect data about monument surroundings.

Parameters monitored include:

- Temperature  
- Humidity  
- Air Pollution  
- Structural Vibration  
- Crack Width *(simulated)*  

Since real hardware deployment may not be available, **sensor data is simulated using Python scripts** representing IoT device behaviour.

---

## 🧠 AI-Based Risk Prediction

Machine learning models analyze environmental and structural conditions to estimate deterioration risks.

Models used:

- **Random Forest** – Predict deterioration risk level  
- **Isolation Forest** – Detect abnormal patterns  

Example prediction output:

```
Risk Level: Medium
Prediction Confidence: 0.87
```

---

## 📊 Monitoring Dashboard

A real-time dashboard allows conservation authorities to monitor monument conditions.

Dashboard capabilities:

- Live sensor data monitoring  
- Environmental trend graphs  
- Risk prediction indicators  
- Site Health Index visualization  
- Alert notifications  

The dashboard is built using **Streamlit**.

---

## 🚨 Alert System

The platform automatically generates alerts when risk thresholds are exceeded.

| Alert Level | Meaning |
|-------------|---------|
| Low | Minor environmental change |
| Medium | Possible deterioration risk |
| High | Structural anomaly detected |
| Critical | Immediate intervention required |

Alerts appear on the dashboard and can optionally trigger email notifications.

---

# 🧠 Site Health Index (SHI)

The system computes a **Site Health Index (SHI)** representing the overall health of a monument.

```
SHI = (Environmental Score × 0.3)
    + (Structural Score × 0.4)
    + (AI Risk Score × 0.3)
```

Example:

```
Site Health Index: 82%
Status: Stable
```

---

# 🏗️ System Architecture

```
IoT Sensor Simulation
        │
        ▼
FastAPI Backend (Data Ingestion API)
        │
        ▼
SQLite Database (Sensor Data Storage)
        │
        ▼
AI Risk Prediction Engine
(Random Forest + Isolation Forest)
        │
        ▼
Alert Detection Logic
        │
        ▼
Streamlit Dashboard
(Real-Time Monitoring & Visualization)
```

---

# 👥 Team Members & Work Division

The project is developed by **three members with equal contribution (~33% each)**.

---

## 👩‍💻 Anishka Jain  
**Role:** IoT Simulation & AI Model Developer  

Responsibilities:

- Design sensor simulation  
- Generate synthetic sensor data  
- Build preprocessing pipeline  
- Train machine learning models  
- Implement anomaly detection  
- Evaluate model performance  

Deliverables:

- Sensor simulation scripts  
- Trained AI models  
- Model evaluation report  

---

## 👩‍💻 Bhoomika Agarwal  
**Role:** Backend & System Developer  

Responsibilities:

- Design backend architecture  
- Develop REST APIs using **FastAPI**  
- Implement sensor data ingestion  
- Manage **SQLite database**  
- Integrate AI prediction model  
- Implement alert detection logic  

Deliverables:

- Backend API  
- Database schema  
- Alert system implementation  

---

## 👩‍💻 Shraddha Singh  
**Role:** Dashboard Developer & Documentation Lead  

Responsibilities:

- Design dashboard layout  
- Develop dashboard using **Streamlit**  
- Implement charts and visualization  
- Display AI predictions and alerts  
- Implement Site Health Index visualization  
- Write system documentation  

Deliverables:

- Interactive monitoring dashboard  
- Visualization modules  
- System documentation  

---

# 🛠️ Technology Stack

### IoT Layer
- Python Sensor Simulation
- REST API communication

### AI / Machine Learning
- Python
- Pandas
- Scikit-learn
- Random Forest
- Isolation Forest

### Backend
- FastAPI
- Python

### Database
- SQLite

### Dashboard
- Streamlit
- Plotly / Matplotlib

### Development Tools
- Git & GitHub
- VS Code

---

# 📁 Project Structure

```
heritage-ai-system
│
├── iot
│   └── sensor_simulator.py
│
├── ai_models
│   ├── train_model.py
│   └── risk_prediction.py
│
├── backend
│   └── api.py
│
├── dashboard
│   └── app.py
│
├── data
│   └── sensor_data.csv
│
└── docs
    └── architecture.md
```

---

# 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/your-repo/heritage-ai-system.git
cd heritage-ai-system
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Backend

```bash
uvicorn backend.api:app --reload
```

### Run Dashboard

```bash
streamlit run dashboard/app.py
```

---

# 📊 Expected Outcomes

- Functional AI-powered heritage monitoring system  
- Real-time monitoring dashboard  
- Deterioration risk prediction model  
- Automated alert system  
- Heritage site health analytics  

---

# ⭐ Future Enhancements

- Computer vision-based crack detection  
- Drone-based monument inspection  
- Satellite environmental monitoring  
- Multi-site heritage monitoring platform  

---

# 📜 License

This project is released under the **MIT License**.
