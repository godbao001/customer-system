# 店铺管理路由
from flask import Blueprint, render_template, request, jsonify
from models import db, Shop, Order, get_pinyin, get_pinyin_initial
from sqlalchemy import or_, func
from utils.address_parser import parse_address
from utils.kuaibao_parser import clear_address

shop_bp = Blueprint('shop', __name__, url_prefix='/shop')

# 店铺列表（正常状态）
@shop_bp.route('/')
def list():
    return render_template('shop/list.html')

# 店铺停用列表
@shop_bp.route('/disabled')
def disabled():
    return render_template('shop/disabled.html')

# 获取店铺列表API
@shop_bp.route('/api/list')
def api_list():
    status = request.args.get('status', 1, type=int)
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    search_id = request.args.get('search_id', '', type=str).strip()
    search = request.args.get('search', '').strip()
    business_model = request.args.get('business_model', '').strip()
    
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
    # 先获取总数（不受分页影响）
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
        shop_dict['last_order_time'] = order_stats.last_order_time.strftime('%Y-%m-%d %H:%M:%S') if order_stats.last_order_time else ''
        
        shop_data.append(shop_dict)
    
    return jsonify({
        'code': 0,
        'msg': 'success',
        'count': total_count,
        'data': shop_data
    })

# 添加店铺
@shop_bp.route('/api/add', methods=['POST'])
def api_add():
    data = request.json
    
    # 检查店铺名称是否重复
    existing = Shop.query.filter_by(shop_name=data.get('shop_name')).first()
    if existing:
        return jsonify({'code': 1, 'msg': '店铺名称已存在'})
    
    # 使用前端解析好的地址信息
    region = data.get('region', '')
    province = data.get('province', '')
    city = data.get('city', '')
    district = data.get('district', '')
    detail = data.get('detail', '')
    address = data.get('address', '')
    
    # 如果地址不为空，检查地址是否重复（使用解析后的字段）
    if address and address.strip():
        if not region or not province or not city or not district or not detail:
            return jsonify({'code': 1, 'msg': '地址信息不完整，请检查大区、省、市、区县、详细地址'})
        
        # 检查地址是否重复
        existing_addr = Shop.query.filter_by(
            region=region,
            province=province,
            city=city,
            district=district,
            address=detail
        ).first()
        if existing_addr:
            return jsonify({'code': 1, 'msg': '该地址已存在'})
    
    # 生成店铺名称拼音
    shop_name_pinyin = get_pinyin(data.get('shop_name', ''))
    shop_name_initial = get_pinyin_initial(data.get('shop_name', ''))
    
    # 生成地址拼音
    full_addr = region + province + city + district + (detail or '')
    address_pinyin = get_pinyin(full_addr)
    address_initial = get_pinyin_initial(full_addr)
    
    try:
        shop = Shop(
            shop_name=data.get('shop_name'),
            shop_name_pinyin=shop_name_pinyin,
            shop_name_initial=shop_name_initial,
            business_model=data.get('business_model'),
            phone=data.get('phone'),
            region=region,
            province=province,
            city=city,
            district=district,
            address=detail,
            address_pinyin=address_pinyin,
            address_initial=address_initial,
            remark=data.get('remark', '')
        )
        db.session.add(shop)
        db.session.commit()
        return jsonify({'code': 0, 'msg': '添加成功', 'data': shop.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': f'添加失败: {str(e)}'})

# 获取单个店铺详情
@shop_bp.route('/api/get/<int:id>')
def api_get(id):
    shop = Shop.query.get(id)
    if not shop:
        return jsonify({'code': 1, 'msg': '店铺不存在'})
    return jsonify({'code': 0, 'data': shop.to_dict()})

# 编辑店铺
@shop_bp.route('/api/edit/<int:id>', methods=['POST'])
def api_edit(id):
    data = request.json
    shop = Shop.query.get(id)
    if not shop:
        return jsonify({'code': 1, 'msg': '店铺不存在'})
    
    # 检查店铺名称是否重复（排除自己）
    new_name = data.get('shop_name')
    existing = Shop.query.filter(Shop.shop_name == new_name, Shop.id != id).first()
    if existing:
        return jsonify({'code': 1, 'msg': '店铺名称已存在'})
    
    # 使用前端解析好的地址信息
    region = data.get('region', '')
    province = data.get('province', '')
    city = data.get('city', '')
    district = data.get('district', '')
    detail = data.get('detail', '')
    address = data.get('address', '')
    
    # 如果地址不为空，检查地址是否重复（使用解析后的字段）
    if address and address.strip():
        if not region or not province or not city or not district or not detail:
            return jsonify({'code': 1, 'msg': '地址信息不完整，请检查大区、省、市、区县、详细地址'})
        
        # 检查地址是否重复（排除自己）
        existing_addr = Shop.query.filter(
            Shop.region == region,
            Shop.province == province,
            Shop.city == city,
            Shop.district == district,
            Shop.address == detail,
            Shop.id != id
        ).first()
        if existing_addr:
            return jsonify({'code': 1, 'msg': '该地址已存在'})
    
    # 生成店铺名称拼音
    shop_name_pinyin = get_pinyin(data.get('shop_name', ''))
    shop_name_initial = get_pinyin_initial(data.get('shop_name', ''))
    
    # 生成地址拼音
    full_addr = region + province + city + district + (detail or '')
    address_pinyin = get_pinyin(full_addr)
    address_initial = get_pinyin_initial(full_addr)
    
    try:
        shop.shop_name = data.get('shop_name', shop.shop_name)
        shop.shop_name_pinyin = shop_name_pinyin
        shop.shop_name_initial = shop_name_initial
        shop.business_model = data.get('business_model', shop.business_model)
        shop.phone = data.get('phone', shop.phone)
        shop.region = region
        shop.province = province
        shop.city = city
        shop.district = district
        shop.address = detail
        shop.address_pinyin = address_pinyin
        shop.address_initial = address_initial
        shop.remark = data.get('remark', shop.remark)
        db.session.commit()
        return jsonify({'code': 0, 'msg': '修改成功', 'data': shop.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': f'修改失败: {str(e)}'})

# 停用/启用店铺
@shop_bp.route('/api/toggle_status/<int:id>', methods=['POST'])
def api_toggle_status(id):
    shop = Shop.query.get(id)
    if not shop:
        return jsonify({'code': 1, 'msg': '店铺不存在'})
    
    try:
        shop.status = 0 if shop.status == 1 else 1
        db.session.commit()
        return jsonify({'code': 0, 'msg': '操作成功', 'data': shop.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': f'操作失败: {str(e)}'})

# 删除店铺
@shop_bp.route('/api/delete/<int:id>', methods=['POST'])
def api_delete(id):
    shop = Shop.query.get(id)
    if not shop:
        return jsonify({'code': 1, 'msg': '店铺不存在'})
    
    try:
        db.session.delete(shop)
        db.session.commit()
        return jsonify({'code': 0, 'msg': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': f'删除失败: {str(e)}'})

# 检查店铺名称API
@shop_bp.route('/api/check_name', methods=['POST'])
def api_check_name():
    """检查店铺名称是否重复"""
    data = request.json
    name = data.get('name', '').strip()
    shop_id = data.get('id', '')
    
    if not name:
        return jsonify({'code': 0, 'msg': 'success'})
    
    # 查询是否重名
    query = Shop.query.filter_by(shop_name=name, status=1)
    if shop_id:
        query = query.filter(Shop.id != int(shop_id))
    
    exists = query.first()
    
    if exists:
        return jsonify({'code': 1, 'msg': '店铺名称已存在'})
    
    return jsonify({'code': 0, 'msg': 'success'})

# 地址解析API
@shop_bp.route('/api/parse_address', methods=['POST'])
def api_parse_address():
    """智能解析地址（使用快宝API）"""
    data = request.json
    address = data.get('address', '')
    
    if not address:
        return jsonify({'code': 1, 'msg': '请输入地址'})
    
    # 调用快宝API解析
    result = clear_address(address)
    
    if 'error' in result:
        return jsonify({'code': 1, 'msg': result['error']})
    
    return jsonify({
        'code': 0,
        'msg': 'success',
        'data': {
            'region': result.get('region', ''),
            'province': result.get('province', ''),
            'city': result.get('city', ''),
            'district': result.get('district', ''),
            'town': result.get('town', ''),
            'detail': result.get('detail', '')
        }
    })
