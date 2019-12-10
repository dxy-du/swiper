#!/bin/bash

PROJECT_DIR='/opt/swiper'

cd $PROJECT_DIR
source $PROJECT_DIR/.venv/bin/activate  # 加载虚拟环境
gunicorn -c $PROJECT_DIR/swiper/gunicorn-config.py swiper.wsgi  # 启动程序
deactivate  # 退出虚拟环境
cd -
