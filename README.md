<div align="center">

<img src="https://img.icons8.com/color/96/stock-market.png" width="80" style="margin:0 10px;"/>
<img src="https://img.icons8.com/color/96/artificial-intelligence.png" width="80" style="margin:0 10px;"/>
<img src="https://img.icons8.com/color/96/python.png" width="80" style="margin:0 10px;"/>
<img src="https://img.icons8.com/color/96/pandas.png" width="80" style="margin:0 10px;"/>
<img src="https://img.icons8.com/color/96/streamlit.png" width="80" style="margin:0 10px;"/>
<img src="https://img.icons8.com/color/96/docker.png" width="80" style="margin:0 10px;"/>

<h1>📈 Stock Market Closing Price Predictor</h1>
<p>
	<b>Forecast tomorrow's closing price for any company on the exchange!</b><br>
	<i>Modern, interactive, and fully reproducible ML pipeline + web app.</i>
</p>

</div>

---

## 🚀 Project Overview

This project is a full-stack machine learning pipeline and web application for predicting the next-day closing price of stocks. It features:

- **Automated data cleaning & feature engineering**
- **Time-series aware ML models** (Linear Regression, Random Forest, XGBoost, etc.)
- **Interactive Streamlit dashboard** for company selection and prediction
- **Beautiful UI & visualizations**
- **Reproducible, modular codebase**

---

## 🛠️ Tech Stack & Tools

- <img src="https://img.icons8.com/color/48/python.png" width="24"/> **Python 3.9+**
- <img src="https://img.icons8.com/color/48/pandas.png" width="24"/> **Pandas**
- <img src="https://img.icons8.com/color/48/scikit-learn.png" width="24"/> **scikit-learn**
- <img src="https://img.icons8.com/color/48/artificial-intelligence.png" width="24"/> **XGBoost**
- <img src="https://img.icons8.com/color/48/streamlit.png" width="24"/> **Streamlit**
- <img src="https://img.icons8.com/color/48/docker.png" width="24"/> **Docker**

---

## 📦 Project Structure

```
project/
│
├── data/
│   └── stock_data.csv
├── models/
│   └── best_model.pkl
├── backend/
├── pages/
├── app.py
├── requirements.txt
└── ...
```

---

## ✨ Features

- **Upload & clean stock data**
- **Feature engineering** (lags, rolling stats, returns, etc.)
- **Time-based train-test split** (no leakage!)
- **Multiple regression models**
- **Model evaluation & selection**
- **Next-day close prediction**
- **Interactive Streamlit UI**
- **Line charts & visualizations**

---

## 🖥️ How to Run

1. **Clone the repo**
2. **Install dependencies**
	 ```bash
	 pip install -r requirements.txt
	 ```
3. **Run the app**
	 ```bash
	 streamlit run app.py
	 ```

---

## 📊 Example UI

![screenshot](https://user-images.githubusercontent.com/674621/235352981-2e7e7e7e-2e7e-4e7e-8e7e-2e7e7e7e7e7e.png)

---

## 🤝 Contributing

Pull requests and suggestions are welcome! For major changes, please open an issue first.

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
│   ├── 3_predictions.py
│   └── 4_data_explorer.py
├── backend/
│   ├── etl/
│   │   ├── pdf_extractor.py
│   │   ├── data_cleaner.py
│   │   └── loader.py
│   ├── db/
│   │   ├── models.py
│   │   ├── schema.sql
│   │   └── db.py
│   ├── ml/
│   │   ├── prophet_model.py
│   │   └── lstm_model.py
│   └── api.py
├── tests/
│   ├── test_pdf_extraction.py
│   ├── test_data_cleaning.py
│   ├── test_db_loading.py
│   └── test_model_training.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .github/workflows/ci.yml
└── README.md
```

## Environment Variables
- `DATABASE_URL` (default: sqlite:///stock-app.db)

## System Dependencies
- Camelot: Requires Ghostscript (`brew install ghostscript` on macOS)

## Acceptance Checklist
- [ ] Upload PDF, preview, save to DB
- [ ] Company analysis and charts
- [ ] Prophet forecast and metrics
- [ ] All tests pass
- [ ] Docker Compose up: app + Postgres

---
