import streamlit as st
import pandas as pd
import plotly.express as px

# Load Dataset
df = pd.read_csv("airline_cleaned.csv")  # replace filename if needed
df['route'] = df['source_city'] + " → " + df['destination_city']

# Streamlit Page Config
st.set_page_config(page_title="✈ Airline Ticket Price Dashboard", layout="wide")

# Title
st.title("✈ Airline Ticket Price Analysis")
st.markdown("Interactive exploration of airline ticket pricing patterns.")

# Sidebar Filters
st.sidebar.header("Filters")
airlines = st.sidebar.multiselect("Select Airlines:", df['airline'].unique(), default=df['airline'].unique())
routes = st.sidebar.multiselect("Select Routes:", df['route'].unique(), default=df['route'].unique())
classes = st.sidebar.multiselect("Select Classes:", df['class'].unique(), default=df['class'].unique())

# Filter Data
filtered_df = df[
    (df['airline'].isin(airlines)) &
    (df['route'].isin(routes)) &
    (df['class'].isin(classes))
]

# KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Flights", filtered_df.shape[0])
col2.metric("Average Price", f"{filtered_df['price'].mean():,.0f}")
col3.metric("Average Duration (hrs)", round(filtered_df['duration'].mean(), 2))

# --------------------
# Row 1: Price Distribution + Price vs Days Left
# --------------------
col4, col5 = st.columns(2)
with col4:
    fig_price = px.histogram(filtered_df, x='price', nbins=40, color='airline',
                             title="Price Distribution by Airline")
    st.plotly_chart(fig_price, use_container_width=True)
with col5:
    fig_days = px.scatter(filtered_df, x='days_left', y='price', color='airline',
                          title="Price vs Days Before Departure", opacity=0.6)
    st.plotly_chart(fig_days, use_container_width=True)

# --------------------
# Row 2: Top 15 Expensive Routes (full width)
# --------------------
fig_route = px.bar(
    filtered_df.groupby('route', as_index=False)['price']
               .mean()
               .sort_values('price', ascending=False)
               .head(15),
    x='price', y='route', orientation='h',
    title="Top 15 Most Expensive Routes",
    color='price', color_continuous_scale='RdYlGn'
)
st.plotly_chart(fig_route, use_container_width=True)

# --------------------
# Row 3: Price by Class + Price by Stops
# --------------------
col6, col7 = st.columns(2)
with col6:
    fig_class = px.box(filtered_df, x='class', y='price', color='class',
                       title="Price by Travel Class")
    st.plotly_chart(fig_class, use_container_width=True)
with col7:
    fig_stops = px.box(filtered_df, x='stops', y='price', color='stops',
                       title="Price by Number of Stops")
    st.plotly_chart(fig_stops, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Data Source: Internal Airline Dataset | Dashboard built with **Streamlit** & **Plotly**")
