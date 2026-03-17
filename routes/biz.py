# 业务管理路由
from permissions import check_permission, ALL_PERMISSIONS
from flask import Blueprint, render_template, request, jsonify, session

biz_bp = Blueprint('biz', __name__, url_prefix='/biz')

# 生成制作页面
@biz_bp.route('/generate')
@check_permission('biz_generate')
def generate():
    """生成制作页面"""
    return render_template('biz/generate.html')

# 强制修改页面
@biz_bp.route('/force_edit')
@check_permission('biz_force_edit')
def force_edit():
    """强制修改页面"""
    return render_template('biz/force_edit.html')
