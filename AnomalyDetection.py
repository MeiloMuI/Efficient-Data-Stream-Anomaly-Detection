import random
import math
from collections import deque

# Parameters for data stream simulation
stream_length = 700
alpha = 0.1 # Smoothing factor for EMA, means that the current value has a lower influence on the EMA calculation.
threshold = 3   # Z-score threshold for anomaly detection
window_size = 50    # Size of rolling window for statistics

# Simulate the data stream with seasonality, trend, noise, and anomalies
def generate_data_stream():
    stream = []
    for i in range(stream_length):
        # Seasonality, it creates a sinusoidal wave that repeats every 50 time steps, with an amplitude of 10.
        seasonal = 10 * math.sin(2 * math.pi * i / 50)
        trend = 0.1 * i # Regular pattern
        noise = random.gauss(0, 2) # Random noise
        value = seasonal + trend + noise

        # Anomalies
        if random.random() < 0.05:
            value += random.choice([30, -30])
        stream.append(value)
    return stream

# Exponential Moving Average (EMA). 
# EMA can be used to track trends in cyclical fluctuations.
# EMA helps identify long-term trends by smoothing short-term fluctuations. When sudden changes occur in the data stream, EMA can quickly capture such changes and reflect them in a timely manner.
def calculate_ema(current_val, prev_ema, alpha):
    return alpha * current_val + (1 - alpha) * prev_ema

# Z-score
# Z-score can effectively identify outliers in new data environments, especially when concept drift occurs.
def calculate_z_score(value, mean, std_dev):
    if std_dev == 0:
        return 0
    return (value - mean) / std_dev

# Calculate mean and stand deviation of a window
def calculate_mean_std(window):
    n = len(window)
    if n == 0:
        return 0, 0
    mean = sum(window) / n
    variance = sum((x - mean) ** 2 for x in window) / n
    std_dev = math.sqrt(variance)
    return mean, std_dev

# Real-time anomaly detection
def detect_anomalies(data_stream, window_size, alpha, threshold):
    rolling_window = deque(maxlen=window_size)
    ema = data_stream[0] # Initialize EMA with the first data point

    for index, value in enumerate(data_stream):
        rolling_window.append(value)

        # Get rolling mean and std_dev
        rolling_mean, rolling_std = calculate_mean_std(rolling_window)
        # 2 times the rolling standard deviation
        ema_threshold = 2 * rolling_std  
        # Update EMA
        ema = calculate_ema(value, ema, alpha)
        # Get Z-score for anomaly detection
        z_score = calculate_z_score(value, rolling_mean, rolling_std)

        new_anomalies = []
        # Flag as anomaly if Z-score exceeds threshold
        if abs(z_score) > threshold:
            new_anomalies.append((index, value, "z-score anomaly"))
        # Flag as anomaly if ema exceeds threshold
        if abs(value - ema) > ema_threshold:
            new_anomalies.append((index, value, "EMA anomaly"))

        yield index, value, ema, rolling_mean, rolling_std, new_anomalies

# Simple text-based visualization function
def visualize_data_stream(index, value, is_anomaly):
    if is_anomaly:
        print(f"Time {index}: {value} (ANOMALY)")
    else:
        print(f"Time {index}: {value}")

# Main function
def main():
    # Generate the data stream
    data_stream = generate_data_stream()

    # Detection of anomalies
    anomalies = set()
    detected_anomalies = detect_anomalies(data_stream, window_size, alpha, threshold)

    # Collect anomalies for visualization and visualize the result
    print("Data Stream (with anomalies marked):")
    for index, value, ema, rolling_mean, rolling_std, new_anomalies in detected_anomalies:
        if new_anomalies:
            anomalies.update(new_anomalies)
            visualize_data_stream(index, value, True)
        else:
            visualize_data_stream(index, value, False)

if __name__ == '__main__':
    main()
