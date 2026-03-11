# 主路由
from flask import Blueprint, render_template, session, redirect, url_for

main_bp = Blueprint('main', __name__)

# 登录检查装饰器
def login_required(f):
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        user = session.get('user_id')
        if not user:
            return redirect('/login')
        return f(*args, **kwargs)
    wrapped.__name__ = f.__name__
    return wrapped

@main_bp.route('/')
@login_required
def index():
    return render_template('index.html')
