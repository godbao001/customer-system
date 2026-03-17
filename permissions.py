# 统一的权限检查模块
from flask import session, redirect, jsonify, request
from functools import wraps

# 所有权限定义
ALL_PERMISSIONS = {
    'login': '系统登录',
    'stats_view': '查看统计',
    'shop_view': '查看客户',
    'shop_add': '添加客户',
    'shop_edit': '编辑客户',
    'shop_delete': '删除客户',
    'order_view': '查看订单',
    'order_edit': '处理订单',
    'order_delete': '删除订单',
    'product_view': '查看产品',
    'product_edit': '编辑产品',
    'biz_generate': '生成制作',
    'biz_force_edit': '强制修改',
    'system_basic': '系统设置',
    'system_field': '字段管理',
    'system_log': '日志管理',
    'user_manage': '用户管理',
    'role_manage': '角色管理'
}

# 公共页面（无需权限检查）
PUBLIC_PATHS = [
    '/login', '/register', '/logout', '/profile',
    '/api/login', '/api/register', '/api/auth_status', '/api/permissions'
]

# 公共API（只需登录，无需具体权限）
PUBLIC_API_PATHS = [
    '/system/api/field/options',  # 获取字段选项
    '/system/api/basic/get',       # 获取系统配置
    '/system/api/field/list',     # 获取字段列表
    '/product/api/category/tree', # 获取产品分类树
    '/order/api/shops',           # 获取店铺列表
]

def check_permission(*permissions):
    """统一权限检查装饰器"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # 公共页面直接放行
            if request.path in PUBLIC_PATHS:
                return f(*args, **kwargs)
            
            # 公共API只需登录即可
            for api_path in PUBLIC_API_PATHS:
                if request.path.startswith(api_path):
                    if 'user_id' not in session:
                        if request.path.startswith('/api/'):
                            return jsonify({'code': 1, 'msg': '请先登录'})
                        return redirect('/login')
                    return f(*args, **kwargs)
            
            # 检查登录
            if 'user_id' not in session:
                return redirect('/login')
            
            user_permissions = session.get('permissions', [])
            
            # 没有权限则拒绝
            if not user_permissions:
                if request.path.startswith('/api/'):
                    return jsonify({'code': 1, 'msg': '没有权限'})
                return redirect('/login?from=noperm')
            
            # 检查具体权限
            for perm in permissions:
                if perm not in user_permissions:
                    # API请求返回JSON错误，而不是重定向
                    if request.path.startswith('/api/'):
                        return jsonify({'code': 1, 'msg': '没有权限'})
                    return redirect('/login?from=noperm')
            
            return f(*args, **kwargs)
        return wrapped
    return decorator

def get_user_permissions():
    """获取当前用户的权限列表"""
    return session.get('permissions', [])
