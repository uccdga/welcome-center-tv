from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import threading
import time
import schedule

app = Flask(__name__)
CORS(app)
EVENTS_FILE = "events.json"

def load_events():
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, "r") as file:
            return json.load(file)
    return []

def save_events(events):
    with open(EVENTS_FILE, "w") as file:
        json.dump(events, file, indent=4)

def execute_event(event):
    print(f"Executing event: {event}")
    tv_id = '0'
    # execute "echo {commands[event['action']]} {tv_id}" as a system process
    if event["action"] == "on":
        os.system(f"./kiosk.sh {event['url']}")
        # save the URL to a file
        with open("current_url.txt", "w") as file:
            file.write(event["url"])
        time.sleep(5)
    os.system(f"echo {event['action']} {tv_id} | cec-client -s -d 1")


def schedule_events():
    schedule.clear()
    events = load_events()
    for event in events:
        day = event["day"]
        on_event = {"action": "on", "url": event["url"]}
        off_event = {"action": "standby"}
        getattr(schedule.every(), day.lower()).at(event["on_time"]).do(execute_event, on_event)
        getattr(schedule.every(), day.lower()).at(event["off_time"]).do(execute_event, off_event)

    while True:
        schedule.run_pending()
        time.sleep(60)

@app.route("/events", methods=["GET"])
def get_events():
    return jsonify(load_events())

@app.route("/events", methods=["POST"])
def update_events():
    events = request.json
    save_events(events)

    # kill the existing scheduler thread if it exists
    for thread in threading.enumerate():
        if thread.name == "scheduler":
            thread.join(timeout=1)
            break

    # start a new thread
    threading.Thread(target=schedule_events, daemon=True, name='scheduler').start()
    return jsonify({"status": "success"})

if __name__ == "__main__":
    # read the prior URL from the file
    if os.path.exists("current_url.txt"):
        with open("current_url.txt", "r") as file:
            current_url = file.read().strip()
            os.system(f"./kiosk.sh {current_url}")
        print(f"Current URL: {current_url}")
    else:
        print("No current URL found.")
    threading.Thread(target=schedule_events, daemon=True, name='scheduler').start()
    app.run(host="0.0.0.0", port=5000)