FROM python:3
ENV influxdbhost=""
ENV influxdbport="8086"
ENV influxdbusername=""
ENV influxdbpass=""
ENV influxdbdatabase="airquality"
ENV purpleairIDs="22553"
ENV key_purpleair=""
ENV key_openweather=""
ENV zip=""

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python ./getAirQuality.py --influxdbhost $influxdbhost --influxdbport $influxdbport --influxdbusername $influxdbusername --influxdbdatabase $influxdbdatabase --influxdbpass $influxdbpass -k $key_purpleair -i $purpleairIDs 
CMD python ./getPollution.py --influxdbhost $influxdbhost --influxdbport $influxdbport --influxdbusername $influxdbusername --influxdbdatabase $influxdbdatabase --influxdbpass $influxdbpass -k $key_openweather -z $zip 

