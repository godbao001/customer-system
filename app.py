# 客户管理系统主应用
from flask import Flask, session, request, make_response
from flask_wtf import CSRFProtect
from config import Config
from models import db
from routes.main import main_bp
from routes.shop import shop_bp
from routes.product import product_bp
from routes.order import order_bp
from routes.system import system_bp
from routes.auth import auth_bp
from routes.stats import stats_bp
from routes.biz import biz_bp
from utils.errors import register_error_handlers
from utils.security import register_jinja_filters
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化数据库
    db.init_app(app)
    
    # 初始化 CSRF 保护
    csrf = CSRFProtect()
    csrf.init_app(app)
    
    # 注册全局错误处理器
    register_error_handlers(app)
    
    # 注册 Jinja2 安全过滤器
    register_jinja_filters(app)
    
    # 配置 CORS（跨域访问）
    cors_origins = app.config.get('CORS_ORIGINS', [])
    if cors_origins:
        from flask_cors import CORS
        CORS(app, origins=cors_origins, supports_credentials=True)
    
    # 注册蓝图
    app.register_blueprint(main_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(system_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(biz_bp)
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # 根据环境配置决定是否开启 debug
    debug_mode = app.config.get('DEBUG', False)
    
    if debug_mode:
        print("⚠️  开发模式已开启 - 注意安全！")
    
    print("🚀 客户管理系统启动成功！")
    print(f"📍 访问地址: http://0.0.0.0:5000")
    print(f"🔒 安全模式: {'关闭' if debug_mode else '开启'}")
    
    # Session 配置 - 根据环境自动设置
    https_mode = os.getenv('HTTPS', '').lower() == 'true'
    app.config['SESSION_COOKIE_SECURE'] = https_mode and not debug_mode
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
