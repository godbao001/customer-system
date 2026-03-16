# 认证和权限管理路由
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Role
from utils.log import log_login, log_logout, add_log
from config import Config
import json
import time
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='')

# 登录失败记录（内存存储，生产环境建议用 Redis）
# 结构: {username: {'count': 次数, 'locked_until': 锁定截止时间}}
login_failed_attempts = {}

def check_login_lockout(username):
    """检查账号是否被锁定"""
    if username in login_failed_attempts:
        attempt = login_failed_attempts[username]
        if attempt['locked_until'] and time.time() < attempt['locked_until']:
            remaining = int(attempt['locked_until'] - time.time())
            return True, remaining
        else:
            # 锁定时间已过，清除记录
            del login_failed_attempts[username]
    return False, 0

def record_login_failure(username):
    """记录登录失败"""
    current_time = time.time()
    if username not in login_failed_attempts:
        login_failed_attempts[username] = {'count': 0, 'locked_until': None}
    
    login_failed_attempts[username]['count'] += 1
    
    # 超过最大失败次数，锁定账号
    if login_failed_attempts[username]['count'] >= Config.MAX_LOGIN_ATTEMPTS:
        login_failed_attempts[username]['locked_until'] = current_time + Config.LOGIN_LOCKOUT_TIME
        return True  # 已锁定
    return False

def clear_login_attempts(username):
    """清除登录失败记录（登录成功后调用）"""
    if username in login_failed_attempts:
        del login_failed_attempts[username]

# 辅助函数：判断用户是否是超级管理员
def is_super_admin_user(user):
    if not user or not user.role_ids:
        return False
    role_ids = [int(rid) for rid in user.role_ids.split(',') if rid]
    if not role_ids:
        return False
    roles = Role.query.filter(Role.id.in_(role_ids), Role.status == 1).all()
    return any(getattr(r, 'is_super_admin', False) for r in roles)

# 权限常量 - 从 permissions.py 导入，确保包含所有权限
from permissions import ALL_PERMISSIONS
PERMISSIONS = ALL_PERMISSIONS

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
            
            # 超级管理员（无角色ID但有所有权限）拥有所有权限
            # 超级管理员的role_ids为'1'（指向超级管理员角色）
            
            # 获取用户所有角色的权限合并
            user_permissions = session.get('permissions', [])
            
            # 检查权限
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
    # 如果已登录，检查是否有权限，没有权限则显示登录页（让用户可以切换账号）
    if 'user_id' in session:
        from flask import request
        # 如果是从没有权限的页面跳转过来的，显示登录页并提示
        if request.args.get('from') == 'noperm':
            # 清除session，让用户重新登录
            session.clear()
            return render_template('auth/login.html', error='没有权限，请使用有权限的账号登录')
        return redirect('/shop/')
    # 首次访问，检查是否有错误提示
    from flask import request
    return render_template('auth/login.html', error=request.args.get('error', ''))

