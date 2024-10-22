import random
import math
from collections import deque

# Parameters for data stream simulation
stream_length = 700
alpha = 0.1 # Smoothing factor for EMA
threshold = 3   # Z-score threshold for anomaly detection
window_size = 50    # Size of rolling window for statistics

# Simulate the data stream with seasonality, trend, noise, and anomalies
def generate_data_stream():
    stream = []
    for i in range(stream_length):
        seasonal = 10 * math.sin(2 * math.pi * i / 50) # Seasonality, it creates a sinusoidal wave that repeats every 50 time steps, with an amplitude of 10.
        trend = 0.1 * i # Regular pattern
        noise = random.gauss(0, 2) # Random noise
        value = seasonal + trend + noise

        # Anomalies
        if random.random() < 0.05:
            value += random.choice([30, -30])
        stream.append(value)
    return stream

# Exponential Moving Average (EMA)
def calculate_ema(current_val, prev_ema, alpha):
    return alpha * current_val + (1 - alpha) * prev_ema

# Z-score
def calculate_z_score(value, mean, std_dev):
    if std_dev == 0:
        return 0
    return (value - mean) / std_dev

# Real-time anomaly detection
def detect_anomalies(data_stream, window_size, alpha, threshold):
    rolling_window = deque(maxlen=window_size)
    anomalies = []
    ema = data_stream[0] # Initialize EMA with the first data point

    for i, value in enumerate(data_stream):
        rolling_window.append(value)

        # Get rolling mean and std_dev
        rolling_mean, rolling_std = calculate_mean_std(rolling_window)
        # Update EMA
        ema = calculate_ema(value, ema, alpha)
        # Get Z-score for anomaly detection
        z_score = calculate_z_score(value, rolling_mean, rolling_std)

        # Flag as anomaly if Z-score exceeds threshold
        if abs(z_score) > threshold:
            anomalies.append((i, value))

        yield value, ema, rolling_mean, rolling_std, anomalies
