# 分页工具
from flask import request
from config import Config

def get_pagination_params():
    """获取分页参数
    
    Returns:
        tuple: (page, limit)
    """
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', Config.PAGE_DEFAULT_LIMIT, type=int)
    
    # 限制 page 最小为 1
    if page < 1:
        page = 1
    
    # 限制 limit 在合理范围内
    if limit < 1:
        limit = Config.PAGE_DEFAULT_LIMIT
    elif limit > Config.PAGE_MAX_LIMIT:
        limit = Config.PAGE_MAX_LIMIT
    
    return page, limit

def paginate_query(query, page=None, limit=None):
    """分页查询
    
    Args:
        query: SQLAlchemy 查询对象
        page: 页码（可选，默认从请求获取）
        limit: 每页数量（可选，默认从请求获取）
    
    Returns:
        dict: 包含分页信息的字典
    """
    if page is None or limit is None:
        page, limit = get_pagination_params()
    
    pagination = query.order_by().paginate(
        page=page, 
        per_page=limit, 
        error_out=False
    )
    
    return {
        'page': page,
        'limit': limit,
        'total': pagination.total,
        'pages': pagination.pages,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev,
        'items': pagination.items
    }
