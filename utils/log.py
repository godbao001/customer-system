# 操作日志工具
from models import OperationLog
from flask import request, session
from datetime import datetime
import json
import re


# 敏感信息掩码模式
SENSITIVE_PATTERNS = [
    (r'password[=：:]\S+', 'password=****'),
    (r'pwd[=：:]\S+', 'pwd=****'),
    (r'token[=：:]\S+', 'token=****'),
    (r'secret[=：:]\S+', 'secret=****'),
    (r'api[_-]?key[=：:]\S+', 'api_key=****'),
    (r'password_hash[=：:]\S+', 'password_hash=****'),
    (r'"\s*password"\s*:\s*"[^"]*"', '"password":"****"'),
    (r'"\s*pwd"\s*:\s*"[^"]*"', '"pwd":"****"'),
]


def mask_sensitive_info(text: str) -> str:
    """
    掩码日志中的敏感信息
    
    Args:
        text: 待处理的日志内容
    
    Returns:
        掩码后的安全内容
    """
    if not text:
        return ''
    
    for pattern, replacement in SENSITIVE_PATTERNS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text


def get_client_ip():
    """获取客户端IP地址"""
    # 优先从代理头获取
    if request.headers.get('X-Forwarded-For'):
        # X-Forwarded-For 可能包含多个 IP，取第一个
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr or '0.0.0.0'


def get_current_user():
    """获取当前登录用户"""
    user_id = session.get('user_id')
    username = session.get('username')
    user_name = session.get('name', '')
    return user_id, username, user_name


def add_log(category: str, action: str, detail: str = '', result: str = 'success'):
    """
    记录操作日志
    
    Args:
        category: 操作分类 (login/logout/shop/product/order/user/role/system)
        action: 操作动作 (如: 登录系统、添加店铺、修改订单等)
        detail: 操作详情 (可选)
        result: 操作结果 (success/fail)
    """
    user_id, username, user_name = get_current_user()
    ip = get_client_ip()
    
    # 掩码敏感信息
    detail = mask_sensitive_info(detail)
    action = mask_sensitive_info(action)
    
    log = OperationLog(
        user_id=user_id,
        username=username or '',
        user_name=user_name or '',
        category=category,
        action=action,
        detail=detail,
        ip=ip,
        result=result
    )
    from models import db
    db.session.add(log)
    db.session.commit()


def log_login(username: str, success: bool = True, detail: str = ''):
    """
    记录登录日志
    
    Args:
        username: 用户名
        success: 是否成功
        detail: 详情（可选）
    """
    result = 'success' if success else 'fail'
    # 不记录完整用户名到详情，只记录操作
    detail = mask_sensitive_info(detail)
    add_log('login', '用户登录', detail or f'登录尝试', result)


def log_logout():
    """记录退出登录日志"""
    add_log('logout', '退出登录', '用户退出系统')


def log_operation(category: str, action: str, detail: str = '', result: str = 'success'):
    """
    通用操作日志记录
    
    Args:
        category: 操作分类
        action: 操作动作
        detail: 操作详情
        result: 操作结果
    """
    # 掩码敏感信息
    detail = mask_sensitive_info(detail)
    add_log(category, action, detail, result)


def log_api_request():
    """
    记录 API 请求日志（开发环境使用）
    
    只在 DEBUG 模式下记录，且自动掩码敏感信息
    """
    from flask import current_app
    
    if not current_app.config.get('DEBUG', False):
        return
    
    # 只记录请求路径，不记录请求体
    method = request.method
    path = request.path
    ip = get_client_ip()
    
    # 跳过静态文件等
    if path.startswith('/static/') or path.startswith('/api/auth_status'):
        return
    
    # 记录请求日志
    detail = f"{method} {path} - IP: {ip}"
    add_log('system', 'API请求', detail, 'success')
