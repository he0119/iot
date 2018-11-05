//WIFI&OTA&FS
#include <ESP8266WiFi.h>
#include <ArduinoOTA.h>
#include <FS.h>

//Ticker&Watchdog
#include <Ticker.h>
Ticker secondTick;
volatile int watchdogCount = 0;

//Config
#include "config.h"

//NTP
#include <NTPClient.h>
#include <WiFiUdp.h>
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "ntp.aliyun.com", 0, 60000);
//FIXME:莫名奇妙会无法与NTP服务器同步时间。(猜测是和路由器有关)

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
unsigned long lastMillis = 0;  //计时器

float temperature = NULL;
float relative_humidity = NULL;

unsigned long data_readtime = 0;

bool need_save_config = false; //设置保存触发器

void event(const char *payload, size_t length)
{
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject &root = jsonBuffer.parseObject(payload);
  //Test if parsing succeeds.
  if (!root.success())
  {
    return;
  }

  event_set();
  upload(0);
  if (need_save_config)
  {
    save_config();
    need_save_config = false;
  }
}

void event_set()
{
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
    relative_humidity = DHT.humidity;
    temperature = DHT.temperature;
    break;
  default:
    relative_humidity = NULL;
    temperature = NULL;
    break;
  }
  data_readtime = timeClient.getEpochTime();     //读取数据的时间
}

void upload(bool reset)
{
  String payload = String("{\"data\":\"");
  payload += String(data_readtime);
  payload += "," + String(device_id);
  payload += "|" + String(temperature);
  payload += "," + String(relative_humidity);
  payload += "\"}";

  char msg[200];
  payload.toCharArray(msg, 200);

  webSocket.emit("devicedata", msg);
  Serial.println(msg);
  if (reset)
    lastMillis = millis(); //重置上传计时
}

bool load_config()
{
  File configFile = SPIFFS.open("/config.json", "r");
  if (!configFile)
  {
    Serial.println("Failed to open config file");
    return false;
  }

  size_t size = configFile.size();
  if (size > 1024)
  {
    Serial.println("Config file size is too large");
    return false;
  }

  //Allocate a buffer to store contents of the file.
  std::unique_ptr<char[]> buf(new char[size]);

  //We don't use String here because ArduinoJson library requires the input
  //buffer to be mutable. If you don't use ArduinoJson, you may as well
  //use configFile.readString instead.
  configFile.readBytes(buf.get(), size);

  StaticJsonBuffer<200> jsonBuffer;
  JsonObject &json = jsonBuffer.parseObject(buf.get());

  if (!json.success())
  {
    Serial.println("Failed to parse config file");
    return false;
  }

  return true;
}

bool save_config()
{
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject &json = jsonBuffer.createObject();

  File configFile = SPIFFS.open("/config.json", "w");
  if (!configFile)
  {
    Serial.println("Failed to open config file for writing");
    return false;
  }

  json.printTo(configFile);
  return true;
}

void ISRwatchdog()
{
  //看门狗
  watchdogCount++;
  if (watchdogCount > 10)
  {
    ESP.reset();
  }
}

void setup()
{
  Serial.begin(115200);

  pinMode(BUILTIN_LED, OUTPUT);
  digitalWrite(BUILTIN_LED, HIGH); //初始为关闭状态

  SPIFFS.begin(); //配置FS
  if (!load_config())
    save_config(); //读取配置，否则保存默认配置

  setup_wifi(); //配置WIFI

  timeClient.begin(); //NTC服务启动

  //OTA设置
  ArduinoOTA.setPort(8266);
  ArduinoOTA.setHostname(device_name);
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
    watchdogCount = 0; //Feed dog while doing update
  });
  ArduinoOTA.begin();

  //WebSocket设置
  webSocket.beginwebsocket(server_url, server_port, "/socket.io/?transport=websocket");
  webSocket.setAuthorization(admin_name, admin_password);

  char buf[16];
  itoa(device_id, buf, 10);
  webSocket.on(buf, event);

  //Watchdog
  secondTick.attach(1, ISRwatchdog);
}

void loop()
{
  watchdogCount = 0; //Feed dog

  ArduinoOTA.handle(); //OTA
  timeClient.update(); //更新NTP时间
  webSocket.loop();    //Websocket loop

  //每10秒上传一次数据
  if (millis() - lastMillis > 10000)
  {
    read_data();
    upload(1);
  }
}
