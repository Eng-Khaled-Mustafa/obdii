import streamlit as st
import random
from datetime import datetime
import pandas as pd

# Simulate OBD-II data for a bus
def simulate_obd_data(bus_id):
    return {
        "Bus ID": bus_id,
        "Timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "Speed (km/h)": random.randint(0, 120),
        "Engine Temp (°C)": random.randint(70, 120),
        "RPM": random.randint(700, 4000),
        "Fuel Level (%)": round(random.uniform(5, 100), 1),
        "Odometer (km)": random.randint(20000, 500000),
        "DTC Code": random.choice([None, "P0300", "P0420", "P0171", None, None])
    }

# Assign priority weight based on data
def calculate_weight(row):
    weight = 0
    if row["Engine Temp (°C)"] > 100:
        weight += 30
    if row["Fuel Level (%)"] < 15:
        weight += 10
    if row["Odometer (km)"] > 300000:
        weight += 20
    if row["DTC Code"]:
        weight += 50
    return weight

# UI layout
st.set_page_config(page_title="Bus OBD-II Simulation", layout="wide")
st.title("🚌 Bus Fleet - OBD-II Data & Priority Weights")

# Sidebar
bus_count = st.sidebar.slider("Number of Buses", min_value=10, max_value=150, value=100)
refresh = st.sidebar.button("🔁 Refresh Simulation")

# Main simulation
data = [simulate_obd_data(f"BUS-{i:03}") for i in range(1, bus_count + 1)]
df = pd.DataFrame(data)
df["Weight"] = df.apply(calculate_weight, axis=1)
df = df.sort_values("Weight", ascending=False)

# Display table
st.dataframe(df, use_container_width=True)

# Optional: show only top N
top_n = st.sidebar.slider("Show Top N Priority Buses", min_value=5, max_value=bus_count, value=20)
st.subheader(f"🚨 Top {top_n} Priority Buses")
st.table(df.head(top_n))
