# -*- coding: utf-8 -*-
"""
店铺管理路由模块

提供店铺（客户）的增删改查等操作接口。
"""
from typing import Optional, Dict, List, Any
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for

from permissions import check_permission, ALL_PERMISSIONS
from models import db, Shop, Order, get_pinyin, get_pinyin_initial
from sqlalchemy import or_, func
from utils.address_parser import parse_address
from utils.kuaibao_parser import clear_address
from utils.log import add_log
from utils.decorators import handle_errors
from config import Config
import json

shop_bp = Blueprint('shop', __name__, url_prefix='/shop')


@shop_bp.route('/')
@check_permission('shop_view')
def list() -> str:
    """
    店铺列表页面
    
    Returns:
        店铺列表 HTML 页面
    """
    return render_template('shop/list.html')


@shop_bp.route('/disabled')
@check_permission('shop_view')
def disabled() -> str:
    """
    店铺停用列表页面
    
    Returns:
        停用店铺列表 HTML 页面
    """
    return render_template('shop/disabled.html')


@shop_bp.route('/api/list')
@check_permission('shop_view')
@handle_errors
def api_list() -> Dict[str, Any]:
    """
    获取店铺列表 API
    
    Query Parameters:
        status: 店铺状态 (1=正常, 0=停用)
        page: 页码
        limit: 每页数量
        search: 搜索关键词
        search_id: ID精确搜索
        business_model: 经营模式筛选
    
    Returns:
        JSON 包含店铺列表和分页信息
    """
    status: int = request.args.get('status', 1, type=int)
    page: int = request.args.get('page', 1, type=int)
    limit: int = request.args.get('limit', Config.PAGE_DEFAULT_LIMIT, type=int)
    search_id: str = request.args.get('search_id', '', type=str).strip()
    search: str = request.args.get('search', '').strip()
    business_model: str = request.args.get('business_model', '').strip()
    
    # 分页参数安全限制
    if page < 1:
        page = 1
    if limit < 1:
        limit = Config.PAGE_DEFAULT_LIMIT
    if limit > Config.PAGE_MAX_LIMIT:
        limit = Config.PAGE_MAX_LIMIT
    
    # ID精确搜索优先
    if search_id:
        query = Shop.query.filter_by(status=status, id=int(search_id))
    else:
        query = Shop.query.filter_by(status=status)
        
        # 经营模式筛选
        if business_model:
            query = query.filter_by(business_model=business_model)
        
        # 搜索功能（支持中文、拼音、拼音首字母）
        if search:
            query = query.filter(
                or_(
                    Shop.shop_name.like(f'%{search}%'),
                    Shop.phone.like(f'%{search}%'),
                    Shop.address.like(f'%{search}%'),
                    Shop.shop_name_pinyin.like(f'%{search}%'),
                    Shop.shop_name_initial.like(f'%{search}%'),
                    Shop.province.like(f'%{search}%'),
                    Shop.city.like(f'%{search}%'),
                    Shop.district.like(f'%{search}%'),
                    Shop.address_pinyin.like(f'%{search}%'),
                    Shop.address_initial.like(f'%{search}%')
                )
            )
    
    # 分页
    total_count = query.count()
    
    pagination = query.order_by(Shop.id.desc()).paginate(page=page, per_page=limit, error_out=False)
    shops = pagination.items
    
    # 为每个店铺添加订单统计信息
    shop_data = []
    for shop in shops:
        shop_dict = shop.to_dict()
        
        # 查询订单统计
        order_stats = db.session.query(
            func.count(Order.id).label('order_count'),
            func.coalesce(func.sum(Order.total_amount), 0).label('total_amount'),
            func.max(Order.order_time).label('last_order_time')
        ).filter(Order.shop_id == shop.id).first()
        
        shop_dict['order_count'] = order_stats.order_count or 0
        shop_dict['total_amount'] = float(order_stats.total_amount or 0)
        shop_dict['last_order_time'] = order_stats.last_order_time.strftime('%Y-%m-%d %H:%M') if order_stats.last_order_time else ''
        
        shop_data.append(shop_dict)
    
    return jsonify({
        'code': 0,
        'msg': 'success',
        'count': total_count,
        'data': shop_data,
        'page': page,
        'limit': limit
    })



@shop_bp.route('/api/get/<int:id>')
@check_permission('shop_view')
@handle_errors
def api_get(id: int) -> Dict[str, Any]:
    """
    获取单个店铺详情
    
    Args:
        id: 店铺ID
    
    Returns:
        JSON 店铺详情
    """
    shop = Shop.query.get(id)
    if not shop:
        return jsonify({'code': 1, 'msg': '店铺不存在'})
    
    return jsonify({
        'code': 0,
        'msg': 'success',
        'data': shop.to_dict()
    })

