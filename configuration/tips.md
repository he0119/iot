# Tips
## 生成requirements.txt
目录下运行
pipreqs ./ --encoding UTF-8 --ignore iot/angular,migrations --print
可以得到requirements.txt

## 启用Gzip(nginx)
使用Gzip压缩JS或者JSON文件[参考](https://www.darrenfang.com/2015/01/setting-up-http-cache-and-gzip-with-nginx/)  
编辑文件`/etc/nginx/nginx.conf`
```conf
http {
  # 开启gzip
  gzip on;
  # 启用gzip压缩的最小文件，小于设置值的文件将不会压缩
  gzip_min_length 1k;
  # gzip 压缩级别，1-10，数字越大压缩的越好，也越占用CPU时间，后面会有详细说明
  gzip_comp_level 1;
  # 进行压缩的文件类型。javascript有多种形式。其中的值可以在 mime.types 文件中找到。
  gzip_types text/plain
             application/javascript
             application/x-javascript
             text/css
             application/xml
             text/javascript
             application/x-httpd-php;
  # 是否在http header中添加Vary: Accept-Encoding，建议开启
  gzip_vary on;
  # 禁用IE 6 gzip
  gzip_disable "MSIE [1-6]\.";
}
```
