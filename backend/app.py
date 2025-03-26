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
    commands = {'On': 'on', 'Off': 'standby'}
    tv_id = '0'
    # execute "echo {commands[event['action']]} {tv_id}" as a system process
    os.system(f"echo {commands[event['state']]} {tv_id} | cec-client -s -d 1")


def schedule_events():
    schedule.clear()
    events = load_events()
    for event in events:
        day = event["day"]
        time_str = event["time"]
        getattr(schedule.every(), day.lower()).at(time_str).do(execute_event, event)

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
    threading.Thread(target=schedule_events, daemon=True, name='scheduler').start()
    app.run(host="0.0.0.0", port=5000)