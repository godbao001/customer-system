# 数据库模型
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Shop(db.Model):
    __tablename__ = 'shops'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shop_name = db.Column(db.String(100), nullable=False, comment='店铺名称')
    shop_name_pinyin = db.Column(db.String(255), comment='店铺名称拼音')
    shop_name_initial = db.Column(db.String(50), comment='店铺名称拼音首字母')
    business_model = db.Column(db.String(50), comment='经营模式')
    phone = db.Column(db.String(20), comment='电话')
    region = db.Column(db.String(20), comment='大区')
    province = db.Column(db.String(50), comment='省份')
    city = db.Column(db.String(50), comment='市/县')
    district = db.Column(db.String(50), comment='区')
    address = db.Column(db.String(255), comment='详细地址')
    address_pinyin = db.Column(db.String(255), comment='地址拼音')
    address_initial = db.Column(db.String(50), comment='地址拼音首字母')
    status = db.Column(db.Integer, default=1, comment='状态: 1=正常, 0=停用')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    remark = db.Column(db.Text, comment='备注')
    free_shipping = db.Column(db.Integer, default=0, comment='是否包邮: 1=是, 0=否')
    
    def to_dict(self):
        return {
            'id': self.id,
            'shop_name': self.shop_name,
            'shop_name_pinyin': self.shop_name_pinyin or '',
            'shop_name_initial': self.shop_name_initial or '',
            'business_model': self.business_model,
            'phone': self.phone,
            'region': self.region or '',
            'province': self.province or '',
            'city': self.city or '',
            'district': self.district or '',
            'address': self.address or '',
            'address_pinyin': self.address_pinyin or '',
            'address_initial': self.address_initial or '',
            'status': self.status,
            
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else '',
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else '',
            'remark': self.remark or '',
            'free_shipping': self.free_shipping or 0
        }


# 产品分类组模型
class CategoryGroup(db.Model):
    __tablename__ = 'category_groups'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_name = db.Column(db.String(100), nullable=False, comment='分类组名称')
    sort_order = db.Column(db.Integer, default=0, comment='排序')
    is_default = db.Column(db.Integer, default=0, comment='是否为默认: 1=是, 0=否')
    color = db.Column(db.String(50), default='', comment='颜色')
    status = db.Column(db.Integer, default=1, comment='状态: 1=正常, 0=停用')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'group_name': self.group_name,
            'sort_order': self.sort_order,
            'is_default': self.is_default,
            'color': self.color or '',
            'status': self.status,
            
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else '',
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else ''
        }


# 产品分类模型
class ProductCategory(db.Model):
    __tablename__ = 'product_categories'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(100), nullable=False, comment='分类名称')
    group_id = db.Column(db.Integer, default=0, comment='所属分类组')
    parent_id = db.Column(db.Integer, default=0, comment='父分类ID')
    sort_order = db.Column(db.Integer, default=0, comment='排序')
    status = db.Column(db.Integer, default=1, comment='状态: 1=正常, 0=停用')
    is_default = db.Column(db.Integer, default=0, comment='是否为默认分类: 1=是, 0=否')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'category_name': self.category_name,
            'group_id': self.group_id,
            'parent_id': self.parent_id,
            'sort_order': self.sort_order,
            'is_default': self.is_default,
            'color': self.color or '',
            'status': self.status,
            'is_default': self.is_default,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else '',
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else ''
        }


# 产品分类值模型（产品与分类的关联）
class ProductCategoryValue(db.Model):
    __tablename__ = 'product_category_values'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, nullable=False, comment='产品ID')
    group_id = db.Column(db.Integer, nullable=False, comment='分类组ID')
    category_id = db.Column(db.Integer, nullable=True, comment='分类ID')
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # 显式指定外键
    __table_args__ = (
        db.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'group_id': self.group_id,
            'category_id': self.category_id
        }


