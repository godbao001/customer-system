# 订单管理路由
from permissions import check_permission, ALL_PERMISSIONS

from flask import Blueprint, render_template, request, jsonify, abort, session, redirect
from models import db, Order, OrderItem, Shop
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from datetime import datetime
from utils.log import add_log
from config import Config
import random
import string
import json

order_bp = Blueprint('order', __name__, url_prefix='/order')

def generate_order_no():
    """生成订单号：日期+随机数"""
    now = datetime.now()
    date_str = now.strftime('%Y%m%d%H%M%S')
    random_str = ''.join(random.choices(string.digits, k=6))
    return f'ORD{date_str}{random_str}'

# 订单列表页面
@order_bp.route('/')
@check_permission('order_view')
def list():
    return render_template('order/list.html')

# 订单状态筛选页面
@order_bp.route('/status/<int:status>')
@check_permission('order_view')
def list_by_status(status):
    return render_template('order/list.html', status=status)

# 获取订单列表API
@order_bp.route('/api/list')
@check_permission('order_view')
def api_list():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 12, type=int)
    status = request.args.get('status', type=int)
    search = request.args.get('search', '').strip()
    include_deleted = request.args.get('include_deleted', '0') == '1'  # 是否包含已删除订单
    
    query = Order.query
    
    # 默认不显示已删除的订单
    if not include_deleted:
        query = query.filter_by(is_deleted=0)
    
    if status:
        query = query.filter_by(status=status)
    
    if search:
        query = query.join(Shop).filter(
            or_(
                Order.order_no.like(f'%{search}%'),
                Shop.shop_name.like(f'%{search}%')
            )
        )
    
    pagination = query.order_by(Order.id.desc()).paginate(page=page, per_page=limit, error_out=False)
    orders = pagination.items
    
    return jsonify({
        'code': 0,
        'msg': 'success',
        'count': pagination.total,
        'data': [o.to_dict() for o in orders]
    })


@order_bp.route('/api/deleted')
@check_permission('order_view')
def api_deleted():
    """获取已删除的订单列表"""
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 12, type=int)
    search = request.args.get('search', '').strip()
    
    query = Order.query.filter_by(is_deleted=1)
    
    if search:
        query = query.join(Shop).filter(
            or_(
                Order.order_no.like(f'%{search}%'),
                Shop.shop_name.like(f'%{search}%')
            )
        )
    
    pagination = query.order_by(Order.deleted_at.desc()).paginate(page=page, per_page=limit, error_out=False)
    orders = pagination.items
    
    return jsonify({
        'code': 0,
        'msg': 'success',
        'count': pagination.total,
        'data': [o.to_dict() for o in orders]
    })

# 获取所有店铺（下拉用）
@order_bp.route('/api/shops')
@check_permission('order_view')
def api_shops():
    shops = Shop.query.filter_by(status=1).order_by(Shop.id.desc()).all()
    return jsonify({
        'code': 0,
        'data': [{'id': s.id, 'shop_name': s.shop_name} for s in shops]
    })

# 获取店铺的产品（下单用）
@order_bp.route('/api/shop/products/<int:shop_id>')
@check_permission('order_view')
def api_shop_products(shop_id):
    # 这里应该查店铺的产品，暂时返回空列表
    return jsonify({
        'code': 0,
        'data': []
    })

# 获取店铺的订单
@order_bp.route('/api/shop/orders/<int:shop_id>')
@check_permission('order_view')
def api_shop_orders(shop_id):
    orders = Order.query.filter_by(shop_id=shop_id).order_by(Order.id.desc()).all()
    return jsonify({
        'code': 0,
        'data': [o.to_dict() for o in orders]
    })

# 获取订单明细
@order_bp.route('/api/items/<int:order_id>')
@check_permission('order_view')
def api_items(order_id):
    items = OrderItem.query.filter_by(order_id=order_id).all()
    return jsonify({
        'code': 0,
        'data': [item.to_dict() for item in items]
    })

