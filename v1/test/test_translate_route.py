from modules.utils import translate_directions_data

def test_translate_directions_data():
    data = {
        "Route1": {
            "geocoded_waypoints": [
                {"geocoder_status": "OK", "place_id": "123", "types": ["locality"]},
                {"geocoder_status": "OK", "place_id": "456", "types": ["locality"]}
            ],
            "routes": [
                {
                    "bounds": {"northeast": {"lat": 1.0, "lng": 2.0}, "southwest": {"lat": 3.0, "lng": 4.0}},
                    "copyrights": "Copyright 2024",
                    "legs": [
                        {
                            "distance": {"text": "5 km"},
                            "duration": {"text": "10 mins"},
                            "end_address": "End Address",
                            "end_location": {"lat": 5.0, "lng": 6.0},
                            "start_address": "Start Address",
                            "start_location": {"lat": 7.0, "lng": 8.0},
                            "steps": [
                                {
                                    "html_instructions": "Step 1",
                                    "distance": {"text": "1 km"},
                                    "duration": {"text": "2 mins"},
                                    "end_location": {"lat": 9.0, "lng": 10.0},
                                    "start_location": {"lat": 11.0, "lng": 12.0},
                                    "travel_mode": "driving"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }

    translated_data = translate_directions_data(data)

    assert "Route1" in translated_data
    assert "Geocoded Waypoints" in translated_data["Route1"]
    assert len(translated_data["Route1"]["Geocoded Waypoints"]) == 2
    assert "Routes" in translated_data["Route1"]
    assert len(translated_data["Route1"]["Routes"]) == 1
    assert "Legs" in translated_data["Route1"]["Routes"][0]
    assert len(translated_data["Route1"]["Routes"][0]["Legs"]) == 1
    assert "Steps" in translated_data["Route1"]["Routes"][0]["Legs"][0]
    assert len(translated_data["Route1"]["Routes"][0]["Legs"][0]["Steps"]) == 1

    assert translated_data["Route1"]["Routes"][0]["Legs"][0]["Steps"][0]["Instructions"] == "Step 1"