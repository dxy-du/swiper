#!/bin/bash

PROJECT_DIR='/opt/swiper'

PID=`cat $PROJECT_DIR/logs/gunicorn.pid`  # 从 pid 文件中获取主进程的 pid
kill $PID
