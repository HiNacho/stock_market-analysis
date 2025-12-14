<div align="center">

<img src="https://img.icons8.com/color/96/stock-market.png" width="80"/>
<img src="https://img.icons8.com/color/96/artificial-intelligence.png" width="80"/>
<img src="https://img.icons8.com/color/96/python.png" width="80"/>
<img src="https://img.icons8.com/color/96/pandas.png" width="80"/>
<img src="https://img.icons8.com/color/96/streamlit.png" width="80"/>
<img src="https://img.icons8.com/color/96/docker.png" width="80"/>

# 📈 Stock Market Closing Price Predictor

**Forecast tomorrow's closing price for any company on the exchange!**  
<i>Modern, interactive, and fully reproducible ML pipeline + web app.</i>

</div>

---

## 🚀 Overview

This project is a full-stack machine learning pipeline and web application for predicting the next-day closing price of stocks. It features:

- Automated data cleaning & feature engineering
- Time-series aware ML models (Linear Regression, Random Forest, Prophet, etc.)
- Interactive Streamlit dashboard for company selection and prediction
- Beautiful UI & visualizations
- Modular, reproducible codebase

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Pandas**
- **scikit-learn**
- **Prophet**
- **Plotly**
- **pdfplumber**
- **SQLAlchemy**
- **Streamlit**
- **Docker**

---

## 📦 Project Structure

```
project/
│
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker support
├── backend/
│   ├── db/                 # Database models and schema
│   ├── etl/                # Data extraction, cleaning, loading
│   └── ml/                 # ML models and utilities
├── data/                   # Raw and processed data
├── models/                 # Trained model artifacts
├── pages/                  # Streamlit multipage scripts
├── tests/                  # Unit tests
└── README.md
```

---

## ✨ Features

- **Upload & clean stock data from PDF**
- **Feature engineering** (lags, rolling stats, returns, etc.)
- **Time-based train-test split** (no leakage!)
- **Multiple regression models**
- **Model evaluation & selection**
- **Next-day close prediction**
- **Interactive Streamlit UI**
- **Line charts & visualizations**
- **Database integration for persistent storage**

---

## 🖥️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

### 4. (Optional) Run with Docker

```bash
docker build -t stock-predictor .
docker run -p 8501:8501 stock-predictor
```

---

## 📊 Example UI

![screenshot](https://user-images.githubusercontent.com/674621/235352981-2e7e7e7e-2e7e-4e7e-8e7e-2e7e7e7e7e7e.png)

---

## 🧪 Testing

Run all tests with:

```bash
pytest
```

---

## ⚙️ Configuration

- Environment variables (see `.env.example` or set `DATABASE_URL`)
- All configuration is handled via `app.py` and Streamlit sidebar

---

## 📄 License

MIT License

---

<div align="center">
	<img src="https://img.icons8.com/color/96/stock-market.png" width="60"/>
	<img src="https://img.icons8.com/color/96/artificial-intelligence.png" width="60"/>
	<img src="https://img.icons8.com/color/96/python.png" width="60"/>
	<img src="https://img.icons8.com/color/96/pandas.png" width="60"/>
	<img src="https://img.icons8.com/color/96/streamlit.png" width="60"/>
	<img src="https://img.icons8.com/color/96/docker.png" width="60"/>
	<br><br>
	<b>Made with ❤️ for the future of finance!</b>
</div>
