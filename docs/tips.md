# Tips

## 生成 requirements.txt

目录下运行 `pipreqs ./ --encoding UTF-8 --ignore angular,migrations`
即可以得到 `requirements.txt`

## 生成 structure.txt

目录下运行`tree -d -L 3 -I "venv|node_modules|__pycache__" . > docs/structure.txt`

## 启用 gzip(nginx)

使用 gzip 压缩 js 或者 json 文件 [参考](https://www.darrenfang.com/2015/01/setting-up-http-cache-and-gzip-with-nginx/)  
编辑文件 `/etc/nginx/nginx.conf`

```nginx
http {
  # 开启gzip
  gzip on;
  # 启用gzip压缩的最小文件，小于设置值的文件将不会压缩
  gzip_min_length 1k;
  # gzip 压缩级别，1-10，数字越大压缩的越好，也越占用CPU时间，后面会有详细说明
  gzip_comp_level 1;
  # 进行压缩的文件类型。其中的值可以在 mime.types 文件中找到。
  gzip_types text/css
             application/javascript
             application/json
  # 是否在http header中添加Vary: Accept-Encoding，建议开启
  gzip_vary on;
  # 禁用IE 6 gzip
  gzip_disable "MSIE [1-6]\.";
}
```
