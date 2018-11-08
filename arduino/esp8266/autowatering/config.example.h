// Config
const char *device_name = "autowatering"; // 设备名称

const char *ssid = "";     // WiFi名称
const char *password = ""; // WiFi密码

const char *server_url = "127.0.0.1"; // 服务器地址
const int server_port = 5000;         // 服务器端口
const int device_id = 1;              // 设备ID，与服务器一致
#define DHT_VER 11                    // DHT版本 11或者22
#define ENABLE_SSL 0                  // 是否使用SSL与服务器通讯

const char *admin_name = ""; // 网页管理员账户
const char *admin_password = "";
// TODO: 以后使用TOKEN与服务器进行认证
