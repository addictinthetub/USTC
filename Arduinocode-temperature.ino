
//_____________________________________________________________________from influxdb website_________________________________________________________________________


#if defined(ESP32)
  #include <WiFiMulti.h>
  WiFiMulti wifiMulti;
  #define DEVICE "ESP32"
  #elif defined(ESP8266)
  #include <ESP8266WiFiMulti.h>
  ESP8266WiFiMulti wifiMulti;
  #define DEVICE "ESP8266"
  #endif
  
  #include <InfluxDbClient.h>
  #include <InfluxDbCloud.h>
  #include <Adafruit_Sensor.h>
  #include <Adafruit_MAX31865.h>
  #include <Wire.h>
  
  #define WIFI_SSID ""
  #define WIFI_PASSWORD ""
  #define INFLUXDB_URL ""
  #define INFLUXDB_TOKEN ""
  #define INFLUXDB_ORG ""
  #define INFLUXDB_BUCKET ""
  #define thermopin 2
  #define RREF 430
  
  Adafruit_MAX31865 thermo = Adafruit_MAX31865(thermopin);

  // Time zone info
  #define TZ_INFO "UTC8"
  
  // Declare InfluxDB client instance with preconfigured InfluxCloud certificate
  InfluxDBClient client(INFLUXDB_URL, INFLUXDB_ORG, INFLUXDB_BUCKET, INFLUXDB_TOKEN, InfluxDbCloud2CACert);
  
  // Declare Data point
  Point sensor("wifi_status");
  
  void setup() {
    Serial.begin(9600);
  
    // Setup wifi
    WiFi.mode(WIFI_STA);
    wifiMulti.addAP(WIFI_SSID, WIFI_PASSWORD);
  
    Serial.print("Connecting to wifi");
    while (wifiMulti.run() != WL_CONNECTED) {
      Serial.print(".");
      delay(100);
    }
    Serial.println();
  

    sensor.addTag("device", DEVICE);

    // Accurate time is necessary for certificate validation and writing in batches
    // We use the NTP servers in your area as provided by: https://www.pool.ntp.org/zone/
    // Syncing progress and the time will be printed to Serial.
    timeSync(TZ_INFO, "pool.ntp.org", "time.nis.gov");
  
  
    // Check server connection
    if (client.validateConnection()) {
      Serial.print("Connected to InfluxDB: ");
      Serial.println(client.getServerUrl());
    } else {
      Serial.print("InfluxDB connection failed: ");
      Serial.println(client.getLastErrorMessage());
    }
    thermo.begin(MAX31865_3WIRE);
  }

  void loop() {
  // Clear fields for reusing the point. Tags will remain untouched
  sensor.clearFields();

  // Read the temperature and humidity from the sensor, and add them to your data point, along with a calculated heat index
  float temperature1;

  temperature1=thermo.temperature(100,RREF);

  sensor.addField("temperature", temperature1);

  // Print what are we exactly writing
  Serial.print("Writing: ");
  Serial.println(sensor.toLineProtocol());


  Serial.println(client.pointToLineProtocol(sensor));

  if (!client.writePoint(sensor)) {
  Serial.print("InfluxDB write failed: ");
  Serial.println(client.getLastErrorMessage());
}

  // If no Wifi signal, try to reconnect it
  if ((WiFi.RSSI() == 0) && (wifiMulti.run() != WL_CONNECTED)) {
    Serial.println("Wifi connection lost");
  }

  // Write point
  if (!client.writePoint(sensor)) {
    Serial.print("InfluxDB write failed: ");
    Serial.println(client.getLastErrorMessage());
  }

  //Wait 10s
  Serial.println("Wait 10s");
  delay(2000);
}



//___________________________________________________________________________________________________________________________________________________________________


