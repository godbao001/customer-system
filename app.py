# 客户管理系统主应用
from flask import Flask
from config import Config
from models import db
from routes.main import main_bp
from routes.shop import shop_bp
from routes.product import product_bp
from routes.order import order_bp
from routes.system import system_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化数据库
    db.init_app(app)
    
    # 注册蓝图
    app.register_blueprint(main_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(system_bp)
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 客户管理系统启动成功！")
    print("📍 访问地址: http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
