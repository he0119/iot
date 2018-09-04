//WIFI&OTA
#include <ESP8266WiFi.h>
#include <ArduinoOTA.h>

//Config
#include "config.h"

//NTP
#include <NTPClient.h>
#include <WiFiUdp.h>
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "ntp.aliyun.com", 0, 60000);

//Json
#include <ArduinoJson.h>

//Socket
#include <SocketIoClient.h>
#if ENABLE_SSL
  #define beginwebsocket beginSSL
#else
  #define beginwebsocket begin
#endif
SocketIoClient webSocket;

//DHT
#include <dht.h>
#if DHT_VER == 11
  #define readdht read11
#elif DHT_VER == 22
  #define readdht read22
#endif
#define DHT_PIN D4 //连接到DHT传感器的端口
dht DHT;

//Status
char msg[50];
unsigned long lastMillis = 0;
String temperature = "";
String relative_humidity = "";
bool relay1_status = false;
bool relay2_status = false;
String data_readtime = "";
#define RELAY1_PIN D1
#define RELAY2_PIN D2 //连接继电器的端口

void event(const char *payload, size_t length)
{
  StaticJsonBuffer<300> jsonBuffer;
  JsonObject &root = jsonBuffer.parseObject(payload);
  // Test if parsing succeeds.
  if (!root.success())
  {
    return;
  }
  if (root["relay1_status"] != "null")
    relay1_status = root["relay1_status"];
  if (root["relay2_status"] != "null")
    relay2_status = root["relay2_status"];
  event_set();
  upload();
}

void event_set()
{
  digitalWrite(RELAY1_PIN, relay1_status);
  digitalWrite(RELAY2_PIN, relay2_status);
  data_readtime = timeClient.getEpochTime();
}

void setup_wifi()
{
  delay(10);
  WiFi.mode(WIFI_STA);
  //We start by connecting to a WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.waitForConnectResult() != WL_CONNECTED)
  {
    delay(5000);
    ESP.restart();
  }
}

void read_data()
{
  int chk = DHT.readdht(DHT_PIN); //读取传感器数据
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

void upload()
{
  String payload = String("{\"data\":\"");
  payload += data_readtime;
  payload += "," + String(device_name);
  payload += "|" + temperature;
  payload += "," + relative_humidity;
  payload += "," + String(relay1_status);
  payload += "," + String(relay2_status);
  payload += "\"}";

  payload.toCharArray(msg, 50);
  webSocket.emit("device status", msg);

  lastMillis = millis(); //重置上传计时
}

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

  //OTA设置
  //Port defaults to 8266
  ArduinoOTA.setPort(8266);
  //Hostname defaults to esp8266-[ChipID]
  ArduinoOTA.setHostname(arduino_ota_name);
  //No authentication by default
  //ArduinoOTA.setPassword("admin");
  ArduinoOTA.begin();

  //WebSocket设置
  webSocket.beginwebsocket(websocket_url, websocket_port, "/socket.io/?transport=websocket");
  webSocket.setAuthorization(admin_name, admin_password);
  webSocket.on(device_name, event);
}

void loop()
{
  ArduinoOTA.handle(); //OTA
  timeClient.update(); //更新NTP时间
  webSocket.loop();    //Websocket loop

  if (millis() - lastMillis > 10000)
  {
    read_data();
    upload(); //每10秒上传一次数据
  }
}