# 产品模型
class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(100), nullable=False, comment='产品名称')
    product_name_pinyin = db.Column(db.String(255), comment='产品名称拼音')
    product_name_initial = db.Column(db.String(50), comment='产品名称拼音首字母')
    width = db.Column(db.Numeric(10, 2), default=0, comment='宽度')
    height = db.Column(db.Numeric(10, 2), default=0, comment='高度')
    price = db.Column(db.Numeric(10, 2), default=0.00, comment='单价')
    unit = db.Column(db.String(20), default='', comment='单位')
    description = db.Column(db.Text, comment='产品描述')
    sales_status = db.Column(db.Integer, default=0, comment='销售状态: 1=在售, 0=停售')
    status = db.Column(db.Integer, default=1, comment='状态: 1=正常, 0=停用')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    remark = db.Column(db.Text, comment='备注')
    free_shipping = db.Column(db.Integer, default=0, comment='是否包邮: 1=是, 0=否')
    
    def to_dict(self, include_categories=False):
        result = {
            'id': self.id,
            'product_name': self.product_name,
            'product_name_pinyin': self.product_name_pinyin or '',
            'product_name_initial': self.product_name_initial or '',
            'width': float(self.width) if self.width else 0,
            'height': float(self.height) if self.height else 0,
            'price': float(self.price) if self.price else 0,
            'unit': self.unit or '',
            'description': self.description or '',
            'sales_status': self.sales_status,
            'status': self.status,
            
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else '',
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else '',
            'remark': self.remark or '',
            'free_shipping': self.free_shipping or 0
        }
        if include_categories:
            # 获取产品的分类信息
            categories = []
            for cv in ProductCategoryValue.query.filter_by(product_id=self.id).all():
                cat = ProductCategory.query.get(cv.category_id) if cv.category_id else None
                categories.append({
                    'group_id': cv.group_id,
                    'category_id': cv.category_id,
                    'category_name': cat.category_name if cat else ''
                })
            result['categories'] = categories
        return result


# 拼音工具函数
from pypinyin import lazy_pinyin, Style

def get_pinyin(text):
    """获取汉字的拼音"""
    if not text:
        return ''
    return ''.join(lazy_pinyin(text, style=Style.NORMAL))

def get_pinyin_initial(text):
    """获取汉字的拼音首字母"""
    if not text:
        return ''
    return ''.join(lazy_pinyin(text, style=Style.FIRST_LETTER))


# 订单状态常量
ORDER_STATUS = {
    1: '下单未确认',
    2: '确认未付款',
    3: '付款未制作',
    4: '制作为打包',
    5: '打包未发货',
    6: '发货未到货',
    7: '已到货'
}

# 订单模型
class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_no = db.Column(db.String(50), nullable=False, unique=True, comment='订单号')
    shop_id = db.Column(db.Integer, nullable=False, comment='店铺ID')
    total_amount = db.Column(db.Numeric(10, 2), default=0.00, comment='订单总金额')
    status = db.Column(db.Integer, default=1, comment='订单状态: 1=下单未确认, 2=确认未付款, 3=付款未制作, 4=制作为打包, 5=打包未发货, 6=发货未到货, 7=已到货')
    remark = db.Column(db.Text, comment='备注')
    free_shipping = db.Column(db.Integer, default=0, comment='是否包邮: 1=是, 0=否')
    # 状态时间
    order_time = db.Column(db.DateTime, default=datetime.now, comment='下单时间')
    confirm_time = db.Column(db.DateTime, nullable=True, comment='确认时间')
    pay_time = db.Column(db.DateTime, nullable=True, comment='付款时间')
    make_time = db.Column(db.DateTime, nullable=True, comment='制作时间')
    pack_time = db.Column(db.DateTime, nullable=True, comment='打包时间')
    # 快递信息
    express_shop_address = db.Column(db.String(255), comment='门店地址')
    express_shop_phone = db.Column(db.String(50), comment='门店电话')
    express_method = db.Column(db.String(50), comment='快递方式: 顺丰快递, 自提, 送货, 滴滴')
    express_fee_type = db.Column(db.String(20), comment='快递费用类型: 寄付, 到付')
    express_fee = db.Column(db.Numeric(10, 2), default=0.00, comment='快递费用')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 关联关系
    shop = db.relationship('Shop', backref='orders', foreign_keys=[shop_id])
    
    # 显式指定外键
    __table_args__ = (
        db.ForeignKeyConstraint(['shop_id'], ['shops.id'], ondelete='CASCADE'),
    )
    
    def to_dict(self):
        # 获取店铺名称
        shop = Shop.query.get(self.shop_id)
        return {
            'id': self.id,
            'order_no': self.order_no,
            'shop_id': self.shop_id,
            'shop_name': shop.shop_name if shop else '',
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'status': self.status,
            
            'status_text': self.get_status_text(),
            'remark': self.remark or '',
            'free_shipping': self.free_shipping or 0,
            # 状态时间
            'order_time': self.order_time.strftime('%Y-%m-%d %H:%M:%S') if self.order_time else '',
            'confirm_time': self.confirm_time.strftime('%Y-%m-%d %H:%M:%S') if self.confirm_time else '',
            'pay_time': self.pay_time.strftime('%Y-%m-%d %H:%M:%S') if self.pay_time else '',
            'make_time': self.make_time.strftime('%Y-%m-%d %H:%M:%S') if self.make_time else '',
            'pack_time': self.pack_time.strftime('%Y-%m-%d %H:%M:%S') if self.pack_time else '',
            # 快递信息
            'express_shop_address': self.express_shop_address or '',
            'express_shop_phone': self.express_shop_phone or '',
            'express_method': self.express_method or '',
            'express_fee_type': self.express_fee_type or '',
            'express_fee': float(self.express_fee) if self.express_fee else 0,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else '',
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else ''
        }
    
    def get_status_text(self):
        return ORDER_STATUS.get(self.status, '未知')


