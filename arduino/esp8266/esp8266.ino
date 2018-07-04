//MQTT&WIFI&OTA
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>
#include <ArduinoOTA.h>

//Config
#include "config.h"

WiFiClientSecure espClient;
PubSubClient client(espClient);
char msg[50];

//NTP
#include <NTPClient.h>
#include <WiFiUdp.h>
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "cn.pool.ntp.org", 0, 60000);

//DHT
#include <dht.h>
#define DHT22_PIN D4  //连接到DHT传感器的端口
dht DHT;

//Status
unsigned long lastMillis = 0;
String temperature = "";
String relative_humidity = "";
String relay1_status = "0";
String relay2_status = "0";
String data_readtime = "";
#define RELAY1_PIN D1
#define RELAY2_PIN D2 //连接继电器的端口

void setup()
{
  pinMode(BUILTIN_LED, OUTPUT);
  pinMode(RELAY1_PIN, OUTPUT);
  pinMode(RELAY2_PIN, OUTPUT);
  digitalWrite(BUILTIN_LED, HIGH); //初始为关闭状态
  digitalWrite(RELAY1_PIN, LOW);
  digitalWrite(RELAY2_PIN, LOW);

  setup_wifi(); //配置WIFI

  timeClient.begin(); //NTC服务启动

  client.setServer(mqtt_server, 8883);
  client.setCallback(callback); //设置MQTT服务

  //OTA设置
  // Port defaults to 8266
  ArduinoOTA.setPort(8266);
  // Hostname defaults to esp8266-[ChipID]
  ArduinoOTA.setHostname(arduino_ota_name);
  // No authentication by default
  // ArduinoOTA.setPassword("admin");
  ArduinoOTA.begin();
}

void setup_wifi()
{
  delay(10);
  WiFi.mode(WIFI_STA);
  // We start by connecting to a WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.waitForConnectResult() != WL_CONNECTED)
  {
    delay(5000);
    ESP.restart();
  }
}

void callback(char *topic, byte *payload, unsigned int length)
{
  data_readtime = timeClient.getEpochTime(); //修改数据的时间

  if ((char)payload[0] == '0')
  {
    upload("1"); //直接上传当前状态
  }

  if ((char)payload[0] == '1')
  {
    if ((char)payload[1] == '1')
    {
      digitalWrite(RELAY1_PIN, HIGH); // Turn the RELAY on
      relay1_status = "1";
    }
    else
    {
      digitalWrite(RELAY1_PIN, LOW); // Turn the RELAY off by making the voltage LOW
      relay1_status = "0";
    }
    upload("0");
  }
  if ((char)payload[0] == '2')
  {
    if ((char)payload[1] == '1')
    {
      digitalWrite(RELAY2_PIN, HIGH); // Turn the RELAY on
      relay2_status = "1";
    }
    else
    {
      digitalWrite(RELAY2_PIN, LOW); // Turn the RELAY off by making the voltage LOW
      relay2_status = "0";
    }
    upload("0");
  }
}

void reconnect()
{
  // Loop until we're reconnected
  while (!client.connected())
  {
    // Attempt to connect
    if (client.connect(mqtt_clientname, mqtt_username, mqtt_password))
    {
      // Once connected, publish an announcement...
      client.publish("MQTT", "hello world");
      // ... and resubscribe
      client.subscribe("control");
    }
    else
    {
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void read_data()
{
  int chk = DHT.read22(DHT22_PIN);
  switch (chk)
  {
    case DHTLIB_OK:
		relative_humidity = String(DHT.humidity);
    temperature = String(DHT.temperature);
		break;
    default:
		relative_humidity = "Error";
    temperature = "Error";
		break;
  }
  data_readtime = timeClient.getEpochTime(); //读取数据的时间
}

void upload(String method)
{
  String payload = method;
  payload += "," + temperature;
  payload += "," + relative_humidity;
  payload += "," + relay1_status;
  payload += "," + relay2_status;
  if (method == "0")
  {
    payload += "," + data_readtime; //只有当定时上传时才上传数据读取时间
  }

  payload.toCharArray(msg, 50);
  client.publish(mqtt_upload_topic, msg);
  lastMillis = millis();
}

void loop()
{
  ArduinoOTA.handle(); //OTA

  if (!client.connected())
  { //检查MQTT服务器状态，自动重连
    reconnect();
  }

  timeClient.update(); //更新NTP时间
  client.loop();       // MQTT loop

  if (millis() - lastMillis > 10000)
  {
    read_data();
    upload("0"); //每10秒上传一次数据
  }
}
