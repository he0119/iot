# Deploy
## Ubuntu 16.04, Nginx 1.14
1. Install Nginx
  ```bash
  sudo apt-get install nginx
  sudo mv docs/iot.conf /etc/nginx/sites-enabled/iot.hemengyang.tk
  ```
2. Add systemd service
  ```bash
  sudo mv docs/iot.service /etc/systemd/system/iot.service
  sudo systemctl daemon-reload
  sudo systemctl enable iot
  sudo systemctl start iot
  ```
