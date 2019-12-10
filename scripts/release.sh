#!/bin/bash

PROJECT_DIR=$1  # 本地项目文件夹
REMOTE_DIR='/opt/swiper/'  # 远程项目文件夹

USER='root'

# 上传代码
for HOST in `cat $PROJECT_DIR/scripts/hosts`
do
    # 上传
    rsync -crvP --exclude={.git,.venv,logs,__pycache__} $PROJECT_DIR $USER@$HOST:$REMOTE_DIR
    # 重启服务器
    ssh $USER@$HOST '/opt/swiper/scripts/restart.sh'
done
