import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")

# Create request dictionary
request = {"Title": "Mission Impossible", "Year": "1996"}
# request = {"Title": "Finding Nemo"}

# Convert dictionary to string format
requestString = json.dumps(request)

# Send string
socket.send_string(requestString)

# Wait for response and decode to string
message = socket.recv().decode()

# Print message
print(json.dumps(json.loads(message), indent=2))