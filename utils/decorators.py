# 统一错误处理装饰器
from flask import jsonify, request
from functools import wraps
import traceback
import sys

def handle_errors(f):
    """
    统一错误处理装饰器
    
    自动捕获并处理：
    - 数据库异常 (SQLAlchemyError)
    - 值错误 (ValueError)
    - 类型错误 (TypeError)
    - 其他预期外的异常
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            # 获取异常类型和消息
            exc_type = type(e).__name__
            exc_message = str(e)
            
            # 记录详细错误到标准错误输出
            print(f"[ERROR] {exc_type}: {exc_message}", file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)
            
            # 根据异常类型返回合适的错误消息
            if 'sqlalchemy' in str(type(e).__module__.lower()) or 'IntegrityError' in exc_type:
                # 数据库相关错误
                error_msg = '数据库操作失败，请检查数据是否重复或关联是否存在'
            elif exc_type == 'ValueError':
                error_msg = '数据格式错误'
            elif exc_type == 'TypeError':
                error_msg = '数据类型错误'
            elif exc_type == 'PermissionError':
                error_msg = '没有操作权限'
            else:
                error_msg = '操作失败，请稍后重试'
            
            # API 请求返回 JSON 错误
            if request.path.startswith('/api/') or request.is_json:
                return jsonify({
                    'code': 500,
                    'msg': error_msg,
                    'error_type': exc_type
                }), 500
            
            # 页面请求返回简单错误消息
            return f"""
            <!DOCTYPE html>
            <html>
            <head><meta charset="UTF-8"><title>操作失败</title></head>
            <body>
                <script>
                    alert('{error_msg}');
                    history.back();
                </script>
            </body>
            </html>
            """
    
    return decorated_function


def safe_db_operation(func):
    """
    数据库安全操作装饰器
    
    专门用于数据库操作，添加事务管理
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        from models import db
        try:
            result = func(*args, **kwargs)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise
    
    return decorated_function
