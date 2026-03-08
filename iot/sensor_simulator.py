import random
import time
import requests
from datetime import datetime

API_URL = "http://localhost:8000/sensor-data"

MONUMENTS = ["Taj Mahal", "Qutub Minar", "Red Fort"]


def generate_sensor_data(monument):
    return {
        "monument": monument,
        "timestamp": datetime.now().isoformat(),
        "temperature": round(random.uniform(15, 45), 2),
        "humidity": round(random.uniform(30, 90), 2),
        "air_pollution": round(random.uniform(50, 400), 2),
        "vibration": round(random.uniform(0.1, 5.0), 3),
        "crack_width": round(random.uniform(0.0, 3.5), 2),
    }


def send_data(data):
    try:
        response = requests.post(API_URL, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")
        return False


def main():
    print("Starting IoT Sensor Simulator...")
    print(f"Sending data to: {API_URL}")
    print(f"Monitoring monuments: {', '.join(MONUMENTS)}")
    print("-" * 50)

    while True:
        for monument in MONUMENTS:
            data = generate_sensor_data(monument)
            
            print(f"\n[{data['timestamp']}] {monument}")
            print(f"  Temperature: {data['temperature']}°C")
            print(f"  Humidity: {data['humidity']}%")
            print(f"  Air Pollution: {data['air_pollution']} AQI")
            print(f"  Vibration: {data['vibration']} mm/s")
            print(f"  Crack Width: {data['crack_width']} mm")
            
            if send_data(data):
                print("  ✓ Data sent successfully")
            else:
                print("  ✗ Failed to send data")

        time.sleep(5)


if __name__ == "__main__":
    main()
