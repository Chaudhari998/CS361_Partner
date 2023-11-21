import zmq
import json

def load_coordinates(file_path):
    """Load coordinates from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def send_request(socket, data):
    """Send a request to the server."""
    print(f"Sending coordinates to the server: {data}")
    socket.send_json(data)

def receive_response(socket):
    """Receive a response from the server."""
    message = socket.recv()
    print("Received reply from server: ")
    print(message.decode())

def main(client_config):
    """Main function to execute the client workflow."""
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(client_config['server_address'])

    coordinates = load_coordinates(client_config['location_data_file'])
    send_request(socket, coordinates)
    receive_response(socket)

if __name__ == "__main__":
    client_config = {
        'server_address': "tcp://localhost:5555",
        'location_data_file': "location_data.json"
    }
    main(client_config)
