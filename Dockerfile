FROM python:3
ENV influxdbhost=""
ENV influxdbport="8086"
ENV influxdbusername=""
ENV influxdbpass=""
ENV influxdbdatabase="airquality"
ENV purpleairIDs="22553"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD python ./getAirQuality.py --influxdbhost $influxdbhost --influxdbport $influxdbport --influxdbusername $influxdbusername --influxdbdatabase $influxdbdatabase --influxdbpass $influxdbpass -i $purpleairIDs

