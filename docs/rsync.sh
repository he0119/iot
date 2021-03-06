# Upload to server
echo "Upload Files to Server"

# -c, --checksum 打开校验开关，强制对文件传输进行校验
# -z, --compress 对备份的文件在传输时进行压缩处理
# -r, --recursive 对子目录以递归模式处理
# -t, --times 保持文件时间信息
# --progress 在传输时显示传输过程
rsync -czrt --progress \
--exclude "__pycache__" \
--exclude ".pytest_cache" \
--exclude "venv" \
--exclude "migrations" \
--exclude ".env" \
--exclude "app.db" \
--exclude "iot.log" \
/mnt/c/Users/hmy01/Desktop/Works/Working/IoT/Flask/ \
ubuntu@iot.hemengyang.tk:/home/ubuntu/iot/
