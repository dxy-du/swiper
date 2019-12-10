#!/bin/bash

# 平滑重启

# 1. 先对主进程发送 kill -HUP 的信号
# 2. 主进程创建新的子进程，子进程回加载新的代码和配置
# 3. 旧的子进程处理完任务后会自己退出

# 1500 : master

# 1517 : worker  -> 978
# 1518 : worker  -> 625
# 1519 : worker  -> 737
# 1520 : worker  -> 992

# 2101 : worker <- 1
# 2103 : worker <- 2
# 2104 : worker <- 4
# 2105 : worker <- 6

PROJECT_DIR='/opt/swiper'

PID=`cat $PROJECT_DIR/logs/gunicorn.pid`
kill -HUP $PID

echo '服务器已重启完毕'
