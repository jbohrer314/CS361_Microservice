import requests
import json
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")

API_KEY = "" # Fill in here

cache = {}

def makeURL(title: str, year: str):
    tokens = title.split(" ")
    urlTitle = "+".join(tokens)
    
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={urlTitle}&y={year}"
    return url


while True:
    # Wait for message
    print("Waiting for message...")
    message = socket.recv()
    messageData = json.loads(message)

    # Generate request url
    try:
        url = makeURL(messageData["Title"], messageData["Year"])
    except KeyError:
        url = makeURL(messageData["Title"], "")
    
    # Query cache for information, if not there request from API
    if url in cache.keys():
        print("from cache")
        response = cache[url]
    else:
        print("from API")
        response = requests.get(url)
        cache[url] = response

    # Get data from response
    data = response.json()
    statusCode = response.status_code

    # Logging messages
    print(url)
    print(statusCode)
    print(json.dumps(data, indent=2))

    # Send Response
    socket.send_json(data)


