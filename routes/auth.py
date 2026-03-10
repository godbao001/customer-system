# 认证和权限管理路由
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Role
import json

auth_bp = Blueprint('auth', __name__, url_prefix='')

# 权限常量
PERMISSIONS = {
    'shop_view': '查看客户',
    'shop_add': '添加客户',
    'shop_edit': '编辑客户',
    'shop_delete': '删除客户',
    'order_view': '查看订单',
    'order_edit': '处理订单',
    'order_delete': '删除订单',
    'product_view': '查看产品',
    'product_edit': '编辑产品',
    'user_manage': '用户管理',
    'role_manage': '角色管理'
}

# 检查权限装饰器
def permission_required(*permissions):
    def decorator(f):
        def wrapped(*args, **kwargs):
            if 'user_id' not in session:
                return redirect('/login')
            
            user = User.query.get(session['user_id'])
            if not user or user.status == 0:
                session.clear()
                return redirect('/login')
            
            # 超级管理员（无角色）拥有所有权限
            if user.role_id is None:
                return f(*args, **kwargs)
            
            # 检查权限
            user_permissions = json.loads(user.role.permissions) if user.role else []
            for perm in permissions:
                if perm not in user_permissions:
                    return jsonify({'code': 1, 'msg': '没有权限'})
            
            return f(*args, **kwargs)
        wrapped.__name__ = f.__name__
        return wrapped
    return decorator

# 登录页
@auth_bp.route('/login')
def login():
    if 'user_id' in session:
        return redirect('/shop/')
    return render_template('auth/login.html')

# 登录API
@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'code': 1, 'msg': '用户名和密码不能为空'})
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'code': 1, 'msg': '用户名或密码错误'})
    
    if user.status == 0:
        return jsonify({'code': 1, 'msg': '账号已被禁用'})
    
    session['user_id'] = user.id
    session['username'] = user.username
    session['role_id'] = user.role_id
    session['permissions'] = json.loads(user.role.permissions) if user.role else []
    
    return jsonify({'code': 0, 'msg': '登录成功'})

# 注册页
@auth_bp.route('/register')
def register():
    if 'user_id' in session:
        return redirect('/shop/')
    return render_template('auth/register.html')

# 注册API
@auth_bp.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')
    
    if not username or not password:
        return jsonify({'code': 1, 'msg': '用户名和密码不能为空'})
    
    if len(username) < 2 or len(username) > 20:
        return jsonify({'code': 1, 'msg': '用户名长度应为2-20个字符'})
    
    if len(password) < 6:
        return jsonify({'code': 1, 'msg': '密码长度至少6个字符'})
    
    if password != confirm_password:
        return jsonify({'code': 1, 'msg': '两次密码输入不一致'})
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'code': 1, 'msg': '用户名已存在'})
    
    # 创建用户（无权限）
    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        role_id=None,  # 无角色，无权限
        status=1
    )
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'code': 0, 'msg': '注册成功'})

# 登出
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# 检查登录状态
@auth_bp.route('/api/auth_status')
def auth_status():
    if 'user_id' not in session:
        return jsonify({'code': 0, 'logged_in': False})
    
    user = User.query.get(session['user_id'])
    if not user or user.status == 0:
        session.clear()
        return jsonify({'code': 0, 'logged_in': False})
    
    return jsonify({
        'code': 0,
        'logged_in': True,
        'username': session.get('username'),
        'role_id': session.get('role_id'),
        'permissions': session.get('permissions', [])
    })

# 获取权限列表
@auth_bp.route('/api/permissions')
def api_permissions():
    return jsonify({'code': 0, 'data': PERMISSIONS})

# ==================== 角色管理 ====================
@auth_bp.route('/admin/roles')
@permission_required('role_manage')
def roles_page():
    return render_template('auth/roles.html')

@auth_bp.route('/api/roles')
@permission_required('role_manage')
def api_roles():
    roles = Role.query.filter_by(status=1).all()
    return jsonify({'code': 0, 'data': [r.to_dict() for r in roles]})

