import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image
sns.set(style='dark')

day_df = pd.read_csv("/content/drive/MyDrive/Dicoding/day_clean.csv")
hour_df = pd.read_csv("/content/drive/MyDrive/Dicoding/hour_clean.csv")

def create_monthly_sharing_df(df):
  monthly_sharing_df = df.resample(rule = "M", on = "date").agg({
    "casual" : "sum",
    "registered" : "sum",
    "count" : "sum"
  })
  monthly_sharing_df.index = monthly_sharing_df.index.strftime("%B-%Y")
  monthly_sharing_df = monthly_sharing_df.reset_index()

  return monthly_sharing_df

def create_consument_distribution_df(df):
  consument_distribution_df = df.groupby(by = "weekday").agg({
    "casual" : "sum",
    "registered" : "sum"
  }).sort_values(by = ["casual", "registered"], ascending = False).reset_index()
  grouped_df = consument_distribution_df.groupby("weekday")[["casual", "registered"]].sum()

  return grouped_df

def create_total_consument_df(df):
  total_casual = df["casual"].sum()
  total_registered = df["registered"].sum()
  total_combine = df["casual"].sum() + df["registered"].sum()
  total_consument_df = {
      "category" : ["casual", "registered", "combine"],
      "total" : [total_casual, total_registered, total_combine]
  }

  return total_consument_df

def create_holiday_sharing_df(df):
  holiday_sharing_df = df.groupby(by = "holiday").agg({
    "casual" : "sum",
    "registered" : "sum",
    "count" : "sum"
  }).reset_index()
  holiday_data_df = holiday_sharing_df.groupby("holiday")[["casual", "registered"]].sum()

  return holiday_data_df

def create_working_sharing_df(df):
  working_sharing_df = df.groupby(by = "workingday").agg({
    "casual" : "sum",
    "registered" : "sum",
    "count" : "sum"
  }).reset_index()
  working_data_df = working_sharing_df.groupby("workingday")[["casual", "registered"]].sum()

  return working_data_df

def create_hour_sharing_df(df):
  hour_sharing_df = df.groupby(by = "hour").agg({
    "casual" : "sum",
    "registered" : "sum",
    "count" : "sum"
  }).reset_index()

  return hour_sharing_df

def create_season_df(df):
  season_df = df.groupby(by = "season")["count"].sum().sort_values(ascending=False).reset_index()

  return season_df

def create_weather_df(df):
  weather_df = df.groupby(by = "weathersit")["count"].sum().sort_values(ascending=False).reset_index()

  return weather_df

def create_weather_parameter_df(df):
  weather_parameter_df = df.groupby(by = ["temperature", "atemp", "humidity", "windspeed"]).agg({
    "count" : "sum"
  }).reset_index()

  return weather_parameter_df

# hour_clean_merged = hour_df.groupby("date").sum().reset_index()
datetime_column = "date"

day_df.sort_values(by=datetime_column, inplace=True)
hour_df.sort_values(by=datetime_column, inplace=True)

day_df[datetime_column] = pd.to_datetime(day_df[datetime_column])
hour_df[datetime_column] = pd.to_datetime(hour_df[datetime_column])

min_date = min(day_df[datetime_column].min(), hour_df[datetime_column].min())
max_date = max(day_df[datetime_column].max(), hour_df[datetime_column].max())

with st.sidebar:
    #image = Image.open("/content/logo.png")
    st.image("https://raw.githubusercontent.com/rajainal/Bike-Sharing-Dataset-Analysis/main/dashboard/logo.png")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

day_date = day_df[(day_df[datetime_column] >= start_date) & (day_df[datetime_column] <= end_date)]
hour_date = hour_df[(hour_df[datetime_column] >= start_date) & (hour_df[datetime_column] <= end_date)]

monthly_sharing_df = create_monthly_sharing_df(day_date)
grouped_df = create_consument_distribution_df(day_date)
total_consument_df = create_total_consument_df(day_date)
holiday_data_df = create_holiday_sharing_df(day_date)
working_data_df = create_working_sharing_df(day_date)

hour_sharing_df = create_hour_sharing_df(hour_date)
season_df = create_season_df(hour_date)
weather_df = create_weather_df(hour_date)
weather_parameter_df = create_weather_parameter_df(hour_date)

st.header('Capital BikeShare Dashboard :sparkles:')

st.subheader('Monthly Bike Use')
 
col1, col2, col3 = st.columns(3)

with col1:
  total_casual = monthly_sharing_df["casual"].sum()
  st.metric("Casual user", value = total_casual)

with col2:
  total_registered = monthly_sharing_df["registered"].sum()
  st.metric("Registered user", value = total_registered)

with col3:
  total_count = monthly_sharing_df["count"].sum()
  st.metric("Casual + Registered user", value = total_count)

col1, col2 = st.columns(2)

with col1:
  fig, ax = plt.subplots(figsize=(10, 5))
  ax.plot(monthly_sharing_df["date"], monthly_sharing_df["count"], marker = "o", linewidth = 2, color = "purple")
  ax.set_title("Number of Sharings per Month (2021) to (2012)", loc = "center", fontsize = 20)
  ax.tick_params(axis = 'x', labelsize = 10, rotation = 90)
  ax.tick_params(axis = 'y', labelsize = 10)
  st.pyplot(fig)

