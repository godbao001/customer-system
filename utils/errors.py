# 统一错误处理
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
import sys
import traceback

def register_error_handlers(app):
    """注册全局错误处理器"""
    
    # 400 - Bad Request
    @app.errorhandler(400)
    def bad_request(e):
        if request.path.startswith('/api/'):
            return jsonify({
                'code': 400,
                'msg': '请求参数错误'
            }), 400
        return render_error_page(400, '请求参数错误'), 400
    
    # 401 - Unauthorized
    @app.errorhandler(401)
    def unauthorized(e):
        if request.path.startswith('/api/'):
            return jsonify({
                'code': 401,
                'msg': '请先登录'
            }), 401
        return render_error_page(401, '请先登录'), 401
    
    # 403 - Forbidden
    @app.errorhandler(403)
    def forbidden(e):
        if request.path.startswith('/api/'):
            return jsonify({
                'code': 403,
                'msg': '没有权限访问'
            }), 403
        return render_error_page(403, '没有权限访问'), 403
    
    # 404 - Not Found
    @app.errorhandler(404)
    def not_found(e):
        if request.path.startswith('/api/'):
            return jsonify({
                'code': 404,
                'msg': '接口不存在'
            }), 404
        return render_error_page(404, '页面不存在'), 404
    
    # 405 - Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(e):
        if request.path.startswith('/api/'):
            return jsonify({
                'code': 405,
                'msg': '请求方法不允许'
            }), 405
        return render_error_page(405, '请求方法不允许'), 405
    
    # 429 - Too Many Requests (限流)
    @app.errorhandler(429)
    def ratelimit(e):
        if request.path.startswith('/api/'):
            return jsonify({
                'code': 429,
                'msg': '请求过于频繁，请稍后再试'
            }), 429
        return render_error_page(429, '请求过于频繁'), 429
    
    # 500 - Internal Server Error
    @app.errorhandler(500)
    def internal_error(e):
        # 生产环境不暴露详细错误信息
        error_id = generate_error_id()
        print(f"Error ID: {error_id}")  # 记录到日志
        
        if request.path.startswith('/api/'):
            return jsonify({
                'code': 500,
                'msg': '服务器内部错误',
                'error_id': error_id
            }), 500
        return render_error_page(500, '服务器内部错误', error_id), 500
    
    # 处理所有其他异常
    @app.errorhandler(Exception)
    def handle_exception(e):
        # HTTP 异常
        if isinstance(e, HTTPException):
            return e
        
        # 其他异常
        error_id = generate_error_id()
        
        # 记录详细错误到日志
        print(f"Error ID: {error_id}")
        print(traceback.format_exc())
        
        if request.path.startswith('/api/'):
            return jsonify({
                'code': 500,
                'msg': '服务器内部错误',
                'error_id': error_id
            }), 500
        return render_error_page(500, '服务器内部错误', error_id), 500

def generate_error_id():
    """生成错误 ID"""
    import uuid
    return str(uuid.uuid4())[:8]

def render_error_page(code, message, error_id=None):
    """渲染错误页面"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>错误 {code}</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #f5f6fa;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .error-container {{
                text-align: center;
                padding: 40px;
            }}
            .error-code {{
                font-size: 72px;
                font-weight: bold;
                color: {'#e74c3c' if code >= 500 else '#f39c12'};
                margin: 0;
            }}
            .error-message {{
                font-size: 24px;
                color: #2c3e50;
                margin: 20px 0;
            }}
            .error-id {{
                color: #7f8c8d;
                font-size: 14px;
            }}
            .btn {{
                display: inline-block;
                padding: 10px 20px;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="error-container">
            <h1 class="error-code">{code}</h1>
            <p class="error-message">{message}</p>
            {'<p class="error-id">错误ID: ' + error_id + '</p>' if error_id else ''}
            <a href="/" class="btn">返回首页</a>
        </div>
    </body>
    </html>
    """
    return html
