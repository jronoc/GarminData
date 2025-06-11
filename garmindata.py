from google import genai

# importing os module for environment variables
import os
import pandas as pd
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 


client = genai.Client(api_key="AIzaSyCZZGB6bJm7DmFXWOLlKbgfhONQSsqvLXc")


#From last chatgpt

# Load CSV
df = pd.read_csv("./Garmindata.csv")

# Clean column names
df.columns = df.columns.str.strip().str.replace('®', '', regex=False)

# Filter running activities
df = df[df["Activity Type"].str.contains("Run", na=False)]

# Convert "Avg Pace" to float (minutes)
def pace_to_float(pace_str):
    try:
        if isinstance(pace_str, str) and ":" in pace_str:
            mins, secs = pace_str.split(":")
            return int(mins) + int(secs) / 60
    except:
        return None
    return None

df["Avg Pace"] = df["Avg Pace"].apply(pace_to_float)
df = df.dropna(subset=["Avg Pace"])

# Convert "Time" to timedelta
df["Time"] = pd.to_timedelta(df["Time"], errors='coerce')
df = df.dropna(subset=["Time"])

# Get last 5 runs
recent = df.tail(5)

# Compute stats
avg_pace = recent["Avg Pace"].mean()
avg_hr = recent["Avg HR"].mean()
total_distance = recent["Distance"].sum()
avg_time = recent["Time"].mean()


prompt = f"""Please generate a personalized 2-week training and recovery plan that minimizes knee strain but improves endurance. based on the following data from my last 5 runs:

- Total distance over 5 runs: {total_distance} km
- Average time per run: {avg_time} 
- Average pace (last 5 runs): {avg_pace}
- Average heart rate (last 5 runs): {avg_hr}
"""
response = client.models.generate_content(
model="gemini-2.0-flash",
contents=prompt,
 )

print(response.text)
