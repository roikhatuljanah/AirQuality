import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('main_data.csv')
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

df = load_data()

st.title('Air Quality Analysis in Beijing')

# Sidebar for user input
st.sidebar.header('User Input Parameters')
selected_station = st.sidebar.selectbox('Select Station', df['station'].unique())

# Main page
st.header('Overview of PM2.5 Levels')
st.write(df.groupby('station')['PM2.5'].describe())

# Visualization 1: Time series of PM2.5 levels
st.subheader('PM2.5 Levels Over Time')
fig, ax = plt.subplots(figsize=(12, 6))
df_station = df[df['station'] == selected_station]
ax.plot(df_station['datetime'], df_station['PM2.5'])
ax.set_title(f'PM2.5 Levels at {selected_station}')
ax.set_xlabel('Date')
ax.set_ylabel('PM2.5')
plt.xticks(rotation=45)
st.pyplot(fig)

# Visualization 2: Seasonal patterns
st.subheader('Seasonal Patterns of PM2.5')
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='season', y='PM2.5', data=df_station, ax=ax)
ax.set_title(f'PM2.5 Distribution by Season at {selected_station}')
st.pyplot(fig)

# Visualization 3: Correlation heatmap
st.subheader('Correlation between PM2.5 and Meteorological Factors')
corr_columns = ['PM2.5', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
corr_matrix = df_station[corr_columns].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Advanced Analysis: Clustering
st.header('Advanced Analysis: Clustering')
st.subheader('Clustering Results')
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(df_station['TEMP'], df_station['PM2.5'], c=df_station['cluster'], cmap='viridis')
ax.set_xlabel('Temperature')
ax.set_ylabel('PM2.5')
ax.set_title(f'Clustering of PM2.5 and Temperature at {selected_station}')
plt.colorbar(scatter)
st.pyplot(fig)

# Conclusions
st.header('Conclusions')
st.write("""
Based on the analysis:
1. PM2.5 levels show clear seasonal patterns, with higher levels typically observed in winter.
2. There is a correlation between PM2.5 levels and meteorological factors, particularly temperature and pressure.
3. Clustering analysis reveals distinct groups of air quality conditions, which could be related to different weather patterns or pollution sources.
""")

st.sidebar.info('This app provides an interactive analysis of air quality data in Beijing. Select a station from the dropdown to explore its specific data.')