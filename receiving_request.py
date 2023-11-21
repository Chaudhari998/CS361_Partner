import zmq
import requests

def fetch_weather_data(api_key, latitude, longitude):
    """Fetch weather data from the WeatherAPI."""
    base_url = "http://api.weatherapi.com/v1"
    api_method = "/current.json"
    url = f"{base_url}{api_method}?key={api_key}&q={latitude},{longitude}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def setup_server(port):
    """Setup the ZMQ server."""
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")
    print(f"Weather server is running and listening on port {port}...")
    return socket

def server_loop(socket, api_key):
    """The main server loop that handles incoming requests."""
    while True:
        coordinates = socket.recv_json()
        print("Received coordinates: ", coordinates)
        weather_data = fetch_weather_data(api_key, coordinates['latitude'], coordinates['longitude'])
        if weather_data:
            socket.send_json(weather_data)
        else:
            socket.send_string("Error fetching weather data")

def main(server_config):
    """Main function to execute the server workflow."""
    socket = setup_server(server_config['port'])
    server_loop(socket, server_config['api_key'])

if __name__ == "__main__":
    server_config = {
        'port': 5555,
        'api_key': "8d650e3e351c44cca3830729232111"  
    }
    main(server_config)
