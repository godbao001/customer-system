# 系统管理路由
from permissions import check_permission, ALL_PERMISSIONS

from flask import Blueprint, render_template, request, jsonify, send_from_directory, session, redirect
from models import db, SystemConfig, FieldConfig, OperationLog
from utils.log import add_log
from utils.decorators import handle_errors
import os
import uuid
import json

system_bp = Blueprint('system', __name__, url_prefix='/system')

# ==================== 首页 ====================

@system_bp.route('/')
@check_permission('system_basic')
def index():
    return render_template('system/basic.html')


# ==================== 基础管理 ====================

@system_bp.route('/basic')
@check_permission('system_basic')
def basic():
    return render_template('system/basic.html')


@system_bp.route('/api/basic/get')
@check_permission('system_basic')
@handle_errors
def api_basic_get():
    """获取系统基础配置"""
    configs = SystemConfig.query.all()
    result = {}
    for c in configs:
        result[c.config_key] = c.config_value
    return jsonify({'code': 0, 'data': result})


@system_bp.route('/api/basic/save', methods=['POST'])
@check_permission('system_basic')
@handle_errors
def api_basic_save():
    """保存系统基础配置"""
    data = request.json
    
    try:
        # 处理包邮金额，转换为整数
        if 'free_shipping_amount' in data:
            data['free_shipping_amount'] = str(int(data.get('free_shipping_amount') or 0))
        
        for key, value in data.items():
            config = SystemConfig.query.filter_by(config_key=key).first()
            if config:
                config.config_value = value
            else:
                config = SystemConfig(config_key=key, config_value=value, config_type='text')
                db.session.add(config)
        
        db.session.commit()
        
        # 记录日志
        keys = ', '.join(data.keys())
        add_log('system', '系统设置', f'修改配置: {keys}', 'success')
        
        return jsonify({'code': 0, 'msg': '保存成功'})
    except Exception as e:
        db.session.rollback()
        add_log('system', '系统设置', f'修改配置失败', 'fail')
        return jsonify({'code': 1, 'msg': f'保存失败: {str(e)}'})


@system_bp.route('/api/upload', methods=['POST'])
@check_permission('system_basic')
@handle_errors
def api_upload():
    """上传文件"""
    if 'file' not in request.files:
        return jsonify({'code': 1, 'msg': '没有文件'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'code': 1, 'msg': '文件名不能为空'})
    
    # 获取文件扩展名
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        return jsonify({'code': 1, 'msg': '只支持图片文件'})
    
    # 生成新文件名
    filename = str(uuid.uuid4()) + ext
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    # 保存到配置
    config_key = request.form.get('config_key', 'logo')
    config = SystemConfig.query.filter_by(config_key=config_key).first()
    if config:
        config.config_value = '/static/uploads/' + filename
    else:
        config = SystemConfig(config_key=config_key, config_value='/static/uploads/' + filename, config_type='image')
        db.session.add(config)
    db.session.commit()
    
    return jsonify({'code': 0, 'msg': '上传成功', 'data': '/static/uploads/' + filename})


# ==================== 字段管理 ====================

@system_bp.route('/field')
@check_permission('system_field')
def field():
    return render_template('system/field.html')


@system_bp.route('/api/field/list')
@check_permission('system_field')
@handle_errors
def api_field_list():
    """获取字段配置列表"""
    field_type = request.args.get('field_type', '')
    
    query = FieldConfig.query
    if field_type:
        query = query.filter_by(field_type=field_type)
    
    fields = query.order_by(FieldConfig.field_type, FieldConfig.sort_order).all()
    return jsonify({'code': 0, 'data': [f.to_dict() for f in fields]})


