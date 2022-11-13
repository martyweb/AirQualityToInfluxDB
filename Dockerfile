FROM alpine:3.15
ENV influxdbhost=""
ENV influxdbport="8086"
ENV influxdbusername=""
ENV influxdbpass=""
ENV influxdbdatabase="airquality"
ENV purpleairIDs=""
ENV key_purpleair=""
ENV key_openweather=""
ENV zip=""

COPY requirements.txt ./
RUN apk add --update --no-cache bash python3  && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN find . -type f -iname "*.sh" -exec chmod +x {} \;
CMD ["./start.sh"]

#RUN python ./getAirQuality.py --influxdbhost $influxdbhost --influxdbport $influxdbport --influxdbusername $influxdbusername --influxdbdatabase $influxdbdatabase --influxdbpass $influxdbpass -k $key_purpleair -i $purpleairIDs 
#CMD python ./getPollution.py --influxdbhost $influxdbhost --influxdbport $influxdbport --influxdbusername $influxdbusername --influxdbdatabase $influxdbdatabase --influxdbpass $influxdbpass -k $key_openweather -z $zip 