# 登录API
@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'code': 1, 'msg': '用户名和密码不能为空'})
    
    # 检查是否被锁定
    is_locked, remaining_time = check_login_lockout(username)
    if is_locked:
        log_login(username, False, f'账号被锁定，剩余{remaining_time}秒')
        return jsonify({
            'code': 1, 
            'msg': f'登录失败次数过多，账号已被锁定，请{remaining_time}秒后再试'
        })
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        # 记录登录失败
        is_now_locked = record_login_failure(username)
        
        # 获取剩余尝试次数
        attempts_left = Config.MAX_LOGIN_ATTEMPTS - login_failed_attempts.get(username, {}).get('count', 0)
        
        log_login(username, False, '密码错误')
        
        if is_now_locked:
            return jsonify({
                'code': 1, 
                'msg': f'登录失败次数过多，账号已被锁定{Config.LOGIN_LOCKOUT_TIME//60}分钟'
            })
        
        return jsonify({
            'code': 1, 
            'msg': f'用户名或密码错误，剩余尝试次数: {attempts_left}'
        })
    
    if user.status == 0:
        log_login(username, False, '账号被禁用')
        return jsonify({'code': 1, 'msg': '账号已被禁用'})
    
    # 登录成功，清除失败记录
    clear_login_attempts(username)
    
    # 重新生成 Session ID（防止 Session 固定攻击）
    session.clear()
    
    # 处理多角色权限合并
    permissions = []
    is_super_admin = False
    
    if user.role_ids:
        role_id_list = [int(rid) for rid in user.role_ids.split(',') if rid]
        roles = Role.query.filter(Role.id.in_(role_id_list), Role.status == 1).all()
        for role in roles:
            # 检查是否是超级管理员角色
            if getattr(role, 'is_super_admin', False):
                is_super_admin = True
            
            if is_super_admin:
                break
            
            perms = json.loads(role.permissions) if role.permissions else []
            for p in perms:
                if p not in permissions:
                    permissions.append(p)
    
    # 超级管理员拥有所有权限
    if is_super_admin:
        permissions = list(PERMISSIONS.keys())
    
    # 检查是否有登录权限（非超级管理员需要login权限）
    if not is_super_admin and 'login' not in permissions:
        return jsonify({'code': 1, 'msg': '没有登录权限，请联系管理员'})
    
    session['user_id'] = user.id
    session['username'] = user.username
    session['name'] = user.name
    session['role_ids'] = user.role_ids
    session['permissions'] = permissions
    
    # 记录登录日志
    log_login(username, True, f'用户: {user.name}')
    
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
    name = data.get('name', '').strip()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')
    
    # 验证姓名：2-10个中文汉字
    import re
    if not name:
        return jsonify({'code': 1, 'msg': '姓名不能为空'})
    if not re.match(r'^[\u4e00-\u9fa5]{2,10}$', name):
        return jsonify({'code': 1, 'msg': '姓名必须是2-10个中文汉字'})
    
    # 验证用户名：字母、数字、下划线，3-20位，不能以数字开头
    if not username:
        return jsonify({'code': 1, 'msg': '用户名不能为空'})
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]{2,19}$', username):
        return jsonify({'code': 1, 'msg': '用户名3-20位，字母/数字/下划线，不能以数字开头'})
    
    if not password:
        return jsonify({'code': 1, 'msg': '密码不能为空'})
    
    if len(password) < 6:
        return jsonify({'code': 1, 'msg': '密码长度至少6个字符'})
    
    if password != confirm_password:
        return jsonify({'code': 1, 'msg': '两次密码输入不一致'})
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'code': 1, 'msg': '用户名已存在'})
    
    # 检查是否是第一个用户（第一个用户成为超级管理员）
    user_count = User.query.count()
    
    # 检查是否已有超级管理员
    def is_super_admin_user(user):
        if not user.role_ids:
            return False
        role_ids = [int(rid) for rid in user.role_ids.split(',') if rid]
        if not role_ids:
            return False
        roles = Role.query.filter(Role.id.in_(role_ids), Role.status == 1).all()
        return any(getattr(r, 'is_super_admin', False) for r in roles)
    
    existing_super_admin = User.query.filter(User.status == 1).all()
    has_super_admin = any(is_super_admin_user(u) for u in existing_super_admin)
    
    if user_count == 0 and not has_super_admin:
        # 创建超级管理员角色
        import json
        super_admin_role = Role(
            role_name='超级管理员',
            permissions='[]',  # 权限为空，使用动态权限
            is_super_admin=True,
            status=1
        )
        db.session.add(super_admin_role)
        db.session.flush()  # 获取ID
        
        # 创建超级管理员用户
        user = User(
            name=name,
            username=username,
            password_hash=generate_password_hash(password),
            role_ids=str(super_admin_role.id),  # 分配超级管理员角色
            status=1
        )
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'code': 0, 'msg': '注册成功，您是系统第一个用户，已设为超级管理员'})
    
    # 创建普通用户（无角色，需要管理员分配）
    user = User(
        name=name,
        username=username,
        password_hash=generate_password_hash(password),
        role_ids='',  # 无角色，无权限
        status=1
    )
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'code': 0, 'msg': '注册成功'})

# 登出
@auth_bp.route('/logout')
def logout():
    username = session.get('username', '')
    user_name = session.get('name', '')
    # 先记录日志
    from utils.log import add_log
    add_log('logout', '退出登录', f'用户: {user_name}({username})')
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
    
    # 获取角色名称
    role_names = user.get_role_names() if hasattr(user, 'get_role_names') else ''
    
    # 重新计算权限（从数据库获取最新的角色权限）
    permissions = user.get_permissions() if hasattr(user, 'get_permissions') else []
    
    return jsonify({
        'code': 0,
        'logged_in': True,
        'username': session.get('username'),
        'name': session.get('name'),
        'avatar': user.avatar,
        'role_ids': session.get('role_ids'),
        'role_names': role_names,
        'permissions': permissions
    })

# 获取权限列表
@auth_bp.route('/api/permissions')
def api_permissions():
    return jsonify({'code': 0, 'data': PERMISSIONS})

