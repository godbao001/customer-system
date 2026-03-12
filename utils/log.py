# 操作日志工具
from models import OperationLog
from flask import request, session
from datetime import datetime
import json


def get_client_ip():
    """获取客户端IP地址"""
    if request.headers.get('X-Forwarded-For'):
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


def add_log(category, action, detail='', result='success'):
    """
    记录操作日志
    
    参数:
        category: 操作分类 (login/logout/shop/product/order/user/role/system)
        action: 操作动作 (如: 登录系统、添加店铺、修改订单等)
        detail: 操作详情 (可选)
        result: 操作结果 (success/fail)
    """
    user_id, username, user_name = get_current_user()
    ip = get_client_ip()
    
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


def log_login(username, success=True, detail=''):
    """记录登录日志"""
    result = 'success' if success else 'fail'
    add_log('login', '用户登录', detail or f'用户名: {username}', result)


def log_logout():
    """记录退出登录日志"""
    add_log('logout', '退出登录', '用户退出系统')


def log_operation(category, action, detail='', result='success'):
    """通用操作日志记录"""
    add_log(category, action, detail, result)
