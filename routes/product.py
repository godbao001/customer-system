# 产品管理路由
from flask import Blueprint, render_template, request, jsonify
from models import db, Product, ProductCategory, CategoryGroup, ProductCategoryValue, get_pinyin, get_pinyin_initial
from sqlalchemy import or_

product_bp = Blueprint('product', __name__, url_prefix='/product')

# ==================== 分类组管理 ====================

@product_bp.route('/group')
def group_list():
    return render_template('product/group.html')

# 获取分类组列表API
@product_bp.route('/api/group/list')
def api_group_list():
    groups = CategoryGroup.query.filter_by(status=1).order_by(CategoryGroup.sort_order, CategoryGroup.id).all()
    return jsonify({
        'code': 0,
        'msg': 'success',
        'data': [g.to_dict() for g in groups]
    })

# 添加分类组
@product_bp.route('/api/group/add', methods=['POST'])
def api_group_add():
    data = request.json
    existing = CategoryGroup.query.filter_by(group_name=data.get('group_name')).first()
    if existing:
        return jsonify({'code': 1, 'msg': '分类组名称已存在'})
    
    try:
        group = CategoryGroup(
            group_name=data.get('group_name'),
            sort_order=data.get('sort_order', 0)
        )
        db.session.add(group)
        db.session.commit()
        return jsonify({'code': 0, 'msg': '添加成功', 'data': group.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': f'添加失败: {str(e)}'})

# 编辑分类组
@product_bp.route('/api/group/edit/<int:id>', methods=['POST'])
def api_group_edit(id):
    data = request.json
    group = CategoryGroup.query.get(id)
    if not group:
        return jsonify({'code': 1, 'msg': '分类组不存在'})
    
    try:
        group.group_name = data.get('group_name', group.group_name)
        group.sort_order = data.get('sort_order', group.sort_order)
        db.session.commit()
        return jsonify({'code': 0, 'msg': '修改成功', 'data': group.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': f'修改失败: {str(e)}'})

# 删除分类组
@product_bp.route('/api/group/delete/<int:id>', methods=['POST'])
def api_group_delete(id):
    group = CategoryGroup.query.get(id)
    if not group:
        return jsonify({'code': 1, 'msg': '分类组不存在'})
    
    # 检查是否有分类
    has_categories = ProductCategory.query.filter_by(group_id=id).count() > 0
    if has_categories:
        return jsonify({'code': 1, 'msg': '请先删除该组下的分类'})
    
    try:
        db.session.delete(group)
        db.session.commit()
        return jsonify({'code': 0, 'msg': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': f'删除失败: {str(e)}'})


# ==================== 产品分类 ====================

# 分类列表页面
@product_bp.route('/category')
def category_list():
    return render_template('product/category.html')

# 获取分类列表API
@product_bp.route('/api/category/list')
def api_category_list():
    status = request.args.get('status', 1, type=int)
    categories = ProductCategory.query.filter_by(status=status).order_by(ProductCategory.group_id, ProductCategory.sort_order, ProductCategory.id).all()
    
    # 获取分类组
    groups = {g.id: g.group_name for g in CategoryGroup.query.filter_by(status=1).all()}
    
    result = []
    for c in categories:
        d = c.to_dict()
        d['group_name'] = groups.get(c.group_id, '')
        result.append(d)
    
    return jsonify({
        'code': 0,
        'msg': 'success',
        'data': result
    })

# 获取分类组和分类树API
@product_bp.route('/api/category/tree')
def api_category_tree():
    # 获取所有启用的分类组
    groups = CategoryGroup.query.filter_by(status=1).order_by(CategoryGroup.sort_order, CategoryGroup.id).all()
    
    tree = []
    for g in groups:
        # 获取该组下的所有分类
        categories = ProductCategory.query.filter_by(group_id=g.id, status=1).order_by(ProductCategory.sort_order).all()
        tree.append({
            'group_id': g.id,
            'group_name': g.group_name,
            
            'categories': [{'id': c.id, 'category_name': c.category_name, 'is_default': c.is_default} for c in categories]
        })
    
    return jsonify({
        'code': 0,
        'data': tree
    })

# 添加分类
@product_bp.route('/api/category/add', methods=['POST'])
def api_category_add():
    data = request.json
    
    # 检查名称是否重复（同组内）
    existing = ProductCategory.query.filter_by(
        category_name=data.get('category_name'),
        group_id=data.get('group_id', 0)
    ).first()
    if existing:
        return jsonify({'code': 1, 'msg': '分类名称已存在'})
    
    try:
        # 如果设为默认，先取消同组内其他默认
        if data.get('is_default') == 1:
            ProductCategory.query.filter_by(group_id=data.get('group_id', 0)).update({'is_default': 0})
        
        category = ProductCategory(
            category_name=data.get('category_name'),
            group_id=data.get('group_id', 0),
            sort_order=data.get('sort_order', 0),
            is_default=data.get('is_default', 0)
        )
        db.session.add(category)
        db.session.commit()
        return jsonify({'code': 0, 'msg': '添加成功', 'data': category.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': f'添加失败: {str(e)}'})

# 编辑分类
@product_bp.route('/api/category/edit/<int:id>', methods=['POST'])
def api_category_edit(id):
    data = request.json
    category = ProductCategory.query.get(id)
    if not category:
        return jsonify({'code': 1, 'msg': '分类不存在'})
    
    # 检查名称重复（同组内，排除自己）
    existing = ProductCategory.query.filter(
        ProductCategory.category_name == data.get('category_name'),
        ProductCategory.group_id == data.get('group_id', category.group_id),
        ProductCategory.id != id
    ).first()
    if existing:
        return jsonify({'code': 1, 'msg': '分类名称已存在'})
    
    try:
        # 如果设为默认，先取消同组内其他默认
        if data.get('is_default') == 1:
            ProductCategory.query.filter(
                ProductCategory.group_id == category.group_id,
                ProductCategory.id != id
            ).update({'is_default': 0})
        
        category.category_name = data.get('category_name', category.category_name)
        category.group_id = data.get('group_id', category.group_id)
        category.sort_order = data.get('sort_order', category.sort_order)
        category.is_default = data.get('is_default', category.is_default)
        db.session.commit()
        return jsonify({'code': 0, 'msg': '修改成功', 'data': category.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': f'修改失败: {str(e)}'})

# 删除分类
@product_bp.route('/api/category/delete/<int:id>', methods=['POST'])
def api_category_delete(id):
    category = ProductCategory.query.get(id)
    if not category:
        return jsonify({'code': 1, 'msg': '分类不存在'})
    
    # 检查是否有产品使用了该分类
    product_count = ProductCategoryValue.query.filter_by(category_id=id).count()
    if product_count > 0:
        return jsonify({'code': 1, 'msg': f'该分类已被 {product_count} 个产品使用，无法删除'})
    
    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'code': 0, 'msg': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': f'删除失败: {str(e)}'})


# ==================== 产品信息 ====================

# 产品列表页面
@product_bp.route('/')
def list():
    return render_template('product/list.html')

# 产品停用列表页面
@product_bp.route('/disabled')
def disabled():
    return render_template('product/disabled.html')

# 获取产品列表API
@product_bp.route('/api/list')
def api_list():
    status = request.args.get('status', 1, type=int)
    sales_status = request.args.get('sales_status', type=int)
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 12, type=int)
    search = request.args.get('search', '').strip()
    
    query = Product.query.filter_by(status=status)
    
    if sales_status is not None:
        query = query.filter_by(sales_status=sales_status)
    
    if search:
        query = query.filter(
            or_(
                Product.product_name.like(f'%{search}%'),
                Product.product_name_pinyin.like(f'%{search}%'),
                Product.product_name_initial.like(f'%{search}%'),
                Product.description.like(f'%{search}%')
            )
        )
    
    pagination = query.order_by(Product.id.desc()).paginate(page=page, per_page=limit, error_out=False)
    products = pagination.items
    
    # 获取分类组和分类信息
    groups = CategoryGroup.query.filter_by(status=1).all()
    group_map = {g.id: g.group_name for g in groups}
    
    result = []
    for p in products:
        d = p.to_dict(include_categories=True)
        # 整理分类显示
        category_display = []
        for cv in ProductCategoryValue.query.filter_by(product_id=p.id).all():
            cat = ProductCategory.query.get(cv.category_id) if cv.category_id else None
            category_display.append({
                'group_name': group_map.get(cv.group_id, ''),
                'category_name': cat.category_name if cat else ''
            })
        d['category_display'] = category_display
        result.append(d)
    
    return jsonify({
        'code': 0,
        'msg': 'success',
        'count': pagination.total,
        'data': result
    })

# 添加产品
@product_bp.route('/api/add', methods=['POST'])
def api_add():
    data = request.json
    
    product_name = data.get('product_name')
    
    # 检查产品名称是否重复
    existing = Product.query.filter_by(product_name=product_name).first()
    if existing:
        return jsonify({'code': 1, 'msg': '产品名称已存在'})
    
    # 生成拼音
    product_name_pinyin = get_pinyin(product_name)
    product_name_initial = get_pinyin_initial(product_name)
    
    try:
        product = Product(
            product_name=product_name,
            product_name_pinyin=product_name_pinyin,
            product_name_initial=product_name_initial,
            width=data.get('width', 0),
            height=data.get('height', 0),
            price=data.get('price', 0),
            unit=data.get('unit', ''),
            description=data.get('description', ''),
            sales_status=data.get('sales_status', 0),
            remark=data.get('remark', '')
        )
        db.session.add(product)
        db.session.flush()  # 获取product.id
        
        # 保存产品分类关联
        categories = data.get('categories', [])
        for cat in categories:
            pcv = ProductCategoryValue(
                product_id=product.id,
                group_id=cat.get('group_id'),
                category_id=cat.get('category_id') or None
            )
            db.session.add(pcv)
        
        db.session.commit()
        return jsonify({'code': 0, 'msg': '添加成功', 'data': product.to_dict(include_categories=True)})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': f'添加失败: {str(e)}'})

# 编辑产品
@product_bp.route('/api/edit/<int:id>', methods=['POST'])
def api_edit(id):
    data = request.json
    product = Product.query.get(id)
    if not product:
        return jsonify({'code': 1, 'msg': '产品不存在'})
    
    # 检查名称重复
    existing = Product.query.filter(Product.product_name == data.get('product_name'), Product.id != id).first()
    if existing:
        return jsonify({'code': 1, 'msg': '产品名称已存在'})
    
    # 更新拼音
    new_name = data.get('product_name', product.product_name)
    product_name_pinyin = get_pinyin(new_name)
    product_name_initial = get_pinyin_initial(new_name)
    
    try:
        product.product_name = new_name
        product.product_name_pinyin = product_name_pinyin
        product.product_name_initial = product_name_initial
        product.width = data.get('width', product.width)
        product.height = data.get('height', product.height)
        product.price = data.get('price', product.price)
        product.unit = data.get('unit', product.unit)
        product.description = data.get('description', product.description)
        product.sales_status = data.get('sales_status', product.sales_status)
        product.remark = data.get('remark', product.remark)
        
        # 更新产品分类关联
        # 先删除旧的
        ProductCategoryValue.query.filter_by(product_id=id).delete()
        
        # 添加新的
        categories = data.get('categories', [])
        for cat in categories:
            pcv = ProductCategoryValue(
                product_id=product.id,
                group_id=cat.get('group_id'),
                category_id=cat.get('category_id') or None
            )
            db.session.add(pcv)
        
        db.session.commit()
        return jsonify({'code': 0, 'msg': '修改成功', 'data': product.to_dict(include_categories=True)})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': f'修改失败: {str(e)}'})

# 停用/启用产品
@product_bp.route('/api/toggle_status/<int:id>', methods=['POST'])
def api_toggle_status(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'code': 1, 'msg': '产品不存在'})
    
    try:
        product.status = 0 if product.status == 1 else 1
        db.session.commit()
        return jsonify({'code': 0, 'msg': '操作成功', 'data': product.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': f'操作失败: {str(e)}'})

# 切换销售状态
@product_bp.route('/api/toggle_sales_status/<int:id>', methods=['POST'])
def api_toggle_sales_status(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'code': 1, 'msg': '产品不存在'})
    
    try:
        product.sales_status = 0 if product.sales_status == 1 else 1
        db.session.commit()
        return jsonify({'code': 0, 'msg': '操作成功', 'data': product.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': f'操作失败: {str(e)}'})

# 切换包邮状态
@product_bp.route('/api/toggle_free_shipping/<int:id>', methods=['POST'])
def api_toggle_free_shipping(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'code': 1, 'msg': '产品不存在'})
    
    try:
        product.free_shipping = 0 if product.free_shipping == 1 else 1
        db.session.commit()
        return jsonify({'code': 0, 'msg': '操作成功', 'data': product.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': f'操作失败: {str(e)}'})

# 删除产品
@product_bp.route('/api/delete/<int:id>', methods=['POST'])
def api_delete(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'code': 1, 'msg': '产品不存在'})
    
    try:
        # 删除产品分类关联
        ProductCategoryValue.query.filter_by(product_id=id).delete()
        db.session.delete(product)
        db.session.commit()
        return jsonify({'code': 0, 'msg': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 1, 'msg': f'删除失败: {str(e)}'})