# ==================== 个人中心 ====================
@auth_bp.route('/profile')
def profile_page():
    """个人中心页面"""
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('auth/profile.html')

@auth_bp.route('/api/profile/change_password', methods=['POST'])
def api_change_password():
    """修改密码"""
    if 'user_id' not in session:
        return jsonify({'code': 1, 'msg': '请先登录'})
    
    data = request.json
    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')
    
    if not old_password or not new_password:
        return jsonify({'code': 1, 'msg': '密码不能为空'})
    
    if len(new_password) < 6:
        return jsonify({'code': 1, 'msg': '新密码至少6位'})
    
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'code': 1, 'msg': '用户不存在'})
    
    # 验证旧密码
    if not check_password_hash(user.password_hash, old_password):
        return jsonify({'code': 1, 'msg': '当前密码错误'})
    
    # 更新密码
    user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    
    return jsonify({'code': 0, 'msg': '密码修改成功'})

@auth_bp.route('/api/profile/avatar', methods=['POST'])
def api_avatar_upload():
    """上传头像"""
    if 'user_id' not in session:
        return jsonify({'code': 1, 'msg': '请先登录'})
    
    if 'avatar' not in request.files:
        return jsonify({'code': 1, 'msg': '请选择图片'})
    
    file = request.files['avatar']
    if file.filename == '':
        return jsonify({'code': 1, 'msg': '请选择图片'})
    
    # 检查文件类型
    allowed_ext = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    import os
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_ext:
        return jsonify({'code': 1, 'msg': '只支持图片文件'})
    
    # 保存文件
    import uuid
    filename = str(uuid.uuid4()) + ext
    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'avatars')
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)
    
    # 更新数据库
    avatar_url = '/static/avatars/' + filename
    user = User.query.get(session['user_id'])
    user.avatar = avatar_url
    db.session.commit()
    
    return jsonify({'code': 0, 'msg': '上传成功', 'data': {'avatar': avatar_url}})

# ==================== 角色管理 ====================
@auth_bp.route('/admin/roles')
@permission_required('role_manage')
def roles_page():
    return render_template('auth/roles.html')

@auth_bp.route('/api/roles')
@permission_required('role_manage')
def api_roles():
    roles = Role.query.filter_by(status=1).all()
    roles_data = []
    has_super_admin = False
    
    for r in roles:
        r_dict = r.to_dict()
        # 检查是否已有超级管理员
        if getattr(r, 'is_super_admin', False):
            all_users = User.query.filter(User.status == 1).all()
            has_super_admin = any(is_super_admin_user(u) for u in all_users)
            r_dict['disabled'] = has_super_admin  # 标记是否禁用
        roles_data.append(r_dict)
    
    return jsonify({'code': 0, 'data': roles_data, 'has_super_admin': has_super_admin})

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
    
    # 记录日志
    add_log('role', '添加角色', f'角色名称: {role_name}', 'success')
    
    return jsonify({'code': 0, 'msg': '添加成功'})

@auth_bp.route('/api/roles/edit/<int:id>', methods=['POST'])
@permission_required('role_manage')
def api_roles_edit(id):
    data = request.json
    role = Role.query.get(id)
    if not role:
        return jsonify({'code': 1, 'msg': '角色不存在'})
    
    # 超级管理员不可修改
    if role.role_name == '超级管理员':
        return jsonify({'code': 1, 'msg': '超级管理员角色不可修改'})
    
    role_name = data.get('role_name', '').strip()
    permissions = data.get('permissions', [])
    
    # 检查名称重复
    existing = Role.query.filter(Role.role_name == role_name, Role.id != id, Role.status == 1).first()
    if existing:
        return jsonify({'code': 1, 'msg': '角色名称已存在'})
    
    role.role_name = role_name
    role.permissions = json.dumps(permissions)
    db.session.commit()
    
    # 记录日志
    add_log('role', '编辑角色', f'角色名称: {role_name}', 'success')
    
    return jsonify({'code': 0, 'msg': '修改成功'})

