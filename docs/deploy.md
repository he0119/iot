# Deploy

## Ubuntu 16.04, Nginx 1.14

1. Install Nginx

```bash
sudo add-apt-repository ppa:ondrej/nginx && sudo apt update
sudo apt-get install nginx
sudo mv docs/iot.conf /etc/nginx/sites-enabled/iot.hemengyang.tk
```

1. Add systemd service

```bash
sudo mv docs/iot.service /etc/systemd/system/iot.service
sudo systemctl daemon-reload
sudo systemctl enable iot
sudo systemctl start iot
```
