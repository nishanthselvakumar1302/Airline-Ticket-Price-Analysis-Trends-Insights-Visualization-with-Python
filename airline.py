import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv("airline_cleaned.csv")

# ==============================
# APP CONFIG
# ==============================
st.set_page_config(page_title="✈ Airline Ticket Price Dashboard", layout="wide")

# ==============================
# STYLES
# ==============================
st.markdown(
    """
    <style>
        .kpi-card {
            background: #ffffff;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            text-align: center;
            margin: 10px;
        }
        .kpi-label {
            font-size: 1rem;
            font-weight: 600;
            color: #374151;
            margin-bottom: 8px;
        }
        .kpi-value {
            font-size: 1.8rem;
            font-weight: 800;
            color: #111827;
        }
        .kpi-icon {
            font-size: 2rem;
            margin-bottom: 6px;
        }
        .streamlit-expanderHeader {
            font-weight: 700 !important;
            font-size: 1.1rem !important;
        }
        .streamlit-expanderContent {
            background: #f9f9f9;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
            margin-bottom: 15px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("✈ Airline Ticket Price Dashboard")

# ==============================
# SLICERS
# ==============================
with st.expander("🎛 Filters / Slicers", expanded=True):
    st.markdown("Adjust the slicers below to filter your dashboard:")

    c1, c2, c3 = st.columns(3)

    with c1:
        airline_slicer = st.multiselect(
            "✈️ Airline", ["All"] + df["airline"].unique().tolist(), default=["All"]
        )

    with c2:
        source_slicer = st.selectbox(
            "🏙️ Source City", ["All"] + sorted(df["source_city"].unique().tolist())
        )

    with c3:
        dest_slicer = st.selectbox(
            "📍 Destination City", ["All"] + sorted(df["destination_city"].unique().tolist())
        )

    c4, c5 = st.columns(2)

    with c4:
        class_slicer = st.selectbox("💺 Class", ["All"] + sorted(df["class"].unique().tolist()))

    with c5:
        stops_slicer = st.selectbox("🛑 Stops", ["All"] + sorted(df["stops"].unique().tolist()))

    c6, c7 = st.columns(2)

    with c6:
        days_range = st.slider(
            "📆 Days Left",
            int(df["days_left"].min()),
            int(df["days_left"].max()),
            (int(df["days_left"].min()), int(df["days_left"].max()))
        )

    with c7:
        price_range = st.slider(
            "💰 Ticket Price",
            int(df["price"].min()),
            int(df["price"].max()),
            (int(df["price"].min()), int(df["price"].max()))
        )

# ==============================
# APPLY FILTERS
# ==============================
f = df.copy()

if "All" not in airline_slicer:
    f = f[f["airline"].isin(airline_slicer)]
if source_slicer != "All":
    f = f[f["source_city"] == source_slicer]
if dest_slicer != "All":
    f = f[f["destination_city"] == dest_slicer]
if class_slicer != "All":
    f = f[f["class"] == class_slicer]
if stops_slicer != "All":
    f = f[f["stops"] == stops_slicer]

f = f[f["days_left"].between(days_range[0], days_range[1])]
f = f[f["price"].between(price_range[0], price_range[1])]

if f.empty:
    st.warning("No records match your current filters. Try widening the ranges or selecting more values.")
    st.stop()

# ==============================
# KPI CARDS
# ==============================
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">✈️</div>
            <div class="kpi-label">Total Flights</div>
            <div class="kpi-value">{len(f):,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Average Price</div>
            <div class="kpi-value">₹{f["price"].mean():,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">📆</div>
            <div class="kpi-label">Avg Days Left</div>
            <div class="kpi-value">{f["days_left"].mean():.1f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">⏱️</div>
            <div class="kpi-label">Avg Duration (hrs)</div>
            <div class="kpi-value">{f["duration"].mean():.1f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==============================
# DASHBOARD LAYOUT
# ==============================

# Row 1
r1c1, r1c2 = st.columns(2)

with r1c1:
    st.subheader("Average Price by Airline")
    fig = px.bar(f.groupby("airline", as_index=False)["price"].mean(),
                 x="airline", y="price", color="price", color_continuous_scale="viridis")
    st.plotly_chart(fig, use_container_width=True)

with r1c2:
    st.subheader("Average Price by Class")
    fig = px.bar(f.groupby("class", as_index=False)["price"].mean(),
                 x="class", y="price", color="price", color_continuous_scale="plasma")
    st.plotly_chart(fig, use_container_width=True)

# Row 2
st.subheader("Average Price Heatmap: Source vs Destination")
heat = f.groupby(["source_city", "destination_city"], as_index=False)["price"].mean()
pivot = heat.pivot(index="source_city", columns="destination_city", values="price")
fig = px.imshow(pivot, aspect="auto", origin="lower",
                labels=dict(color="Avg Price"),
                title="Source → Destination: Average Ticket Price")
st.plotly_chart(fig, use_container_width=True)

# Row 3
r3c1, r3c2 = st.columns(2)

with r3c1:
    st.subheader("Price Distribution")
    fig = px.histogram(f, x="price", nbins=40, color="class")
    st.plotly_chart(fig, use_container_width=True)

with r3c2:
    st.subheader("Flights by Days Left")
    fig = px.box(f, x="class", y="days_left", color="class")
    st.plotly_chart(fig, use_container_width=True)

# Row 4 → Route Map
st.subheader("Flight Route Map")

coords = {
    "Delhi": [28.7041, 77.1025],
    "Mumbai": [19.0760, 72.8777],
    "Bangalore": [12.9716, 77.5946],
    "Hyderabad": [17.3850, 78.4867],
    "Kolkata": [22.5726, 88.3639],
    "Chennai": [13.0827, 80.2707]
}

map_df = f.groupby(["source_city", "destination_city"]).size().reset_index(name="flights")
map_df["source_lat"] = map_df["source_city"].map(lambda x: coords.get(x, [None, None])[0])
map_df["source_lon"] = map_df["source_city"].map(lambda x: coords.get(x, [None, None])[1])
map_df["dest_lat"] = map_df["destination_city"].map(lambda x: coords.get(x, [None, None])[0])
map_df["dest_lon"] = map_df["destination_city"].map(lambda x: coords.get(x, [None, None])[1])
map_df = map_df.dropna()

if not map_df.empty:
    fig = px.scatter_mapbox(map_df,
                            lat="source_lat", lon="source_lon",
                            size="flights", hover_name="source_city",
                            zoom=3, mapbox_style="carto-darkmatter")
    for _, row in map_df.iterrows():
        fig.add_scattermapbox(
            lat=[row["source_lat"], row["dest_lat"]],
            lon=[row["source_lon"], row["dest_lon"]],
            mode="lines",
            line=dict(width=2, color="blue"),
            showlegend=False
        )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No route data available for selected filters.")