@auth_bp.route('/api/roles/delete/<int:id>', methods=['POST'])
@permission_required('role_manage')
def api_roles_delete(id):
    role = Role.query.get(id)
    if not role:
        return jsonify({'code': 1, 'msg': '角色不存在'})
    
    # 超级管理员不可删除
    if role.role_name == '超级管理员':
        return jsonify({'code': 1, 'msg': '超级管理员角色不可删除'})
    
    # 检查是否有用户使用该角色（role_ids包含该角色ID）
    all_users = User.query.filter_by(status=1).all()
    for u in all_users:
        if u.role_ids:
            role_id_list = [int(rid) for rid in u.role_ids.split(',') if rid]
            if id in role_id_list:
                return jsonify({'code': 1, 'msg': '该角色下有用户，无法删除'})
    
    role.status = 0
    db.session.commit()
    
    # 记录日志
    add_log('role', '删除角色', f'角色名称: {role.role_name}', 'success')
    
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
    # 获取所有用户（包括停用的）
    users = User.query.all()
    roles = Role.query.filter_by(status=1).all()
    
    users_data = []
    for u in users:
        u_dict = u.to_dict()
        u_dict['is_super_admin'] = is_super_admin_user(u)
        users_data.append(u_dict)
    
    return jsonify({'code': 0, 'data': users_data})

@auth_bp.route('/api/users/add', methods=['POST'])
@permission_required('user_manage')
def api_users_add():
    data = request.json
    name = data.get('name', '').strip()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    role_ids = data.get('role_ids', [])
    
    if not name:
        return jsonify({'code': 1, 'msg': '姓名不能为空'})
    
    if not username or not password:
        return jsonify({'code': 1, 'msg': '用户名和密码不能为空'})
    
    if User.query.filter_by(username=username).first():
        return jsonify({'code': 1, 'msg': '用户名已存在'})
    
    # 检查是否已有超级管理员
    all_users = User.query.filter(User.status == 1).all()
    if any(is_super_admin_user(u) for u in all_users):
        # 如果已有超级管理员，检查是否要分配超级管理员角色
        if 1 in role_ids:  # 1是超级管理员角色的ID
            return jsonify({'code': 1, 'msg': '系统已有超级管理员，不能重复创建'})
    
    user = User(
        name=name,
        username=username,
        password_hash=generate_password_hash(password),
        role_ids=','.join(map(str, role_ids)) if role_ids else '',
        status=1
    )
    db.session.add(user)
    db.session.commit()
    
    # 记录日志
    add_log('user', '添加用户', f'用户名: {username}, 姓名: {name}', 'success')
    
    return jsonify({'code': 0, 'msg': '添加成功'})

@auth_bp.route('/api/users/edit/<int:id>', methods=['POST'])
@permission_required('user_manage')
def api_users_edit(id):
    """编辑用户：启用/停用、修改角色"""
    data = request.json
    user = User.query.get(id)
    if not user:
        return jsonify({'code': 1, 'msg': '用户不存在'})
    
    # 超级管理员不能被停用/启用或修改角色
    if is_super_admin_user(user):
        return jsonify({'code': 1, 'msg': '超级管理员不能被修改'})
    
    # 启用/停用
    if 'status' in data:
        user.status = data['status']
    
    # 修改角色（多选）
    if 'role_ids' in data:
        user.role_ids = ','.join(map(str, data['role_ids'])) if data['role_ids'] else ''
    
    db.session.commit()
    
    # 记录日志
    if 'status' in data:
        action = '启用' if data['status'] == 1 else '停用'
        add_log('user', f'{action}用户', f'用户名: {user.username}', 'success')
    else:
        add_log('user', '修改用户角色', f'用户名: {user.username}', 'success')
    
    return jsonify({'code': 0, 'msg': '修改成功'})

@auth_bp.route('/api/users/reset_password/<int:id>', methods=['POST'])
@permission_required('user_manage')
def api_users_reset_password(id):
    """重置密码为8位数字"""
    import random
    user = User.query.get(id)
    if not user:
        return jsonify({'code': 1, 'msg': '用户不存在'})
    
    # 超级管理员不能被重置密码
    if is_super_admin_user(user):
        return jsonify({'code': 1, 'msg': '超级管理员不能重置密码'})
    
    new_password = str(random.randint(10000000, 99999999))
    user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    
    # 记录日志
    add_log('user', '重置密码', f'用户名: {user.username}', 'success')
    
    return jsonify({'code': 0, 'msg': '重置成功', 'password': new_password})

@auth_bp.route('/api/users/delete/<int:id>', methods=['POST'])
@permission_required('user_manage')
def api_users_delete(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'code': 1, 'msg': '用户不存在'})
    
    # 超级管理员不能被删除
    if is_super_admin_user(user):
        return jsonify({'code': 1, 'msg': '超级管理员不能被删除'})
    
    user.status = 0
    db.session.commit()
    
    # 记录日志
    add_log('user', '删除用户', f'用户名: {user.username}', 'success')
    
    return jsonify({'code': 0, 'msg': '删除成功'})
