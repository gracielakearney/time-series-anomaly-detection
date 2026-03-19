import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest


# Cargar datos
df = pd.read_csv("time_series.csv")

# Convertir columnas
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")

# Feature engineering
df["lag_1"] = df["value"].shift(1)
df["rolling_mean"] = df["value"].rolling(3).mean()
df["rolling_std"] = df["value"].rolling(3).std()

df = df.dropna()

# Modelo
model = IsolationForest(contamination=0.05, random_state=42)
df["anomaly"] = model.fit_predict(df[["value", "lag_1", "rolling_mean", "rolling_std"]])

# Visualización
plt.figure(figsize=(10,5))
plt.plot(df["timestamp"], df["value"], label="Serie")
plt.scatter(df[df["anomaly"]==-1]["timestamp"],
            df[df["anomaly"]==-1]["value"],
            label="Anomalías")

plt.legend()
plt.title("Anomaly Detection")
plt.show()
