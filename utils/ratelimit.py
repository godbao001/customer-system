# API 限流工具
import time
from functools import wraps
from flask import request, jsonify
from collections import defaultdict

# 简单的内存限流存储（生产环境建议用 Redis）
# 结构: {ip: [(时间戳, 请求数)]}
request_history = defaultdict(list)

# 配置
MAX_REQUESTS_PER_MINUTE = 60  # 每分钟最大请求数
CLEANUP_INTERVAL = 60  # 清理过期记录的时间间隔（秒）

def check_rate_limit(ip=None):
    """检查请求是否超过限流阈值"""
    if ip is None:
        # 从请求获取 IP
        ip = request.remote_addr or 'unknown'
    
    current_time = time.time()
    
    # 清理超过1分钟的记录
    request_history[ip] = [
        (t, count) for t, count in request_history[ip]
        if current_time - t < 60
    ]
    
    # 统计当前分钟的请求数
    total_requests = sum(count for _, count in request_history[ip])
    
    # 检查是否超过限制
    if total_requests >= MAX_REQUESTS_PER_MINUTE:
        return False, MAX_REQUESTS_PER_MINUTE - total_requests
    
    # 记录本次请求
    request_history[ip].append((current_time, 1))
    
    return True, MAX_REQUESTS_PER_MINUTE - total_requests - 1

def rate_limit(f):
    """限流装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 只对 API 请求进行限流
        if not request.path.startswith('/api/'):
            return f(*args, **kwargs)
        
        allowed, remaining = check_rate_limit()
        
        # 添加限流头信息
        from flask import make_response
        response = make_response(f(*args, **kwargs))
        response.headers['X-RateLimit-Limit'] = str(MAX_REQUESTS_PER_MINUTE)
        response.headers['X-RateLimit-Remaining'] = str(max(0, remaining))
        
        if not allowed:
            return jsonify({
                'code': 429,
                'msg': '请求过于频繁，请稍后再试'
            }), 429
        
        return response
    return decorated_function

def get_real_ip():
    """获取真实 IP（考虑代理）"""
    # 如果有代理/负载均衡，获取真实 IP
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr or 'unknown'
