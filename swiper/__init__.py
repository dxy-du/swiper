from pymysql import install_as_MySQLdb

from libs.orm import patch_model

install_as_MySQLdb()
patch_model()
