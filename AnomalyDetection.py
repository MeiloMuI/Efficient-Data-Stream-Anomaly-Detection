import random
import math
from collections import deque

# Parameters for data stream simulationß
stream_length = 700

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