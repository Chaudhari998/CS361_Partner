import zmq
import json

def read_coordinates_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data

context = zmq.Context()
print("Connecting to the weather server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Read coordinates from the JSON file
coordinates = read_coordinates_from_file("location_data.json")

print(f"Sending coordinates to the server: {coordinates}")
socket.send_json(coordinates)

# Wait for the response from the server
message = socket.recv()
print("Received reply from server: ")
print(message.decode())