@auth_bp.route('/api/roles/add', methods=['POST'])
@permission_required('role_manage')
def api_roles_add():
    data = request.json
    role_name = data.get('role_name', '').strip()
    permissions = data.get('permissions', [])
    
    if not role_name:
        return jsonify({'code': 1, 'msg': '角色名称不能为空'})
    
    if Role.query.filter_by(role_name=role_name, status=1).first():
        return jsonify({'code': 1, 'msg': '角色名称已存在'})
    
    role = Role(
        role_name=role_name,
        permissions=json.dumps(permissions),
        status=1
    )
    db.session.add(role)
    db.session.commit()
    
    return jsonify({'code': 0, 'msg': '添加成功'})

@auth_bp.route('/api/roles/edit/<int:id>', methods=['POST'])
@permission_required('role_manage')
def api_roles_edit(id):
    data = request.json
    role = Role.query.get(id)
    if not role:
        return jsonify({'code': 1, 'msg': '角色不存在'})
    
    role_name = data.get('role_name', '').strip()
    permissions = data.get('permissions', [])
    
    # 检查名称重复
    existing = Role.query.filter(Role.role_name == role_name, Role.id != id, Role.status == 1).first()
    if existing:
        return jsonify({'code': 1, 'msg': '角色名称已存在'})
    
    role.role_name = role_name
    role.permissions = json.dumps(permissions)
    db.session.commit()
    
    return jsonify({'code': 0, 'msg': '修改成功'})

@auth_bp.route('/api/roles/delete/<int:id>', methods=['POST'])
@permission_required('role_manage')
def api_roles_delete(id):
    role = Role.query.get(id)
    if not role:
        return jsonify({'code': 1, 'msg': '角色不存在'})
    
    # 检查是否有用户使用该角色
    if User.query.filter_by(role_id=id, status=1).first():
        return jsonify({'code': 1, 'msg': '该角色下有用户，无法删除'})
    
    role.status = 0
    db.session.commit()
    
    return jsonify({'code': 0, 'msg': '删除成功'})

# ==================== 用户管理 ====================
@auth_bp.route('/admin/users')
@permission_required('user_manage')
def users_page():
    roles = Role.query.filter_by(status=1).all()
    return render_template('auth/users.html', roles=roles)

@auth_bp.route('/api/users')
@permission_required('user_manage')
def api_users():
    users = User.query.filter_by(status=1).all()
    roles = Role.query.filter_by(status=1).all()
    
    users_data = []
    for u in users:
        u_dict = u.to_dict()
        u_dict['role_name'] = u.role.role_name if u.role else '无'
        users_data.append(u_dict)
    
    return jsonify({'code': 0, 'data': users_data})

@auth_bp.route('/api/users/add', methods=['POST'])
@permission_required('user_manage')
def api_users_add():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    role_id = data.get('role_id')
    
    if not username or not password:
        return jsonify({'code': 1, 'msg': '用户名和密码不能为空'})
    
    if User.query.filter_by(username=username).first():
        return jsonify({'code': 1, 'msg': '用户名已存在'})
    
    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        role_id=role_id if role_id else None,
        status=1
    )
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'code': 0, 'msg': '添加成功'})

@auth_bp.route('/api/users/edit/<int:id>', methods=['POST'])
@permission_required('user_manage')
def api_users_edit(id):
    data = request.json
    user = User.query.get(id)
    if not user:
        return jsonify({'code': 1, 'msg': '用户不存在'})
    
    if data.get('password'):
        user.password_hash = generate_password_hash(data['password'])
    
    user.role_id = data.get('role_id') if data.get('role_id') else None
    db.session.commit()
    
    return jsonify({'code': 0, 'msg': '修改成功'})

@auth_bp.route('/api/users/delete/<int:id>', methods=['POST'])
@permission_required('user_manage')
def api_users_delete(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'code': 1, 'msg': '用户不存在'})
    
    user.status = 0
    db.session.commit()
    
    return jsonify({'code': 0, 'msg': '删除成功'})
