import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import io
import requests
from google.colab import files

# Upload data
uploaded = files.upload()

# Read data
df = pd.read_csv(io.StringIO(uploaded['Unemployment_Rate_upto_11_2020.csv'].decode('utf-8')))

# Check for missing values
print(df.isnull().sum())

# Rename columns
df = df.rename(columns={
    df.columns[0]: 'State',
    df.columns[3]: 'EUR',
    df.columns[4]: 'EE',
    df.columns[5]: 'ELPR',
    df.columns[6]: 'Region'
})

# Explore unique values and group sizes
print(df["State"].nunique())
print(df["Region"].nunique())
print(df.groupby("Region").size())

# Calculate mean unemployment rates by region
region_stats = df.groupby(['Region'])[['EUR','EE','ELPR']].mean().round(2).reset_index()
print(region_stats)

# Create correlation heatmap
heat_maps = df[['EUR','EE', 'ELPR','longitude', 'latitude']].corr()
plt.figure(figsize=(10,6))
sns.set_context('notebook',font_scale=1)
sns.heatmap(heat_maps, annot=True,cmap='summer')
plt.show()

# Plot unemployment rate distribution by region
df.columns = ["State","Date","Frequency","EUR","EE","ELPR","Region","longitude","latitude"]
plt.figure(figsize=(10, 8))
plt.title("Unemployment Rate")
sns.histplot(x="EUR", hue="Region", data=df)
plt.show()

# Visualize average unemployment rate by region using bar chart
region = df.groupby(["Region"])[['EUR', "EE", "ELPR"]].mean().reset_index()
fig = px.bar(region, x="Region", y="EUR", color="Region", title="Average Unemployment Rate by Region")
fig.update_layout(xaxis={'categoryorder':'total descending'})
fig.show()

# Visualize unemployment rate by state and region using sunburst chart
unemployment = df[["State", "Region", "EUR"]]
fig = px.sunburst(unemployment, path=['Region','State'], values='EUR',
                  title='Unemployment rate in every State and Region', height=650)
fig.show()

