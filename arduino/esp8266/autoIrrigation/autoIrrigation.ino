// WIFI&OTA
#include <ESP8266WiFi.h>
#include <ArduinoOTA.h>

// Config
#include "config.h"

// NTP
#include <NTPClient.h>
#include <WiFiUdp.h>
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "ntp.aliyun.com", 0, 60000);
// FIXME:莫名奇妙会无法与NTP服务器同步时间。(猜测是和路由器有关)

// Json
#include <ArduinoJson.h>

// Socket
#include <SocketIoClient.h>
#if ENABLE_SSL
#define beginwebsocket beginSSL
#else
#define beginwebsocket begin
#endif
SocketIoClient webSocket;

// DHT
#include <dht.h>
#if DHT_VER == 11
#define readdht read11
#elif DHT_VER == 22
#define readdht read22
#endif
#define DHT_PIN D4 // 连接到DHT传感器的端口
dht DHT;

// Status
char msg[100];
unsigned long lastMillis = 0;  //计时器
unsigned long valveMillis = 0; //电磁阀自动关闭计时器
bool valve_delay_trigger = 0;  //电磁阀自动关闭触发器
unsigned long pumpMillis = 0;  //抽水机自动关闭计时器
bool pump_delay_trigger = 0;   //抽水机自动关闭触发器

String temperature = "";
String relative_humidity = "";
bool valve = false;
bool pump = false;
unsigned long valve_delay = 60; //电磁阀延时，单位 秒
unsigned long pump_delay = 60;  //抽水机延时，单位 秒
String data_readtime = "";
#define PUMP_PIN D1  // 抽水机
#define VALVE_PIN D2 // 电磁阀 (连接继电器的端口)

void event(const char *payload, size_t length)
{
  StaticJsonBuffer<300> jsonBuffer;
  JsonObject &root = jsonBuffer.parseObject(payload);
  // Test if parsing succeeds.
  if (!root.success())
  {
    return;
  }
  if (root["valve"] != "null")
  {
    valve = root["valve"];
    if (valve)
    {
      valve_delay_trigger = true;
      valveMillis = millis(); //重置电磁阀关闭计时
    }
  }
  if (root["pump"] != "null")
  {
    pump = root["pump"];
    if (pump)
    {
      pump_delay_trigger = true;
      pumpMillis = millis(); //重置抽水机关闭计时
    }
  }
  if (root["valve_delay"] != "null")
    valve_delay = root["valve_delay"];
  if (root["pump_delay"] != "null")
    pump_delay = root["pump_delay"];
  event_set();
  upload();
}

void event_set()
{
  digitalWrite(PUMP_PIN, pump);
  digitalWrite(VALVE_PIN, valve);
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
  payload += "," + String(device_id);
  payload += "|" + temperature;
  payload += "," + relative_humidity;
  payload += "," + String(valve);
  payload += "," + String(pump);
  payload += "," + String(valve_delay);
  payload += "," + String(pump_delay);
  payload += "\"}";

  payload.toCharArray(msg, 100);
  webSocket.emit("device status", msg);

  lastMillis = millis(); //重置上传计时
}

void setup()
{
  pinMode(BUILTIN_LED, OUTPUT);
  pinMode(PUMP_PIN, OUTPUT);
  pinMode(VALVE_PIN, OUTPUT);
  digitalWrite(BUILTIN_LED, HIGH); //初始为关闭状态
  digitalWrite(PUMP_PIN, LOW);
  digitalWrite(VALVE_PIN, LOW);

  setup_wifi(); //配置WIFI

  timeClient.begin(); //NTC服务启动

  //OTA设置
  //Port defaults to 8266
  ArduinoOTA.setPort(8266);
  //Hostname defaults to esp8266-[ChipID]
  ArduinoOTA.setHostname(device_name);
  //No authentication by default
  //ArduinoOTA.setPassword("admin");
  ArduinoOTA.begin();

  //WebSocket设置
  webSocket.beginwebsocket(server_url, server_port, "/socket.io/?transport=websocket");
  webSocket.setAuthorization(admin_name, admin_password);
  webSocket.on(device_id, event);
}

void loop()
{
  ArduinoOTA.handle(); // OTA
  timeClient.update(); // 更新NTP时间
  webSocket.loop();    // Websocket loop

  // 每10秒上传一次数据
  if (millis() - lastMillis > 10000)
  {
    read_data();
    upload();
  }

  // 延时关闭电磁阀
  if (valve_delay_trigger && millis() - valveMillis > 1000 * valve_delay)
  {
    valve_delay_trigger = false;
    valve = false;
    digitalWrite(VALVE_PIN, valve);
    upload();
  }

  // 延时关闭抽水机
  if (pump_delay_trigger && millis() - pumpMillis > 1000 * pump_delay)
  {
    pump_delay_trigger = false;
    pump = false;
    digitalWrite(PUMP_PIN, pump);
    upload();
  }
}
