#!/usr/bin/bash

### 进入中转站目录
cd /home/water/beifen_1218
unzip /home/water/website.zip
docker cp website sad_shaw:/home/django/
docker restart 9f0738ddb11c
rm /home/water/website.zip
rm -rf website
echo "all have complete!"


