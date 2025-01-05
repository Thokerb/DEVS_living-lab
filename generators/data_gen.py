import numpy as np
import math

from livingLab.util.experiment_constants import SUNRISE, SUNSET, MAX_DNI


def simulate_dni(sunrise, sunset):
    """
    Simulate DNI values across a day.

    Parameters:
        sunrise (float): Time of sunrise in hours (e.g., 6.0 for 6:00 AM).
        sunset (float): Time of sunset in hours (e.g., 18.0 for 6:00 PM).

    Returns:
        np.ndarray: Array of 24*60 entries representing DNI values.
    """
    # Number of minutes in a day
    minutes_per_day = 24 * 60

    # Create an array representing each minute of the day
    dni = np.zeros(minutes_per_day)

    # Convert sunrise and sunset to minute indices
    sunrise_idx = (sunrise * 60.0)
    sunset_idx = (sunset * 60.0)

    # Define the time range of active DNI
    active_minutes = np.arange(sunrise_idx, sunset_idx)
    # active minutes to int array
    active_minutes = active_minutes.astype(int)

    # Simulate DNI values using a sine wave for a natural curve
    peak_dni = MAX_DNI  # Define peak DNI value (in W/m^2)

    if sunset_idx > sunrise_idx:
        for t in active_minutes:
            # Normalize time within the active range
            normalized_time = (t - sunrise_idx) / (sunset_idx - sunrise_idx)
            # Use a sine curve to simulate the DNI distribution
            dni[t] = peak_dni * math.sin(normalized_time * math.pi)

    return dni

#plot dni values
import matplotlib.pyplot as plt

dni_values = simulate_dni(SUNRISE, SUNSET)

plt.figure(figsize=(10, 6))
plt.plot(dni_values)
plt.xlabel("Time (minutes)")
plt.ylabel("DNI (W/m^2)")
plt.title("Daily DNI Profile")
plt.grid(True)
plt.show()