with col2:
  fig2, ax2 = plt.subplots(figsize=(10, 5))
  ax2.plot(monthly_sharing_df["date"], monthly_sharing_df["casual"], marker = "o", linewidth = 2, color = "green", label = "casual")
  ax2.plot(monthly_sharing_df["date"], monthly_sharing_df["registered"], marker = "o", linewidth = 2, color = "red", label = "registered")
  ax2.set_title("Number of Sharings per Month by Category (2021) to (2012)", loc = "center", fontsize = 17)
  ax2.tick_params(axis = 'x', labelsize = 10, rotation = 90)
  ax2.tick_params(axis = 'y', labelsize = 10)
  ax2.legend()
  st.pyplot(fig2)

st.subheader('Hourly Bike Use')

col1, col2 = st.columns(2)

with col1:
  fig, ax = plt.subplots(figsize=(10, 5))
  ax.plot(hour_sharing_df["hour"], hour_sharing_df["count"], marker = "o", linewidth = 2, color = "purple")
  ax.set_title("Number of Sharings per Hour", loc = "center", fontsize = 20)
  ax.set_xticks(hour_sharing_df["hour"])
  ax.tick_params(axis = "x", labelsize = 10)
  ax.tick_params(labelsize = 10)
  st.pyplot(fig)

with col2:
  fig2, ax2 = plt.subplots(figsize=(10, 5))
  ax2.plot(hour_sharing_df["hour"], hour_sharing_df["casual"], marker = "o", linewidth = 2, color = "green", label = "casual")
  ax2.plot(hour_sharing_df["hour"], hour_sharing_df["registered"], marker = "o", linewidth = 2, color = "red", label = "registered")
  ax2.set_title("Number of Sharings per Hour by Category", loc = "center", fontsize = 20)
  ax2.set_xticks(hour_sharing_df["hour"])
  ax2.tick_params(axis = 'x', labelsize = 10)
  ax2.tick_params(axis = 'y', labelsize = 10)
  ax2.legend()
  st.pyplot(fig2)

st.subheader("Holiday and Workingday Bike Use")

col1, col2 = st.columns(2)

with col1:
  fig, ax = plt.subplots()
  holiday_data_df.plot(kind = "bar", color = ["green", "red"], ax = ax)
  plt.xlabel("Holiday")
  plt.ylabel("Total")
  plt.title("Total Casual and Registered by Holiday")
  plt.xticks(rotation = 0)
  ax.legend(["Casual", "Registered"])
  st.pyplot(fig)

with col2:
  fig2, ax = plt.subplots()
  working_data_df.plot(kind = "bar", color = ["green", "red"], ax = ax)
  plt.xlabel("Workingday")
  plt.ylabel("Total")
  plt.title("Total Casual and Registered by Workingday")
  plt.xticks(rotation = 0)
  ax.legend(["Casual", "Registered"])
  st.pyplot(fig2)

st.subheader("Bike Use Every Day and Consument Type Distribution")

col1, col2 = st.columns(2)

with col1:
  fig, ax = plt.subplots()
  grouped_df.plot(kind = "bar", color = ["green", "red"], ax = ax)
  plt.xlabel("Weekday")
  plt.ylabel("Total")
  plt.title("Total Casual and Registered per Weekday")
  plt.xticks(rotation = 45)
  ax.legend(["Casual", "Registered"])
  st.pyplot(fig)

with col2:
  fig2, ax = plt.subplots()
  ax.bar(total_consument_df["category"], total_consument_df["total"], color=["green", "red", "purple"])
  ax.set_xlabel("Category")
  ax.set_ylabel("Total")
  ax.set_title("Consument Type Distribution")
  st.pyplot(fig2)

st.subheader("The Influence of Seasons and Weather on Bike Use")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="count", y="season", data=season_df, palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Season", loc="center", fontsize=15)
ax[0].tick_params(axis='y', labelsize=12)

sns.barplot(x="count", y="weathersit", data=weather_df, palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("By Weather", loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)

plt.suptitle("Best and Worst Bike Sharing by Season and Weather", fontsize=20)
st.pyplot(fig)

st.subheader("The Influence of Weather Parameters on Bike Use")

fig, axs = plt.subplots(2, 2, figsize=(10, 8))

colors = ['green', 'yellow', 'red', 'blue']

axs[0, 0].scatter(weather_parameter_df['temperature'], weather_parameter_df['count'], color=colors[0], alpha=0.5)
axs[0, 0].set_title('Temperature vs Count')

axs[0, 1].scatter(weather_parameter_df['atemp'], weather_parameter_df['count'], color=colors[1], alpha=0.5)
axs[0, 1].set_title('Atemp vs Count')

axs[1, 0].scatter(weather_parameter_df['humidity'], weather_parameter_df['count'], color=colors[2], alpha=0.5)
axs[1, 0].set_title('Humidity vs Count')

axs[1, 1].scatter(weather_parameter_df['windspeed'], weather_parameter_df['count'], color=colors[3], alpha=0.5)
axs[1, 1].set_title('Windspeed vs Count')

plt.suptitle('Weather Parameters vs Count', fontsize=16)
plt.tight_layout()
st.pyplot(fig)