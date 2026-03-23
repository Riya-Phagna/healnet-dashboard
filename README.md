# 🏥 HealNet — AI Clinical Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![InfluxDB](https://img.shields.io/badge/InfluxDB-2.x-22ADF6?style=for-the-badge&logo=influxdb&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A real-time AI-powered clinical health management platform built with Streamlit, InfluxDB, and Python.**

*Developed as an internship project at [IoTrenetics Solutions Pvt. Ltd.](https://iotrenetics.com)*

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Authentication System](#-authentication-system)
- [Vital Ranges](#-vital-ranges-classification)
- [InfluxDB Integration](#-influxdb-integration)
- [Running Tests](#-running-tests)
- [Screenshots](#-screenshots)
- [Roadmap](#-roadmap)

---

## 🌟 Overview

HealNet is a full-stack clinical health monitoring platform that enables hospitals, clinics, doctors, staff, and individual patients to manage real-time health vitals. It connects to a live **InfluxDB** time-series database to pull patient metrics, classifies them against clinical guidelines (AHA/WHO/NIH), and displays trend charts with auto-refresh.

---

## ✨ Features

### 🔐 Authentication
- **4-tier role system** — Organisation, Doctor/Staff, Hospital Patient, Individual
- Secure SHA-256 password hashing
- Auto-generated IDs (`HN-XXXXX`, `DR-0001`, `PT-0001`, `HN-00001`)
- SQLite-backed persistent auth (`healnet_auth.db`)

### 📊 Health Monitoring
- **Live InfluxDB data** — no manual sliders; real sensor data
- Real-time classification of **7 clinical vitals** against AHA/WHO/NIH guidelines
- Severity levels: 🟢 Normal · 🟡 Moderate · 🔵 Low · 🔴 High · 🚨 Critical
- **Auto-refresh** at 5 / 10 / 30 / 60 second intervals
- **Trend charts** for the last 6 hours (Heart Rate, SpO₂, Blood Pressure, Risk Score)

### 👥 Patient Management
- Register patients with full demographics
- SQLite patient database (`patients.db`)
- View/search/delete patients in a live table
- CSV export of patient records

### 🎨 UI/UX
- Premium **frosted glass** login panel with background imagery
- Inter + Instrument Serif typography
- Colour-coded portal cards per role
- Responsive, single-file Streamlit app

---

## 📁 Project Structure

```
HealNet/
├── login.py              ← Entry point · auth screens · 4-tier login
├── app.py                ← Main app · InfluxDB · vitals dashboard
├── vital_ranges.py       ← Clinical range classification module
├── test_vitals_mock.py   ← 31 unit tests (unittest + mock)
├── write_data.py         ← Push test vitals to InfluxDB
├── influx_config.py      ← InfluxDB connection config
├── healnet_auth.db       ← Auto-created · users & orgs
└── patients.db           ← Auto-created · registered patients
```

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit, Custom CSS |
| Backend | Python 3.8+ |
| Time-series DB | InfluxDB 2.x (Flux queries) |
| Relational DB | SQLite3 |
| Auth | SHA-256 (hashlib) |
| Charts | Streamlit native charts |
| Testing | unittest, unittest.mock |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- InfluxDB 2.x running locally on `localhost:8086`

### 1. Clone the repository

```bash
git clone https://github.com/your-username/healnet.git
cd healnet
```

### 2. Install dependencies

```bash
pip install streamlit influxdb-client pandas
```

### 3. Configure InfluxDB

Edit `influx_config.py` with your InfluxDB credentials:

```python
INFLUX_URL   = "http://localhost:8086"
INFLUX_TOKEN = "your-token-here"
INFLUX_ORG   = "healnet-org"
INFLUX_BUCKET = "healnet"
```

### 4. Push sample data (optional)

```bash
python write_data.py
```

### 5. Run the app

```bash
streamlit run login.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🔑 Authentication System

| Role | Access Code | Org Code Required | Auto ID Format |
|---|---|---|---|
| **Organisation** (Hospital/Clinic) | `org` | ❌ Auto-generated | `HN-XXXXX` |
| **Doctor / Staff** | `staff` | ✅ Yes | `DR-0001` |
| **Hospital Patient** | `orgpatient` | ✅ Yes | `PT-0001` |
| **Individual / Personal** | `solo` | ❌ No | `HN-00001` |

> **Not sure which to pick?**  
> - Hospital gave you a code → *Patient at a Hospital*  
> - No code → *Individual / Personal*

---

## 🩺 Vital Ranges Classification

All ranges follow **AHA / WHO / NIH** clinical guidelines.

| Vital | Low | Normal | Moderate | High | Critical |
|---|---|---|---|---|---|
| **Blood Pressure** | < 90/60 | 90–119 | 120–129 | 130–179 | ≥ 180/120 |
| **Heart Rate** | < 50 bpm | 60–100 | — | > 100 | > 150 or < 38 |
| **SpO₂** | — | ≥ 95% | 90–94% | 85–89% | < 85% |
| **Blood Sugar** | < 70 mg/dL | 70–99 | 100–125 | 126–199 | ≥ 200 |
| **Temperature** | < 97°F | 97–100.3 | — | ≥ 100.4 | ≥ 104 |
| **Respiratory Rate** | < 12 | 12–20 | — | > 20 | > 30 |
| **BMI** | < 18.5 | 18.5–24.9 | 25–29.9 | 30–39.9 | ≥ 40 |

---

## 📡 InfluxDB Integration

HealNet queries InfluxDB for the following fields:

```
Measurement : health_metrics
Tag         : patient_id
Fields      : heart_rate, spo2, systolic, diastolic,
              blood_sugar, temperature, respiratory_rate,
              bmi, steps, sleep_hours, risk_score
```

Two query functions are provided in `app.py`:

- `fetch_latest_vitals(patient_id, hours=1)` — Returns the most recent reading as a dict
- `fetch_history(patient_id, hours=6)` — Returns a pivoted DataFrame for trend charts

---

## 🧪 Running Tests

31 unit tests covering all vital classifiers and mock sensor inputs:

```bash
python test_vitals_mock.py
```

**Test coverage:**

| Suite | Tests |
|---|---|
| `TestBloodPressure` | 6 |
| `TestHeartRate` | 5 |
| `TestSpO2` | 4 |
| `TestBloodSugar` | 5 |
| `TestEdgeCases` | 6 |
| `TestMockSensorInput` | 5 |
| **Total** | **31 ✅** |

---

## 🗺 Roadmap

- [ ] Replace SQLite auth with **Supabase / PostgreSQL** for multi-device access
- [ ] Email verification, JWT tokens, password reset, 2FA
- [ ] RBAC — role-based field and action restrictions
- [ ] Upgrade password hashing to **bcrypt / Argon2**
- [ ] Integrate AI scan analysis models (`ai_models/`)
- [ ] Mobile-responsive layout
- [ ] PDF report generation and email delivery
- [ ] Docker + deployment guide

---
## output

## 🏢 About

Built as an internship project at **IoTrenetics Solutions Pvt. Ltd.**  
© 2025 HealNet · HIPAA-ready architecture · 256-bit Encryption

---

<div align="center">
  <sub>Made with ❤️ using Python & Streamlit</sub>
</div>
