import pandas as pd
from fredapi import Fred
from sqlalchemy import create_engine
import plotly.express as px
import streamlit as st
import os

# --- Configuration ---
# Get the API key from environment variables for security
# You can set this in your terminal: set FRED_API_KEY=your_key (Windows) or export FRED_API_KEY=your_key (macOS/Linux)
# Or, you can replace os.getenv("FRED_API_KEY") with your key as a string, e.g., "YOUR_API_KEY"
API_KEY = os.getenv("FRED_API_KEY", "YOUR_API_KEY") 
DB_FILE = "econ.db"

# --- Data Loading and Caching ---
@st.cache_data(ttl=60*60*24) # Cache data for 24 hours
def load_data():
    """
    Fetches data from FRED API, cleans it, and loads it into a SQLite database.
    Then, it queries and returns the aggregated yearly data.
    """
    if API_KEY == "YOUR_API_KEY":
        st.error("Please replace 'YOUR_API_KEY' with your actual FRED API key.")
        return pd.DataFrame()

    # Step 2: Extract Data with Python
    fred = Fred(api_key=API_KEY)

    # Pull series
    gdp = fred.get_series('GDP')
    cpi = fred.get_series('CPIAUCSL')
    unemp = fred.get_series('UNRATE')

    # Combine into a single DataFrame
    df = pd.DataFrame({
        "GDP": gdp,
        "CPI": cpi,
        "Unemployment": unemp
    })
    df.index.name = "Date"
    df.reset_index(inplace=True)
    df.dropna(inplace=True) # Remove rows with any missing values

    # Step 3: Load into SQL (ETL Pipeline)
    engine = create_engine(f"sqlite:///{DB_FILE}")
    df.to_sql("econ_data", engine, if_exists="replace", index=False)

    # Query aggregated yearly data
    query = """
    SELECT strftime('%Y', Date) AS Year,
           AVG(GDP) AS GDP,
           AVG(CPI) AS CPI,
           AVG(Unemployment) AS Unemployment
    FROM econ_data
    GROUP BY Year
    """
    yearly_data = pd.read_sql(query, engine)
    # Convert Year to integer for better plotting
    yearly_data['Year'] = yearly_data['Year'].astype(int)
    return yearly_data

# --- Streamlit Dashboard ---
st.set_page_config(page_title="US Economic Insights", layout="wide")

st.title("📊 US Economic Insights Dashboard")
st.write("Data sourced from FRED (Federal Reserve Economic Data).")

yearly_data = load_data()

if not yearly_data.empty:
    # Step 5: Build the Dashboard
    st.sidebar.header("Chart Controls")
    kpis = ["GDP", "CPI", "Unemployment"]
    
    selected_kpi = st.sidebar.selectbox("Choose a Key Performance Indicator (KPI):", kpis)

    st.header(f"{selected_kpi} Over Time")
    
    # Step 4: Interactive plot with Plotly
    fig = px.line(yearly_data, 
                  x="Year", 
                  y=selected_kpi, 
                  title=f"Annual US {selected_kpi} Over Time")
    fig.update_layout(xaxis_title="Year", yaxis_title=selected_kpi)
    st.plotly_chart(fig, use_container_width=True)

    # Display raw data table
    if st.checkbox("Show Raw Yearly Data"):
        st.dataframe(yearly_data)
else:
    st.warning("Could not load data. Please check your API key and network connection.")
