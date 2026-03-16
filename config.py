# 配置
import os

class Config:
    # MySQL配置 - 支持环境变量覆盖
    MYSQL_HOST = os.getenv('MYSQL_HOST', '10.0.1.70')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '998135AAaa')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'hsay_20260303')
    
    # 格式化成MySQL连接字符串
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 安全配置
    SECRET_KEY = os.getenv('SECRET_KEY') or os.urandom(24)
    
    # Session 配置 - 防止 Session 固定攻击
    SESSION_COOKIE_SECURE = os.getenv('HTTPS', '').lower() == 'true'  # 仅 HTTPS 传输
    SESSION_COOKIE_HTTPONLY = True  # 禁止 JavaScript 访问
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF 防护
    SESSION_REGENERATE = True  # 登录后重新生成 Session ID
    
    # CSRF 配置
    WTF_CSRF_ENABLED = False  # 临时禁用调试
    WTF_CSRF_TIME_LIMIT = 3600  # CSRF token 有效期（秒）
    
    # 登录安全配置
    LOGIN_TIMEOUT = 3600  # 登录会话有效期（秒）
    MAX_LOGIN_ATTEMPTS = 5  # 最大登录失败次数
    LOGIN_LOCKOUT_TIME = 300  # 登录锁定时间（秒），5分钟
    
    # Flask-WTF CSRF secret key
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY') or os.urandom(16)
    
    # CORS 配置
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '').split(',') if os.getenv('CORS_ORIGINS') else []  # 允许的跨域来源
    
    # 环境配置
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = FLASK_ENV == 'development'
    
    # 分页配置
    PAGE_DEFAULT_LIMIT = 10  # 默认每页数量
    PAGE_MAX_LIMIT = 100  # 最大每页数量
    
    # API 限流配置
    RATELIMIT_ENABLED = True  # 开启限流
    RATELIMIT_DEFAULT = "200 per minute"  # 默认限流规则