@shop_bp.route('/api/add', methods=['POST'])
@check_permission('shop_add')
@handle_errors
def api_add() -> Dict[str, Any]:
    """
    添加店铺 API
    
    Request JSON:
        shop_name: 店铺名称
        phone: 电话
        address: 地址
        province/city/district: 省市区
        business_model: 经营模式
        free_shipping: 是否包邮
        remark: 备注
    
    Returns:
        JSON 添加结果
    """
    data = request.json
    shop_name = data.get('shop_name', '').strip()
    
    if not shop_name:
        return jsonify({'code': 1, 'msg': '店铺名称不能为空'})
    
    # 检查店铺名称是否已存在
    existing = Shop.query.filter_by(shop_name=shop_name).first()
    if existing:
        return jsonify({'code': 1, 'msg': '店铺名称已存在'})
    
    # 解析地址
    address = data.get('address', '')
    province = data.get('province', '')
    city = data.get('city', '')
    district = data.get('district', '')
    
    if address and not (province and city):
        parsed = parse_address(address)
        province = province or parsed.get('province', '')
        city = city or parsed.get('city', '')
        district = district or parsed.get('district', '')
    
    # 获取拼音
    shop_name_pinyin = get_pinyin(shop_name) if shop_name else ''
    shop_name_initial = get_pinyin_initial(shop_name) if shop_name else ''
    address_pinyin = get_pinyin(address) if address else ''
    address_initial = get_pinyin_initial(address) if address else ''
    
    # 检查地址是否已存在
    if address and province and city and district:
        existing_addr = Shop.query.filter_by(
            province=province,
            city=city,
            district=district,
            address=address,
            status=1
        ).first()
        if existing_addr:
            return jsonify({'code': 1, 'msg': '该地址已存在'})
    
    # 创建店铺
    shop = Shop(
        shop_name=shop_name,
        shop_name_pinyin=shop_name_pinyin,
        shop_name_initial=shop_name_initial,
        phone=data.get('phone', ''),
        province=province,
        city=city,
        district=district,
        address=address,
        address_pinyin=address_pinyin,
        address_initial=address_initial,
        business_model=data.get('business_model', ''),
        free_shipping=data.get('free_shipping', 0),
        remark=data.get('remark', ''),
        status=1
    )
    
    db.session.add(shop)
    db.session.commit()
    
    # 记录操作日志
    add_log('shop', '添加店铺', f'店铺名称: {shop_name}', 'success')
    
    return jsonify({'code': 0, 'msg': '添加成功', 'data': {'id': shop.id}})


@shop_bp.route('/api/edit/<int:id>', methods=['POST'])
@check_permission('shop_edit')
@handle_errors
def api_edit(id: int) -> Dict[str, Any]:
    """
    编辑店铺 API
    
    Args:
        id: 店铺ID
    
    Request JSON:
        shop_name: 店铺名称
        phone: 电话
        address: 地址
        province/city/district: 省市区
        business_model: 经营模式
        free_shipping: 是否包邮
        remark: 备注
    
    Returns:
        JSON 编辑结果
    """
    shop = Shop.query.get(id)
    if not shop:
        return jsonify({'code': 1, 'msg': '店铺不存在'})
    
    data = request.json
    new_name = data.get('shop_name', '').strip()
    
    if not new_name:
        return jsonify({'code': 1, 'msg': '店铺名称不能为空'})
    
    # 检查名称是否重复
    existing = Shop.query.filter(Shop.shop_name == new_name, Shop.id != id).first()
    if existing:
        return jsonify({'code': 1, 'msg': '店铺名称已存在'})
    
    # 地址重复检查
    address = data.get('address', '')
    province = data.get('province', '')
    city = data.get('city', '')
    district = data.get('district', '')
    
    if address and province and city and district:
        existing_addr = Shop.query.filter(
            Shop.province == province,
            Shop.city == city,
            Shop.district == district,
            Shop.address == address,
            Shop.id != id,
            Shop.status == 1
        ).first()
        if existing_addr:
            return jsonify({'code': 1, 'msg': '该地址已存在'})
    
    # 更新店铺信息
    old_name = shop.shop_name
    shop.shop_name = new_name
    shop.shop_name_pinyin = get_pinyin(new_name) if new_name else ''
    shop.shop_name_initial = get_pinyin_initial(new_name) if new_name else ''
    shop.phone = data.get('phone', '')
    shop.province = province
    shop.city = city
    shop.district = district
    shop.address = address
    shop.address_pinyin = get_pinyin(address) if address else ''
    shop.address_initial = get_pinyin_initial(address) if address else ''
    shop.business_model = data.get('business_model', '')
    shop.free_shipping = data.get('free_shipping', 0)
    shop.remark = data.get('remark', '')
    
    db.session.commit()
    
    # 记录操作日志
    add_log('shop', '编辑店铺', f'店铺: {old_name} -> {new_name}', 'success')
    
    return jsonify({'code': 0, 'msg': '修改成功'})


