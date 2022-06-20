# Info
Grabs data from purpleair.com and stores it in an InfluxDB

# Example Docker
sudo docker run --name airqualitytoinfluxdb \
-e influxdbhost="192.168.103.122" \
-e influxdbusername="airquality" \
-e influxdbpass="<your pass>" \
-e purpleairIDs="22553" \
-e key_purpleair="<your key>" \
-e key_openweather="<your key>" \
-e zip=60564 \
--net pub_net \
-d airqualitytoinfluxdb