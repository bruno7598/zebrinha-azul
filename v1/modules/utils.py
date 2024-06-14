
def translate_directions_data(data):
    """
    Translates the Google Maps Directions API response data into a more readable format.

    Parameters:
    data (dict): The Google Maps Directions API response data.

    Returns:
    dict: A dictionary containing the translated data. If no routes are found, returns a message indicating this.

    The function iterates through the provided data, extracts relevant information, and constructs a new dictionary
    with the translated data. It handles cases where no routes are found and returns an appropriate message.
    """
    if not data:
        return {"message": "Nenhuma rota encontrada"}

    result = {}
    for route_name, route_data in data.items():
        result[route_name] = {}

        if 'geocoded_waypoints' in route_data:
            result[route_name]['Geocoded Waypoints'] = route_data['geocoded_waypoints']

        if 'routes' in route_data:
            routes = []
            for route in route_data['routes']:
                route_info = {
                    "Bounds": route.get('bounds', {}),
                    "Copyrights": route.get('copyrights', ''),
                    "Legs": []
                }

                for leg in route.get('legs', []):
                    leg_info = {
                        "Distance": leg['distance'].get('text', 'N/A'),
                        "Duration": leg['duration'].get('text', 'N/A'),
                        "End Address": leg['end_address'],
                        "End Location": leg['end_location'],
                        "Start Address": leg['start_address'],
                        "Start Location": leg['start_location'],
                        "Steps": []
                    }

                    for step in leg.get('steps', []):
                        step_info = {
                            "Instructions": step.get('html_instructions', 'N/A'),
                            "Distance": step['distance'].get('text', 'N/A'),
                            "Duration": step['duration'].get('text', 'N/A'),
                            "End Location": step['end_location'],
                            "Start Location": step['start_location'],
                            "Travel Mode": step.get('travel_mode', 'N/A')
                        }
                        leg_info["Steps"].append(step_info)

                    route_info["Legs"].append(leg_info)

                routes.append(route_info)

            result[route_name]['Routes'] = routes

    return result