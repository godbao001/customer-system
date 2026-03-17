# 统计管理路由
from permissions import check_permission

from flask import Blueprint, render_template, request, jsonify, session
from models import db, Shop, Order, Product
from sqlalchemy import func
from datetime import datetime, timedelta
from utils.decorators import handle_errors

stats_bp = Blueprint('stats', __name__, url_prefix='/stats')


@stats_bp.route('/shop')
@check_permission('stats_view')
def shop():
    """店铺统计页面"""
    return render_template('stats/shop.html')


@stats_bp.route('/order')
@check_permission('stats_view')
def order():
    """订单统计页面"""
    return render_template('stats/order.html')


@stats_bp.route('/revenue')
@check_permission('stats_view')
def revenue():
    """营业额统计页面"""
    return render_template('stats/revenue.html')


# ============ API 接口 ============

@stats_bp.route('/api/shop/summary')
@check_permission('stats_view')
@handle_errors
def api_shop_summary():
    """获取店铺统计摘要"""
    # 店铺总数
    total_shops = Shop.query.filter_by(status=1).count()
    
    # 停用店铺数
    disabled_shops = Shop.query.filter_by(status=0).count()
    
    return jsonify({
        'code': 0,
        'data': {
            'total_shops': total_shops,
            'disabled_shops': disabled_shops
        }
    })


@stats_bp.route('/api/shop/by_province')
@check_permission('stats_view')
@handle_errors
def api_shop_by_province():
    """获取按省份统计的店铺数量"""
    shops = Shop.query.filter(Shop.province.isnot(None), Shop.province != '').all()
    
    province_count = {}
    for shop in shops:
        province = shop.province
        if province:
            province_count[province] = province_count.get(province, 0) + 1
    
    data = [{'name': k, 'value': v} for k, v in province_count.items()]
    
    return jsonify({
        'code': 0,
        'data': data
    })


@stats_bp.route('/api/shop/by_city')
@check_permission('stats_view')
@handle_errors
def api_shop_by_city():
    """获取按城市统计的店铺数量"""
    shops = Shop.query.filter(Shop.city.isnot(None), Shop.city != '').all()
    
    city_count = {}
    for shop in shops:
        city = shop.city
        if city:
            city_count[city] = city_count.get(city, 0) + 1
    
    data = [{'name': k, 'value': v} for k, v in city_count.items()]
    
    return jsonify({
        'code': 0,
        'data': data
    })


@stats_bp.route('/api/order/summary')
@check_permission('stats_view')
@handle_errors
def api_order_summary():
    """获取订单统计摘要"""
    from datetime import timedelta
    
    # 订单总数（排除已删除）
    total_orders = Order.query.filter_by(is_deleted=0).count()
    
    # 今日订单
    today = datetime.now().date()
    today_orders = Order.query.filter(
        func.date(Order.created_at) == today,
        Order.is_deleted == 0
    ).count()
    
    # 本月订单
    first_day_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0)
    month_orders = Order.query.filter(
        Order.created_at >= first_day_of_month,
        Order.is_deleted == 0
    ).count()
    
    # 本年订单
    first_day_of_year = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0)
    year_orders = Order.query.filter(
        Order.created_at >= first_day_of_year,
        Order.is_deleted == 0
    ).count()
    
    return jsonify({
        'code': 0,
        'data': {
            'total_orders': total_orders,
            'today_orders': today_orders,
            'month_orders': month_orders,
            'year_orders': year_orders
        }
    })


