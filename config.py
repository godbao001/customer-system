# 配置
import os

class Config:
    # MySQL配置
    MYSQL_HOST = '10.0.1.70'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '998135AAaa'
    MYSQL_DATABASE = 'hsay_20260303'
    
    # 格式化成MySQL连接字符串
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SECRET_KEY = os.urandom(24)
