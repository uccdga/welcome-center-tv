import React, {useState, useEffect} from "react";
import "./App.css";
import Switch from "react-switch";
import {FaTrash} from 'react-icons/fa';

const defaultEvent = {day: "Sunday", time: "12:00", state: "On"};
const daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

function App() {
    const [loading, setLoading] = useState(true);
    const [events, setEvents] = useState([]);

    useEffect(() => {
        fetch("http://localhost:5000/events")
            .then((res) => res.json())
            .then((data) => setEvents(data));
    }, []);

    const addEvent = () => {
        setEvents([...events, {...defaultEvent}]);
    };

    const updateEvent = (index, key, value) => {
        const newEvents = [...events];
        newEvents[index][key] = value;
        setEvents(newEvents);
    };

    const publishChanges = () => {
        setLoading(true)
        fetch("http://localhost:5000/events", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(events),
        }).then(() => {
            setLoading(false);
            alert("Events saved successfully!");
        }).catch((error) => {
            console.error("Error saving events:", error);
            setLoading(false);
            alert("Failed to save events.");
        });
    };

    const deleteEvent = (index) => {
        const newEvents = events.filter((_, i) => i !== index);
        setEvents(newEvents);
    };

    return (
        <div className="container">
            <div className="header">
                <button onClick={addEvent}>Add New Event</button>
                <button onClick={publishChanges}>Publish Changes</button>
            </div>
            <hr className="separator"/>

            <div className="event-list">
                {events.map((event, index) => (

                    <div key={index} className="event">
                        <div className="first-row">

                            <label>
                                Day:
                            </label>

                                <select value={event.day} onChange={(e) => updateEvent(index, "day", e.target.value)}>
                                    {daysOfWeek.map((day) => (
                                        <option key={day} value={day}>{day}</option>
                                    ))}
                                </select>

                            <label>
                                On Time:
                            </label>
                            <input
                                type="time"
                                value={event.on_time}
                                onChange={(e) => updateEvent(index, "on_time", e.target.value)}
                            />

                            <label>
                                Off Time:
                            </label>

                            <input
                                type="time"
                                value={event.off_time}
                                onChange={(e) => updateEvent(index, "off_time", e.target.value)}
                            />
                            <button className="delete-button" onClick={() => deleteEvent(index)}>
                                <FaTrash/>
                            </button>


                        </div>
                        <div className="url-row">
                            <label>URL: </label>
                            <input
                                type="text"
                                placeholder="Enter URL"
                                value={event.url}
                                onChange={(e) => updateEvent(index, "url", e.target.value)}
                                className="url-input"
                            />
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
        ;
}

export default App;