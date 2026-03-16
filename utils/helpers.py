# -*- coding: utf-8 -*-
"""
公共工具函数模块

包含系统中共用的辅助函数。
"""
from typing import Optional, Dict, Any, List, Union
from flask import Request, session
import json
from datetime import datetime


def get_request_json() -> Dict[str, Any]:
    """
    获取请求的 JSON 数据
    
    Args:
        request: Flask 请求对象
    
    Returns:
        解析后的 JSON 数据
    """
    from flask import request
    return request.json or {}


def get_param(key: str, default: Any = None, param_type: str = 'str') -> Any:
    """
    获取请求参数
    
    Args:
        key: 参数名
        default: 默认值
        param_type: 参数类型 (str/int/float/bool)
    
    Returns:
        转换后的参数值
    """
    from flask import request
    
    value = request.args.get(key) or request.form.get(key)
    
    if value is None:
        return default
    
    try:
        if param_type == 'int':
            return int(value)
        elif param_type == 'float':
            return float(value)
        elif param_type == 'bool':
            return value.lower() in ('true', '1', 'yes')
        else:
            return value
    except (ValueError, TypeError):
        return default


def success_response(data: Any = None, msg: str = 'success') -> Dict[str, Any]:
    """
    返回成功响应
    
    Args:
        data: 响应数据
        msg: 成功消息
    
    Returns:
        JSON 响应字典
    """
    response = {'code': 0, 'msg': msg}
    if data is not None:
        response['data'] = data
    return response


def error_response(msg: str, code: int = 1, **kwargs) -> Dict[str, Any]:
    """
    返回错误响应
    
    Args:
        msg: 错误消息
        code: 错误代码
        **kwargs: 其他附加字段
    
    Returns:
        JSON 响应字典
    """
    response = {'code': code, 'msg': msg}
    response.update(kwargs)
    return response


def require_params(*params: str) -> Optional[Dict[str, Any]]:
    """
    检查必需参数
    
    Args:
        *params: 必需的参数名列表
    
    Returns:
        如果参数完整返回 None，否则返回错误响应
    """
    from flask import request
    
    data = request.json or {}
    missing = [p for p in params if p not in data or data[p] is None]
    
    if missing:
        return error_response(f'缺少参数: {", ".join(missing)}')
    return None


def get_current_user_id() -> Optional[int]:
    """获取当前登录用户 ID"""
    return session.get('user_id')


def get_current_username() -> Optional[str]:
    """获取当前登录用户名"""
    return session.get('username')


def get_current_user_name() -> Optional[str]:
    """获取当前登录用户姓名"""
    return session.get('name')


def is_logged_in() -> bool:
    """检查用户是否已登录"""
    return 'user_id' in session


def format_datetime(dt: Optional[datetime], fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    格式化日期时间
    
    Args:
        dt: 日期时间对象
        fmt: 格式字符串
    
    Returns:
        格式化后的日期时间字符串
    """
    if dt is None:
        return ''
    if isinstance(dt, str):
        return dt
    return dt.strftime(fmt)


def format_date(dt: Optional[datetime]) -> str:
    """格式化日期 (不含时间)"""
    return format_datetime(dt, '%Y-%m-%d')


def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """
    安全地解析 JSON 字符串
    
    Args:
        json_str: JSON 字符串
        default: 解析失败时的默认值
    
    Returns:
        解析后的对象或默认值
    """
    if not json_str:
        return default
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default


def safe_json_dumps(obj: Any, default: str = '{}') -> str:
    """
    安全地序列化为 JSON 字符串
    
    Args:
        obj: 要序列化的对象
        default: 序列化失败时的默认字符串
    
    Returns:
        JSON 字符串
    """
    try:
        return json.dumps(obj, ensure_ascii=False)
    except (TypeError, ValueError):
        return default


def truncate_string(s: str, length: int = 50, suffix: str = '...') -> str:
    """
    截断字符串
    
    Args:
        s: 原始字符串
        length: 最大长度
        suffix: 截断后缀
    
    Returns:
        截断后的字符串
    """
    if not s:
        return ''
    if len(s) <= length:
        return s
    return s[:length] + suffix


def calculate_pagination(page: int, limit: int, total: int) -> Dict[str, Any]:
    """
    计算分页信息
    
    Args:
        page: 当前页码
        limit: 每页数量
        total: 总记录数
    
    Returns:
        分页信息字典
    """
    total_pages = (total + limit - 1) // limit if limit > 0 else 0
    
    return {
        'page': page,
        'limit': limit,
        'total': total,
        'pages': total_pages,
        'has_next': page < total_pages,
        'has_prev': page > 1,
        'first': 1,
        'last': total_pages
    }


def get_pagination_params(
    default_page: int = 1,
    default_limit: int = 10,
    max_limit: int = 100
) -> tuple:
    """
    获取并验证分页参数
    
    Args:
        default_page: 默认页码
        default_limit: 默认每页数量
        max_limit: 最大每页数量
    
    Returns:
        (page, limit) 元组
    """
    from flask import request
    
    page = request.args.get('page', default_page, type=int)
    limit = request.args.get('limit', default_limit, type=int)
    
    if page < 1:
        page = 1
    if limit < 1:
        limit = default_limit
    elif limit > max_limit:
        limit = max_limit
    
    return page, limit