# 更新订单（完整更新）
@order_bp.route('/api/update/<int:id>', methods=['POST'])
@check_permission('order_edit')
def api_update(id):
    data = request.json
    order = Order.query.get(id)
    if not order:
        return jsonify({'code': 1, 'msg': '订单不存在'})
    
    try:
        # 更新订单基本信息
        order.express_method = data.get('express_method', order.express_method)
        order.express_fee_type = data.get('express_fee_type', order.express_fee_type)
        order.express_shop_address = data.get('express_shop_address', order.express_shop_address)
        order.express_shop_phone = data.get('express_shop_phone', order.express_shop_phone)
        order.total_amount = data.get('total_amount', order.total_amount)
        order.remark = data.get('remark', order.remark)
        
        # 删除旧的订单明细
        OrderItem.query.filter_by(order_id=id).delete()
        
        # 创建新的订单明细
        items = data.get('items', [])
        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.get('product_id'),
                product_name=item.get('product_name', ''),
                price=item.get('price', 0),
                quantity=item.get('quantity', 1),
                width=item.get('width', 0),
                height=item.get('height', 0),
                original_width=item.get('original_width', item.get('width', 0)),
                original_height=item.get('original_height', item.get('height', 0)),
                remark=item.get('remark', ''),
                subtotal=item.get('subtotal', 0)
            )
            db.session.add(order_item)
        
        db.session.commit()
        return jsonify({'code': 0, 'msg': '保存成功', 'data': order.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': f'保存失败: {str(e)}'})

# 创建订单
@order_bp.route('/api/add', methods=['POST'])
@check_permission('order_edit')
def api_add():
    data = request.json
    
    shop_id = data.get('shop_id')
    
    if not shop_id:
        return jsonify({'code': 1, 'msg': '请选择店铺'})
    
    shop = Shop.query.get(shop_id)
    if not shop:
        return jsonify({'code': 1, 'msg': f'店铺不存在 (ID: {shop_id})'})
    
    try:
        # 生成订单号
        order_no = generate_order_no()
        
        # 计算总金额
        items = data.get('items', [])
        total_amount = sum(item.get('subtotal', 0) for item in items)
        
        # 快递费用
        express_fee = float(data.get('express_fee', 0) or 0)
        total_amount += express_fee  # 加上快递费用
        
        # 创建订单
        order = Order(
            order_no=order_no,
            shop_id=shop_id,
            total_amount=total_amount,
            remark=data.get('remark', ''),
            # 快递信息
            express_shop_address=data.get('express_shop_address', ''),
            express_shop_phone=data.get('express_shop_phone', ''),
            express_method=data.get('express_method', ''),
            express_fee_type=data.get('express_fee_type', ''),
            express_fee=express_fee
        )
        db.session.add(order)
        db.session.flush()
        
        # 创建订单明细
        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.get('product_id'),
                product_name=item.get('product_name', ''),
                price=item.get('price', 0),
                quantity=item.get('quantity', 1),
                width=item.get('width', 0),
                height=item.get('height', 0),
                original_width=item.get('original_width', item.get('width', 0)),
                original_height=item.get('original_height', item.get('height', 0)),
                remark=item.get('remark', ''),
                subtotal=item.get('subtotal', 0)
            )
            db.session.add(order_item)
        
        db.session.commit()
        
        # 记录日志
        add_log('order', '创建订单', f'订单号: {order.order_no}, 店铺: {shop.shop_name}', 'success')
        
        return jsonify({'code': 0, 'msg': '下单成功', 'data': order.to_dict()})
    except Exception as e:
        db.session.rollback()
        add_log('order', '创建订单', f'店铺ID: {shop_id}', 'fail')
        return jsonify({'code': 1, 'msg': f'下单失败: {str(e)}'})

# 更新订单状态
@order_bp.route('/api/update_status/<int:id>', methods=['POST'])
@check_permission('order_edit')
def api_update_status(id):
    data = request.json
    order = Order.query.get(id)
    if not order:
        return jsonify({'code': 1, 'msg': '订单不存在'})
    
    try:
        new_status = data.get('status', order.status)
        
        # 状态只能是1-6，不能跳过
        # 1下单未确认 -> 2确认未付款 -> 3付款未制作 -> 4制作未打包 -> 5发货未到货 -> 6已到货
        # 2确认未付款 可以退回 1下单未确认
        allowed_transitions = {
            1: [2, 3],      # 下单未确认 -> 确认订单/确认付款
            2: [1, 3],      # 确认未付款 -> 退回/确认付款
            3: [4],         # 付款未制作 -> 制作未打包
            4: [5],         # 制作未打包 -> 发货未到货
            5: [6],         # 发货未到货 -> 已到货
            6: []           # 已到货 -> 不可操作
        }
        
        if new_status not in allowed_transitions.get(order.status, []):
            return jsonify({'code': 1, 'msg': '不能将状态从 {} 改为 {}'.format(order.status, new_status)})
        
        # 保存原来的状态
        old_status = order.status
        order.status = new_status
        
        # 根据状态自动设置时间
        if new_status == 2:
            order.confirm_time = datetime.now()
        elif new_status == 3:
            # 如果是从状态1（下单未确认）直接到状态3（付款未制作），确认时间和付款时间都设置
            if old_status == 1:
                order.confirm_time = datetime.now()
            order.pay_time = datetime.now()
        elif new_status == 4:
            order.make_time = datetime.now()
        elif new_status == 5:
            order.pack_time = datetime.now()
        
        # 如果是退回状态，清除相关时间
        if new_status == 1:
            order.confirm_time = None
        
        db.session.commit()
        
        # 记录日志
        from models import ORDER_STATUS
        old_status_text = ORDER_STATUS.get(old_status, '')
        new_status_text = ORDER_STATUS.get(new_status, '')
        add_log('order', '更新订单状态', f'订单号: {order.order_no}, {old_status_text} → {new_status_text}', 'success')
        
        return jsonify({'code': 0, 'msg': '状态更新成功', 'data': order.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': f'更新失败: {str(e)}'})

# 编辑订单
@order_bp.route('/api/edit/<int:id>', methods=['POST'])
@check_permission('order_edit')
def api_edit(id):
    data = request.json
    order = Order.query.get(id)
    if not order:
        return jsonify({'code': 1, 'msg': '订单不存在'})
    
    try:
        order.express_method = data.get('express_method', order.express_method)
        order.express_fee_type = data.get('express_fee_type', order.express_fee_type)
        order.express_shop_address = data.get('express_shop_address', order.express_shop_address)
        order.express_shop_phone = data.get('express_shop_phone', order.express_shop_phone)
        order.total_amount = data.get('total_amount', order.total_amount)
        order.remark = data.get('remark', order.remark)
        
        db.session.commit()
        
        # 记录日志
        add_log('order', '编辑订单', f'订单号: {order.order_no}', 'success')
        
        return jsonify({'code': 0, 'msg': '保存成功', 'data': order.to_dict()})
    except Exception as e:
        db.session.rollback()
        add_log('order', '编辑订单', f'订单ID: {id}', 'fail')
        return jsonify({'code': 1, 'msg': f'保存失败: {str(e)}'})

# 删除订单
@order_bp.route('/api/delete/<int:id>', methods=['POST'])
@check_permission('order_delete')
def api_delete(id):
    """软删除订单"""
    order = Order.query.get(id)
    if not order:
        return jsonify({'code': 1, 'msg': '订单不存在'})
    
    try:
        order.is_deleted = 1
        order.deleted_at = datetime.now()
        db.session.commit()
        
        # 记录日志
        add_log('order', '删除订单', f'订单号: {order.order_no}', 'success')
        
        return jsonify({'code': 0, 'msg': '删除成功'})
    except Exception as e:
        db.session.rollback()
        add_log('order', '删除订单', f'订单ID: {id}', 'fail')
        return jsonify({'code': 1, 'msg': f'删除失败: {str(e)}'})


@order_bp.route('/api/restore/<int:id>', methods=['POST'])
@check_permission('order_delete')
def api_restore(id):
    """恢复已删除的订单"""
    order = Order.query.get(id)
    if not order:
        return jsonify({'code': 1, 'msg': '订单不存在'})
    
    try:
        order.is_deleted = 0
        order.deleted_at = None
        db.session.commit()
        
        # 记录日志
        add_log('order', '恢复订单', f'订单号: {order.order_no}', 'success')
        
        return jsonify({'code': 0, 'msg': '恢复成功'})
    except Exception as e:
        db.session.rollback()
        add_log('order', '恢复订单', f'订单ID: {id}', 'fail')
        return jsonify({'code': 1, 'msg': f'恢复失败: {str(e)}'})

# 下单页面（新增订单）
@order_bp.route('/add/<int:shop_id>')
@check_permission('order_edit')
def add(shop_id):
    shop = Shop.query.get(shop_id)
    if not shop:
        abort(404)
    # 创建一个空的order对象用于模板
    order = type('Order', (), {
        'id': None,
        'shop_id': shop_id,
        'shop': shop,
        'express_shop_address': shop.address or '',
        'express_shop_phone': shop.phone or '',
        'express_method': '',
        'express_fee_type': '',
        'remark': '',
        'total_amount': 0
    })()
    return render_template('order/edit.html', order=order, is_new=True)

# 订单编辑页面
@order_bp.route('/edit/<int:id>')
@check_permission('order_edit')
def edit(id):
    order = Order.query.options(joinedload(Order.shop)).get(id)
    if not order:
        abort(404)
    items = OrderItem.query.filter_by(order_id=id).all()
    return render_template('order/edit.html', order=order, is_new=False)

# 订单详情
@order_bp.route('/detail/<int:id>')
@check_permission('order_view')
def detail(id):
    from sqlalchemy.orm import joinedload
    order = Order.query.options(joinedload(Order.shop)).get(id)
    if not order:
        abort(404)
    items = OrderItem.query.filter_by(order_id=id).all()
    return render_template('order/detail.html', order=order, items=items)