# 订单明细模型
class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, nullable=False, comment='订单ID')
    product_id = db.Column(db.Integer, comment='产品ID')
    product_name = db.Column(db.String(100), comment='产品名称')
    price = db.Column(db.Numeric(10, 2), default=0.00, comment='单价')
    quantity = db.Column(db.Integer, default=1, comment='数量')
    width = db.Column(db.Numeric(10, 2), default=0, comment='宽度')
    height = db.Column(db.Numeric(10, 2), default=0, comment='高度')
    original_width = db.Column(db.Numeric(10, 2), default=0, comment='原始宽度')
    original_height = db.Column(db.Numeric(10, 2), default=0, comment='原始高度')
    remark = db.Column(db.String(255), default='', comment='备注')
    free_shipping = db.Column(db.Integer, default=0, comment='是否包邮: 1=是, 0=否')
    subtotal = db.Column(db.Numeric(10, 2), default=0.00, comment='小计')
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def is_custom(self):
        """判断是否为定制：宽高变化或有备注"""
        orig_w = float(self.original_width) if self.original_width else 0
        orig_h = float(self.original_height) if self.original_height else 0
        curr_w = float(self.width) if self.width else 0
        curr_h = float(self.height) if self.height else 0
        return curr_w != orig_w or curr_h != orig_h or (self.remark and self.remark.strip())
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_name': self.product_name or '',
            'price': float(self.price) if self.price else 0,
            'quantity': self.quantity,
            'width': float(self.width) if self.width else 0,
            'height': float(self.height) if self.height else 0,
            'original_width': float(self.original_width) if self.original_width else 0,
            'original_height': float(self.original_height) if self.original_height else 0,
            'remark': self.remark or '',
            'free_shipping': self.free_shipping or 0,
            'subtotal': float(self.subtotal) if self.subtotal else 0,
            'is_custom': self.is_custom()
        }


# ==================== 系统配置 ====================

class SystemConfig(db.Model):
    __tablename__ = 'system_config'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    config_key = db.Column(db.String(50), unique=True, nullable=False, comment='配置键')
    config_value = db.Column(db.Text, comment='配置值')
    config_type = db.Column(db.String(20), default='text', comment='类型: text/text/number/image')
    description = db.Column(db.String(200), comment='描述')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'config_key': self.config_key,
            'config_value': self.config_value,
            'config_type': self.config_type,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else '',
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else ''
        }


class FieldConfig(db.Model):
    __tablename__ = 'field_config'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    field_type = db.Column(db.String(50), nullable=False, comment='字段类型: express_method/express_fee_type')
    field_name = db.Column(db.String(100), nullable=False, comment='字段显示名称')
    field_value = db.Column(db.String(200), nullable=False, comment='字段值')
    sort_order = db.Column(db.Integer, default=0, comment='排序')
    is_default = db.Column(db.Integer, default=0, comment='是否为默认: 1=是, 0=否')
    color = db.Column(db.String(20), default='', comment='标记颜色')
    status = db.Column(db.Integer, default=1, comment='状态: 1=启用, 0=停用')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'field_type': self.field_type,
            'field_name': self.field_name,
            'field_value': self.field_value,
            'sort_order': self.sort_order,
            'is_default': self.is_default,
            'color': self.color or '',
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else '',
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else ''
        }