@system_bp.route('/api/field/save', methods=['POST'])
@check_permission('system_field')
@handle_errors
def api_field_save():
    """保存字段配置"""
    data = request.json
    
    field_type = data.get('field_type')
    field_name = data.get('field_name')
    field_value = data.get('field_value')
    sort_order = data.get('sort_order', 0)
    is_default = data.get('is_default', 0)
    color = data.get('color', '')
    id = data.get('id')
    
    try:
        # 如果设置为默认，先取消同类型的其他默认
        if is_default == 1:
            FieldConfig.query.filter_by(field_type=field_type, is_default=1).update({'is_default': 0})
        
        if id:
            # 更新
            field = FieldConfig.query.get(id)
            if field:
                field.field_name = field_name
                field.field_value = field_value
                field.sort_order = sort_order
                field.is_default = is_default
                field.color = color
        else:
            # 新增
            field = FieldConfig(
                field_type=field_type,
                field_name=field_name,
                field_value=field_value,
                sort_order=sort_order,
                is_default=is_default,
                color=color
            )
            db.session.add(field)
        
        db.session.commit()
        return jsonify({'code': 0, 'msg': '保存成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': f'保存失败: {str(e)}'})


@system_bp.route('/api/field/delete/<int:id>', methods=['POST'])
@check_permission('user_manage')
def api_field_delete(id):
    """删除字段配置"""
    field = FieldConfig.query.get(id)
    if not field:
        return jsonify({'code': 1, 'msg': '记录不存在'})
    
    try:
        db.session.delete(field)
        db.session.commit()
        return jsonify({'code': 0, 'msg': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': f'删除失败: {str(e)}'})


@system_bp.route('/api/field/options')
@check_permission('system_field')
@handle_errors
def api_field_options():
    """获取字段选项（用于下拉选择）"""
    field_type = request.args.get('field_type')
    
    fields = FieldConfig.query.filter_by(field_type=field_type, status=1).order_by(FieldConfig.sort_order).all()
    return jsonify({'code': 0, 'data': [f.to_dict() for f in fields]})


# ==================== 日志管理 ====================

@system_bp.route('/log')
@check_permission('system_log')
def log():
    return render_template('system/log.html')


@system_bp.route('/api/log/list')
@check_permission('system_log')
@handle_errors
def api_log_list():
    """获取日志列表"""
    category = request.args.get('category', '')
    result = request.args.get('result', '')
    keyword = request.args.get('keyword', '')
    date = request.args.get('date', '')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    
    query = OperationLog.query
    
    # 按分类筛选
    if category:
        query = query.filter_by(category=category)
    
    # 按结果筛选
    if result:
        query = query.filter_by(result=result)
    
    # 按日期筛选
    if date:
        from datetime import datetime
        try:
            start_date = datetime.strptime(date, '%Y-%m-%d')
            end_date = datetime.strptime(date, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
            query = query.filter(OperationLog.created_at >= start_date, OperationLog.created_at <= end_date)
        except:
            pass  # 日期格式错误则忽略
    
    # 关键词搜索（搜索操作人、操作动作、操作详情）
    if keyword:
        query = query.filter(
            db.or_(
                OperationLog.username.ilike(f'%{keyword}%'),
                OperationLog.user_name.ilike(f'%{keyword}%'),
                OperationLog.action.ilike(f'%{keyword}%'),
                OperationLog.detail.ilike(f'%{keyword}%')
            )
        )
    
    # 按时间倒序
    query = query.order_by(OperationLog.created_at.desc())
    
    # 分页
    total = query.count()
    logs = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return jsonify({
        'code': 0, 
        'data': [log.to_dict() for log in logs], 
        'total': total,
        'page': page,
        'page_size': page_size
    })


@system_bp.route('/api/log/categories')
@check_permission('system_log')
@handle_errors
def api_log_categories():
    """获取日志分类统计"""
    date = request.args.get('date', '')
    
    query = OperationLog.query
    
    # 按日期筛选
    if date:
        from datetime import datetime
        try:
            start_date = datetime.strptime(date, '%Y-%m-%d')
            end_date = datetime.strptime(date, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
            query = query.filter(OperationLog.created_at >= start_date, OperationLog.created_at <= end_date)
        except:
            pass
    
    # 统计每个分类的日志数量
    categories = query.with_entities(
        OperationLog.category, 
        db.func.count(OperationLog.id)
    ).group_by(OperationLog.category).all()
    
    result = []
    total = 0
    for cat, count in categories:
        result.append({
            'category': cat,
            'category_name': OperationLog.CATEGORY_NAMES.get(cat, cat),
            'count': count
        })
        total += count
    
    # 添加"全部"选项
    result.insert(0, {'category': '', 'category_name': '全部', 'count': total})
    
    return jsonify({'code': 0, 'data': result})
