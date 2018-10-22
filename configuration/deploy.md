# Deploy
## Ubuntu 16.04, Nginx 1.10.3
1. Install Nginx
  ```bash
  sudo apt-get install nginx
  sudo mv configuration/iot.conf /etc/nginx/sites-enabled/iot
  ``` 
2. Enable HTTPS and HTTP2
  - Install certbot
    ```bash
    sudo apt-get update
    sudo apt-get install software-properties-common
    sudo add-apt-repository ppa:certbot/certbot
    sudo apt-get update
    sudo apt-get install python-certbot-nginx
    sudo certbot --nginx
    ``` 
  - Enable HTTP2  
    Open `/etc/nginx/sites-enabled/iot` and add `http2` like this:
    ```conf
    listen 443 ssl http2; # managed by Certbot
    ``` 
3. Add systemd service
  ```bash
  sudo mv configuration/iot.service /etc/systemd/system/iot.service
  sudo systemctl daemon-reload
  sudo systemctl enable iot
  sudo systemctl start iot
  ```