@stats_bp.route('/api/order/monthly')
@check_permission('stats_view')
@handle_errors
def api_order_monthly():
    """获取月度订单统计数据（过去12个月）"""
    from dateutil.relativedelta import relativedelta
    now = datetime.now()
    monthly_data = []
    
    for i in range(11, -1, -1):
        target_date = now - relativedelta(months=i)
        year = target_date.year
        month = target_date.month
        
        month_start = datetime(year, month, 1)
        if month == 12:
            month_end = datetime(year + 1, 1, 1) - timedelta(seconds=1)
        else:
            month_end = datetime(year, month + 1, 1) - timedelta(seconds=1)
        
        count = Order.query.filter(
            Order.created_at >= month_start,
            Order.created_at <= month_end,
            Order.is_deleted == 0
        ).count()
        
        monthly_data.append({
            'year': year,
            'month': month,
            'month_name': f'{month}月',
            'count': count
        })
    
    # 12个月的数据（包含环比同比）
    result_12 = []
    for i, item in enumerate(monthly_data[:12]):
        # 环比
        if i > 0:
            prev_count = monthly_data[i-1]['count']
            if prev_count > 0:
                环比 = round((item['count'] - prev_count) / prev_count * 100, 1)
            else:
                环比 = 100 if item['count'] > 0 else 0
        else:
            环比 = 0
        
        # 同比
        target_date = datetime(item['year'], item['month'], 1) - relativedelta(years=1)
        last_year_start = target_date.replace(day=1)
        if target_date.month == 12:
            last_year_end = target_date.replace(year=target_date.year+1, month=1, day=1) - timedelta(seconds=1)
        else:
            last_year_end = target_date.replace(month=target_date.month+1, day=1) - timedelta(seconds=1)
        
        same_count = Order.query.filter(
            Order.created_at >= last_year_start,
            Order.created_at <= last_year_end,
            Order.is_deleted == 0
        ).count()
        
        if same_count > 0:
            同比 = round((item['count'] - same_count) / same_count * 100, 1)
        else:
            同比 = 100 if item['count'] > 0 else 0
        
        result_12.append({
            'year': item['year'],
            'month': item['month'],
            'month_name': item['month_name'],
            'count': item['count'],
            '环比': 环比,
            '同比': 同比
        })
    
    # 30个月的数据
    result_30 = [{'year': m['year'], 'month': m['month'], 'month_name': m['month_name'], 'count': m['count']} for m in monthly_data]
    
    return jsonify({
        'code': 0,
        'data_12': result_12,
        'data_30': result_30
    })


@stats_bp.route('/api/order/yearly')
@check_permission('stats_view')
@handle_errors
def api_order_yearly():
    """获取年度订单统计数据（过去8年）"""
    now = datetime.now()
    yearly_data = []
    
    for i in range(7, -1, -1):
        year = now.year - i
        
        year_start = datetime(year, 1, 1)
        year_end = datetime(year, 12, 31, 23, 59, 59)
        
        count = Order.query.filter(
            Order.created_at >= year_start,
            Order.created_at <= year_end,
            Order.is_deleted == 0
        ).count()
        
        yearly_data.append({
            'year': year,
            'count': count
        })
    
    # 计算同比
    result = []
    for i, item in enumerate(yearly_data):
        if i > 0:
            prev_count = yearly_data[i-1]['count']
            if prev_count > 0:
                同比 = round((item['count'] - prev_count) / prev_count * 100, 1)
            else:
                同比 = 100 if item['count'] > 0 else 0
        else:
            同比 = 0
        
        result.append({
            'year': item['year'],
            'count': item['count'],
            '同比': 同比
        })
    
    return jsonify({
        'code': 0,
        'data': result
    })


@stats_bp.route('/api/revenue/summary')
@check_permission('stats_view')
@handle_errors
def api_revenue_summary():
    """获取营业额统计摘要（基于付款时间，状态>=2的订单即付款未制作以上都算入营业额）"""
    
    def get_revenue_query(date_start, date_end):
        """查询指定日期范围内的营业额"""
        return db.session.query(func.sum(Order.total_amount)).filter(
            Order.pay_time >= date_start,
            Order.pay_time <= date_end,
            Order.status >= 2,  # 大于或等于付款未制作状态
            Order.is_deleted == 0
        ).scalar() or 0
    
    # 总营业额（所有符合条件的订单）
    total = db.session.query(func.sum(Order.total_amount)).filter(
        Order.status >= 2,
        Order.is_deleted == 0,
        Order.pay_time.isnot(None)
    ).scalar() or 0
    
    # 今日营业额
    today = datetime.now().date()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    today_revenue = get_revenue_query(today_start, today_end)
    
    # 本月营业额
    first_day_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0)
    month_revenue = get_revenue_query(first_day_of_month, datetime.now())
    
    # 本年营业额
    first_day_of_year = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0)
    year_revenue = get_revenue_query(first_day_of_year, datetime.now())
    
    return jsonify({
        'code': 0,
        'data': {
            'total_revenue': float(total),
            'today_revenue': float(today_revenue),
            'month_revenue': float(month_revenue),
            'year_revenue': float(year_revenue)
        }
    })


