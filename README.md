# zebrinha-azul
Uma startup inovadora que se destaca no mercado por sua expertise em lidar com dados de clima e tráfego.



# Build Api Environment

    conda create -n zebrinha-azul python=3.10.8 -y
    conda activate zebrinha-azul
    pip install -r requirements.txt

# Run

    export MODE_DEPLOY=dev && export API_KEY_TEMP=8e4a3c2c7638bbd6d1a2477967c208fe && export API_KEY_TRAFFIC=AIzaSyBQDK6oefbA81kpgIRMpKq_vQO5dGDV3ZI && python main.py 

    curl -X GET "https://maps.googleapis.com/maps/api/directions/json?origin=-23.55052,-46.633308&destination=-22.906847,-43.172896&departure_time=1623427200&key=AIzaSyBQDK6oefbA81kpgIRMpKq_vQO5dGDV3ZI"