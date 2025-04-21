import time
import requests

# Putanje do senzora (levi i desni)
SENSOR_PATHS = {
    "rightChamber": "/sys/bus/w1/devices/28-3ce0f6497f97/w1_slave",
    "leftChamber": "/sys/bus/w1/devices/28-3ce1e380aa99/w1_slave"
}

# API URL
API_URL = "https://susaraapi.edinmesan.ba/api/temperatures"

def read_temp(sensor_path):
    """Čita temperaturu sa senzora."""
    try:
        with open(sensor_path, 'r') as file:
            lines = file.readlines()
            if "YES" in lines[0]:
                temp_data = lines[1].split("t=")[-1]
                return float(temp_data) / 1000.0
            else:
                return None
    except FileNotFoundError:
        return None

def send_to_api(left_temp, right_temp):
    """Šalje podatke na API."""
    data = {
        "leftChamber": left_temp,
        "rightChamber": right_temp
    }
    try:
        response = requests.post(API_URL, json=data)
        response.raise_for_status()
        print(f"Podaci uspešno poslati: {data}")
    except requests.RequestException as e:
        print(f"Greška pri slanju podataka: {e}")

while True:
    print("\n--- Čitanje temperatura ---")
    temperatures = {}
    for chamber, path in SENSOR_PATHS.items():
        temperature = read_temp(path)
        if temperature is not None:
            temperatures[chamber] = round(temperature)
            print(f"{chamber}: {temperature:.2f}°C")
        else:
            print(f"{chamber}: Neuspelo čitanje temperature")

    if "leftChamber" in temperatures and "rightChamber" in temperatures:
        send_to_api(temperatures["leftChamber"], temperatures["rightChamber"])

    time.sleep(120)  # Pauza od 5 minuta