@stats_bp.route('/api/revenue/monthly')
@check_permission('stats_view')
@handle_errors
def api_revenue_monthly():
    """获取月度营业额统计数据（过去12个月，基于付款时间）"""
    from dateutil.relativedelta import relativedelta
    now = datetime.now()
    monthly_data = []
    
    for i in range(11, -1, -1):
        # 计算该月的起始和结束日期
        target_date = now - relativedelta(months=i)
        year = target_date.year
        month = target_date.month
        
        month_start = datetime(year, month, 1)
        if month == 12:
            month_end = datetime(year + 1, 1, 1) - timedelta(seconds=1)
        else:
            month_end = datetime(year, month + 1, 1) - timedelta(seconds=1)
        
        # 统计该月营业额（基于付款时间，状态>=2）
        revenue = db.session.query(func.sum(Order.total_amount)).filter(
            Order.pay_time >= month_start,
            Order.pay_time <= month_end,
            Order.status >= 2,
            Order.is_deleted == 0
        ).scalar() or 0
        
        monthly_data.append({
            'year': year,
            'month': month,
            'month_name': f'{month}月',
            'revenue': float(revenue)
        })
    
    # 计算环比和同比（只对近12个月）
    result_12 = []
    for i, item in enumerate(monthly_data[:12]):
        # 环比
        if i > 0:
            prev_revenue = monthly_data[i-1]['revenue']
            if prev_revenue > 0:
                环比 = round((item['revenue'] - prev_revenue) / prev_revenue * 100, 1)
            else:
                环比 = 100 if item['revenue'] > 0 else 0
        else:
            环比 = 0
        
        # 同比（去年同月）
        target_date = datetime(item['year'], item['month'], 1) - relativedelta(years=1)
        last_year_start = target_date.replace(day=1)
        if target_date.month == 12:
            last_year_end = target_date.replace(year=target_date.year+1, month=1, day=1) - timedelta(seconds=1)
        else:
            last_year_end = target_date.replace(month=target_date.month+1, day=1) - timedelta(seconds=1)
        
        same_revenue = db.session.query(func.sum(Order.total_amount)).filter(
            Order.pay_time >= last_year_start,
            Order.pay_time <= last_year_end,
            Order.status >= 2,
            Order.is_deleted == 0
        ).scalar() or 0
        
        if same_revenue > 0:
            同比 = round((item['revenue'] - same_revenue) / same_revenue * 100, 1)
        else:
            同比 = 100 if item['revenue'] > 0 else 0
        
        result_12.append({
            'year': item['year'],
            'month': item['month'],
            'month_name': item['month_name'],
            'revenue': item['revenue'],
            '环比': 环比,
            '同比': 同比
        })
    
    # 30个月的数据（不含环比同比）
    result_30 = [{'year': m['year'], 'month': m['month'], 'month_name': m['month_name'], 'revenue': m['revenue']} for m in monthly_data]
    
    return jsonify({
        'code': 0,
        'data_12': result_12,
        'data_30': result_30
    })


@stats_bp.route('/api/revenue/yearly')
@check_permission('stats_view')
@handle_errors
def api_revenue_yearly():
    """获取年度营业额统计数据（过去8年）"""
    now = datetime.now()
    yearly_data = []
    
    for i in range(7, -1, -1):
        year = now.year - i
        
        year_start = datetime(year, 1, 1)
        year_end = datetime(year, 12, 31, 23, 59, 59)
        
        revenue = db.session.query(func.sum(Order.total_amount)).filter(
            Order.pay_time >= year_start,
            Order.pay_time <= year_end,
            Order.status >= 2,
            Order.is_deleted == 0
        ).scalar() or 0
        
        yearly_data.append({
            'year': year,
            'revenue': float(revenue)
        })
    
    # 计算同比
    result = []
    for i, item in enumerate(yearly_data):
        if i > 0:
            prev_revenue = yearly_data[i-1]['revenue']
            if prev_revenue > 0:
                同比 = round((item['revenue'] - prev_revenue) / prev_revenue * 100, 1)
            else:
                同比 = 100 if item['revenue'] > 0 else 0
        else:
            同比 = 0
        
        result.append({
            'year': item['year'],
            'revenue': item['revenue'],
            '同比': 同比
        })
    
    return jsonify({
        'code': 0,
        'data': result
    })
