Economic Insights Dashboard

📊 Interactive dashboard visualizing U.S. macroeconomic indicators (GDP, CPI, Unemployment, etc.) using data from the **FRED API**. Built with **Python, Streamlit, Plotly, and SQLite**.

---

## Features

* Pulls live economic data from the FRED API.
* Stores and queries data in a local SQLite database.
* Interactive charts with Plotly for GDP, CPI, and Unemployment.
* Sidebar control for selecting KPIs.
* Optional raw data table view.
* Fully local, can be extended for deployment.

---

## Tech Stack

* Python
* Streamlit
* Plotly
* SQLite
* pandas
* sqlalchemy
* fredapi

---

## Setup Instructions

Follow these steps to run the dashboard locally. This guide assumes you’re using **Windows PowerShell**.

### 1️⃣ Clone the repository

```powershell
git clone https://github.com/yourusername/Economic-Insights-Dashboard.git
cd "Economic Insights Dashboard"
```

> Note: Use quotes if the folder name has spaces.

### 2️⃣ Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3️⃣ Install dependencies

```powershell
pip install -r requirements.txt
```

### 4️⃣ Set up your FRED API key

1. Register and get a FRED API key here: [FRED API](https://fred.stlouisfed.org/docs/api/api_key.html)
2. Create a `.env` file in the project root:

```
FRED_API_KEY=your_api_key_here
```

3. Make sure `.env` is listed in `.gitignore` to keep it hidden.

> Alternatively, you can set it as a PowerShell environment variable (without using `.env`):

```powershell
setx FRED_API_KEY "your_api_key_here"
```

Then restart PowerShell.

---

### 5️⃣ Run the dashboard

```powershell
streamlit run app.py
```

* This will open a browser window with your interactive dashboard.

---

## Notes

* **Security:** Your FRED API key is never stored in code or GitHub. Using `.env` or environment variables keeps it private.
* **Caching:** The app caches data for 24 hours to reduce API calls.
* **Database:** SQLite (`econ.db`) stores the fetched data. It’s ignored by GitHub in `.gitignore`.

---

## Folder Structure

```
Economic-Insights-Dashboard/
│
├─ app.py
├─ requirements.txt
├─ .gitignore
├─ README.md
├─ .env       # ignored by git
└─ econ.db    # ignored by git
```

---

## Screenshot

<img width="1263" height="1306" alt="Screenshot 2025-08-26 142118" src="https://github.com/user-attachments/assets/8fb261eb-3f41-452b-8f89-7e4b2f3e4989" />

---

## Future Improvements

* Add more KPIs (Interest Rates, Money Supply, Employment, etc.).
* Enable CSV download for selected KPIs.
* Deploy as a live web app (Streamlit Cloud, Render, or Docker).