@shop_bp.route('/api/delete/<int:id>', methods=['POST'])
@check_permission('shop_delete')
@handle_errors
def api_delete(id: int) -> Dict[str, Any]:
    """
    删除（停用）店铺 API
    
    Args:
        id: 店铺ID
    
    Returns:
        JSON 删除结果
    """
    shop = Shop.query.get(id)
    if not shop:
        return jsonify({'code': 1, 'msg': '店铺不存在'})
    
    # 软删除（停用）
    shop.status = 0
    db.session.commit()
    
    # 记录操作日志
    add_log('shop', '删除店铺', f'店铺名称: {shop.shop_name}', 'success')
    
    return jsonify({'code': 0, 'msg': '删除成功'})


@shop_bp.route('/api/restore/<int:id>', methods=['POST'])
@check_permission('shop_edit')
@handle_errors
def api_restore(id: int) -> Dict[str, Any]:
    """
    恢复已删除（停用）的店铺 API
    
    Args:
        id: 店铺ID
    
    Returns:
        JSON 恢复结果
    """
    shop = Shop.query.get(id)
    if not shop:
        return jsonify({'code': 1, 'msg': '店铺不存在'})
    
    # 恢复
    shop.status = 1
    db.session.commit()
    
    # 记录操作日志
    add_log('shop', '恢复店铺', f'店铺名称: {shop.shop_name}', 'success')
    
    return jsonify({'code': 0, 'msg': '恢复成功'})


@shop_bp.route('/api/check_name', methods=['GET', 'POST'])
@check_permission('shop_view')
@handle_errors
def api_check_name() -> Dict[str, Any]:
    """
    检查店铺名称是否已存在
    
    Query Parameters (GET) / Request JSON (POST):
        name: 店铺名称
        shop_id: 排除的店铺ID（编辑时使用）
    
    Returns:
        JSON 检查结果
    """
    # 支持 GET 和 POST 两种方式
    if request.method == 'POST':
        data = request.json or {}
        name = data.get('name', '').strip()
        shop_id = data.get('shop_id', '').strip()
    else:
        name = request.args.get('name', '').strip()
        shop_id = request.args.get('shop_id', '').strip()
    
    if not name:
        return jsonify({'code': 0, 'exists': False})
    
    if shop_id:
        exists = Shop.query.filter(Shop.shop_name == name, Shop.id != int(shop_id), Shop.status == 1).first()
    else:
        exists = Shop.query.filter_by(shop_name=name, status=1).first()
    
    return jsonify({'code': 0, 'exists': bool(exists)})


@shop_bp.route('/api/business_models')
@check_permission('shop_view')
@handle_errors
def api_business_models() -> Dict[str, Any]:
    """
    获取所有经营模式
    
    Returns:
        JSON 经营模式列表
    """
    models = db.session.query(Shop.business_model).filter(
        Shop.business_model != '',
        Shop.business_model is not None,
        Shop.status == 1
    ).distinct().all()
    
    return jsonify({
        'code': 0,
        'data': [m[0] for m in models if m[0]]
    })


@check_permission('shop_edit')
@shop_bp.route('/api/toggle_status/<int:id>', methods=['POST'])
@handle_errors
def api_toggle_status(id: int) -> Dict[str, Any]:
    """
    启用/停用客户
    
    Args:
        id: 客户ID
    
    Returns:
        JSON 操作结果
    """
    shop = Shop.query.get(id)
    if not shop:
        return jsonify({'code': 1, 'msg': '客户不存在'})
    
    # 切换状态
    new_status = 0 if shop.status == 1 else 1
    shop.status = new_status
    
    db.session.commit()
    
    # 记录日志
    action = '启用客户' if new_status == 1 else '停用客户'
    add_log('shop', action, f'客户ID: {id}, 名称: {shop.shop_name}')
    
    status_text = '启用' if new_status == 1 else '停用'
    return jsonify({'code': 0, 'msg': f'{status_text}成功'})
