# -*- coding: utf-8 -*-
"""
XSS 防护工具

提供 HTML 转义、数据清洗等 XSS 防护功能。
"""
import html
import re
from typing import Any, Optional, List, Dict
from markupsafe import escape as html_escape


def escape_html(text: Any) -> str:
    """
    HTML 转义 - 防止 XSS 攻击
    
    Args:
        text: 待转义的文本
    
    Returns:
        转义后的安全文本
    """
    if text is None:
        return ''
    return html_escape(str(text))


def unescape_html(text: str) -> str:
    """
    HTML 反转义
    
    Args:
        text: 待反转义的文本
    
    Returns:
        反转义后的文本
    """
    if not text:
        return ''
    return html.unescape(text)


def strip_html_tags(text: str, allowed_tags: Optional[List[str]] = None) -> str:
    """
    移除 HTML 标签
    
    Args:
        text: 待处理的文本
        allowed_tags: 允许保留的标签列表
    
    Returns:
        移除标签后的文本
    """
    if not text:
        return ''
    
    if allowed_tags is None:
        # 移除所有 HTML 标签
        return re.sub(r'<[^>]+>', '', text)
    
    # 保留允许的标签
    allowed_pattern = '|'.join(allowed_tags)
    # 先替换允许的标签为占位符
    for tag in allowed_tags:
        text = re.sub(f'<{tag}[^>]*>', f'___ALLOWED_{tag}___', text, flags=re.IGNORECASE)
        text = re.sub(f'</{tag}>', f'___ALLOWED_{tag}_END___', text, flags=re.IGNORECASE)
    
    # 移除其他标签
    text = re.sub(r'<[^>]+>', '', text)
    
    # 恢复允许的标签
    for tag in allowed_tags:
        text = text.replace(f'___ALLOWED_{tag}___', f'<{tag}>')
        text = text.replace(f'___ALLOWED_{tag}_END___', f'</{tag}>')
    
    return text


def sanitize_input(text: Any, max_length: Optional[int] = None) -> str:
    """
    清洗用户输入
    
    1. HTML 转义
    2. 移除危险字符
    3. 限制长度
    
    Args:
        text: 用户输入
        max_length: 最大长度
    
    Returns:
        清洗后的安全文本
    """
    if text is None:
        return ''
    
    # 转换为字符串
    text = str(text)
    
    # 移除空字符
    text = text.replace('\x00', '')
    
    # 转义 HTML
    text = escape_html(text)
    
    # 限制长度
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text


def sanitize_dict(data: Dict[str, Any], max_length: int = 1000) -> Dict[str, Any]:
    """
    递归清洗字典中的所有字符串值
    
    Args:
        data: 待清洗的字典
        max_length: 字符串最大长度
    
    Returns:
        清洗后的字典
    """
    if not data:
        return {}
    
    result = {}
    for key, value in data.items():
        if isinstance(value, str):
            result[key] = sanitize_input(value, max_length)
        elif isinstance(value, dict):
            result[key] = sanitize_dict(value, max_length)
        elif isinstance(value, list):
            result[key] = [
                sanitize_input(v, max_length) if isinstance(v, str) else v
                for v in value
            ]
        else:
            result[key] = value
    
    return result


def is_safe_url(url: str, allowed_hosts: Optional[List[str]] = None) -> bool:
    """
    检查 URL 是否安全
    
    防止开放重定向漏洞
    
    Args:
        url: 待检查的 URL
        allowed_hosts: 允许的域名列表
    
    Returns:
        True 表示安全，False 表示不安全
    """
    if not url:
        return True
    
    # 禁止 javascript: 等危险协议
    dangerous_protocols = ['javascript:', 'data:', 'vbscript:']
    url_lower = url.lower()
    for proto in dangerous_protocols:
        if url_lower.startswith(proto):
            return False
    
    # 检查是否为相对路径
    if url.startswith('/'):
        return True
    
    # 检查是否为允许的绝对 URL
    if allowed_hosts:
        from urllib.parse import urlparse
        try:
            parsed = urlparse(url)
            return parsed.hostname in allowed_hosts
        except Exception:
            return False
    
    # 默认不允许外部 URL
    return False


def mask_sensitive_data(text: str, sensitive_patterns: Optional[List[str]] = None) -> str:
    """
    掩码敏感数据
    
    用于日志记录，防止敏感信息泄露
    
    Args:
        text: 待处理的文本
        sensitive_patterns: 敏感数据正则模式
    
    Returns:
        掩码处理后的文本
    """
    if not text:
        return ''
    
    if sensitive_patterns is None:
        # 默认敏感模式
        sensitive_patterns = [
            (r'\b\d{15,19}\b', '****'),  # 银行卡号
            (r'\b1[3-9]\d{9}\b', '****'),  # 手机号
            (r'password[=：:]\S+', 'password=****'),  # 密码
            (r'token[=：:]\S+', 'token=****'),  # Token
            (r'secret[=：:]\S+', 'secret=****'),  # 密钥
            (r'api[_-]?key[=：:]\S+', 'api_key=****'),  # API Key
        ]
    
    for pattern, replacement in sensitive_patterns:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text


# Jinja2 过滤器注册
def register_jinja_filters(app):
    """注册 Jinja2 模板过滤器"""
    
    @app.template_filter('escape')
    def escape_filter(text):
        """模板过滤器：HTML 转义"""
        return escape_html(text)
    
    @app.template_filter('safe')
    def safe_filter(text):
        """模板过滤器：标记为安全（谨慎使用）"""
        from markupsafe import Markup
        return Markup(text)
    
    @app.template_filter('mask')
    def mask_filter(text):
        """模板过滤器：掩码敏感数据"""
        return mask_sensitive_data(text)
