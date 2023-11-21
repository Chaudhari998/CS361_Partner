import zmq
import requests

def fetch_weather_data(api_key, latitude, longitude):
    base_url = "http://api.weatherapi.com/v1"
    api_method = "/current.json"  # You can change this as needed
    url = f"{base_url}{api_method}?key={api_key}&q={latitude},{longitude}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
print("Weather server is running and listening for incoming requests...")

api_key = "8d650e3e351c44cca3830729232111"  # Replace with your actual API key

while True:
    # Receive message
    coordinates = socket.recv_json()
    print("Received coordinates: ", coordinates)

    # Fetch weather data using the received coordinates
    weather_data = fetch_weather_data(api_key, coordinates['latitude'], coordinates['longitude'])

    if weather_data:
        socket.send_json(weather_data)
    else:
        socket.send_string("Error fetching weather data")
