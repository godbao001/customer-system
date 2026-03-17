# 客户管理系统 API 文档

> 版本: 1.0  
> 最后更新: 2026-03-17

---

## 目录

1. [认证相关](#认证相关)
2. [店铺管理](#店铺管理)
3. [订单管理](#订单管理)
4. [产品管理](#产品管理)
5. [系统管理](#系统管理)
6. [统计报表](#统计报表)

---

## 认证相关

### 1.1 用户登录

**POST** `/api/login`

**请求体:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**响应:**
```json
{
  "code": 0,
  "msg": "登录成功",
  "data": {
    "user_id": 1,
    "username": "admin",
    "name": "管理员",
    "avatar": "/static/avatars/xxx.webp",
    "permissions": ["shop_view", "shop_add", ...]
  }
}
```

---

### 1.2 用户注册

**POST** `/api/register`

**请求体:**
```json
{
  "username": "newuser",
  "password": "password123",
  "confirm_password": "password123",
  "name": "新用户"
}
```

**响应:**
```json
{
  "code": 0,
  "msg": "注册成功"
}
```

---

### 1.3 获取当前用户权限

**GET** `/api/permissions`

**响应:**
```json
{
  "code": 0,
  "data": ["shop_view", "shop_add", "order_view", ...]
}
```

---

### 1.4 修改密码

**POST** `/api/profile/change_password`

**请求体:**
```json
{
  "old_password": "oldpass123",
  "new_password": "newpass123",
  "confirm_password": "newpass123"
}
```

**响应:**
```json
{
  "code": 0,
  "msg": "密码修改成功"
}
```

---

### 1.5 获取用户列表

**GET** `/api/users`

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| page | int | 页码，默认1 |
| limit | int | 每页数量，默认12 |
| search | string | 搜索用户名或姓名 |
| status | int | 状态筛选，1=启用，0=禁用 |

**响应:**
```json
{
  "code": 0,
  "msg": "success",
  "count": 10,
  "data": [
    {
      "id": 1,
      "username": "admin",
      "name": "管理员",
      "role_ids": "1,2",
      "role_names": "超级管理员、普通用户",
      "status": 1,
      "created_at": "2026-01-01 10:00:00"
    }
  ]
}
```

---

### 1.6 新增用户

**POST** `/api/users/add`

**请求体:**
```json
{
  "username": "newuser",
  "password": "password123",
  "name": "新用户",
  "role_ids": "1,2"
}
```

**响应:**
```json
{
  "code": 0,
  "msg": "添加成功",
  "data": {"id": 2}
}
```

---

### 1.7 编辑用户

**POST** `/api/users/edit/{id}`

**请求体:**
```json
{
  "name": "修改后的名字",
  "role_ids": "1"
}
```

---

### 1.8 重置用户密码

**POST** `/api/users/reset_password/{id}`

**响应:**
```json
{
  "code": 0,
  "msg": "重置成功",
  "password": "12345678"
}
```

---

### 1.9 删除用户

**POST** `/api/users/delete/{id}`

**响应:**
```json
{
  "code": 0,
  "msg": "删除成功"
}
```

---

### 1.10 获取角色列表

**GET** `/api/roles`

**响应:**
```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "role_name": "超级管理员",
      "permissions": ["shop_view", "shop_add", ...],
      "is_super_admin": true,
      "status": 1
    }
  ]
}
```

---

## 店铺管理

### 2.1 获取店铺列表

**GET** `/shop/api/list`

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| page | int | 页码 |
| limit | int | 每页数量 |
| status | int | 状态筛选 |
| search | string | 搜索店铺名/拼音 |
| search_id | string | 搜索店铺ID |
| business_model | string | 经营模式 |

**响应:**
```json
{
  "code": 0,
  "msg": "success",
  "count": 100,
  "data": [
    {
      "id": 1,
      "shop_name": "店铺名称",
      "shop_name_pinyin": "dianpumingcheng",
      "business_model": "经营模式",
      "province": "省份",
      "city": "城市",
      "address": "详细地址",
      "contact": "联系人",
      "phone": "电话",
      "status": 1,
      "created_at": "2026-01-01"
    }
  ]
}
```

---

### 2.2 添加店铺

**POST** `/shop/api/add`

**请求体:**
```json
{
  "shop_name": "店铺名称",
  "business_model": "经营模式",
  "province": "广东省",
  "city": "深圳市",
  "address": "详细地址",
  "contact": "联系人",
  "phone": "13800138000"
}
```

**响应:**
```json
{
  "code": 0,
  "msg": "添加成功",
  "data": {"id": 1}
}
```

---

### 2.3 编辑店铺

**POST** `/shop/api/edit/{id}`

**请求体:** 同添加店铺

---

### 2.4 删除店铺

**POST** `/shop/api/delete/{id}`

**响应:**
```json
{
  "code": 0,
  "msg": "删除成功"
}
```

---

### 2.5 恢复店铺

**POST** `/shop/api/restore/{id}`

---

### 2.6 检查店铺名称

**POST** `/shop/api/check_name`

**请求体:**
```json
{
  "name": "店铺名称",
  "id": "排除的店铺ID（编辑时使用）"
}
```

**响应:**
```json
{
  "code": 0,
  "exists": true
}
```

---

### 2.7 获取经营模式列表

**GET** `/shop/api/business_models`

**响应:**
```json
{
  "code": 0,
  "data": ["模式1", "模式2", ...]
}
```

---

## 订单管理

### 3.1 获取订单列表

**GET** `/order/api/list`

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| page | int | 页码 |
| limit | int | 每页数量 |
| status | int | 订单状态 |
| search | string | 搜索订单号/店铺名 |
| include_deleted | string | 是否包含已删除，1=是 |

**响应:**
```json
{
  "code": 0,
  "count": 50,
  "data": [
    {
      "id": 1,
      "order_no": "ORD20260317100001",
      "shop_id": 1,
      "shop_name": "店铺名称",
      "total_amount": 100.00,
      "status": 1,
      "created_at": "2026-03-17 10:00:00"
    }
  ]
}
```

---

### 3.2 获取订单详情

**GET** `/order/api/items/{id}`

**响应:**
```json
{
  "code": 0,
  "data": {
    "id": 1,
    "order_no": "ORD20260317100001",
    "shop": {...},
    "items": [
      {
        "id": 1,
        "product_name": "产品名称",
        "quantity": 2,
        "price": 50.00
      }
    ],
    "total_amount": 100.00,
    "status": 1,
    "created_at": "..."
  }
}
```

---

### 3.3 创建订单

**POST** `/order/api/add`

**请求体:**
```json
{
  "shop_id": 1,
  "items": [
    {"product_id": 1, "quantity": 2},
    {"product_id": 2, "quantity": 1}
  ]
}
```

---

### 3.4 更新订单

**POST** `/order/api/update/{id}`

**请求体:**
```json
{
  "items": [
    {"id": 1, "product_id": 1, "quantity": 3}
  ],
  "remark": "备注"
}
```

---

### 3.5 更新订单状态

**POST** `/order/api/update_status/{id}`

**请求体:**
```json
{
  "status": 2
}
```

---

### 3.6 删除订单

**POST** `/order/api/delete/{id}`

---

### 3.7 恢复订单

**POST** `/order/api/restore/{id}`

---

## 产品管理

### 4.1 获取产品列表

**GET** `/product/api/list`

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| page | int | 页码 |
| limit | int | 每页数量 |
| search | string | 搜索产品名 |
| category_id | int | 分类ID |
| status | int | 状态 |

**响应:**
```json
{
  "code": 0,
  "count": 100,
  "data": [
    {
      "id": 1,
      "product_name": "产品名称",
      "category_id": 1,
      "category_name": "分类名称",
      "price": 99.00,
      "status": 1,
      "is_on_sale": 1,
      "free_shipping": 0
    }
  ]
}
```

---

### 4.2 添加产品

**POST** `/product/api/add`

**请求体:**
```json
{
  "product_name": "产品名称",
  "category_id": 1,
  "price": 99.00,
  "stock": 100
}
```

---

### 4.3 编辑产品

**POST** `/product/api/edit/{id}`

---

### 4.4 删除产品

**POST** `/product/api/delete/{id}`

---

### 4.5 获取产品分类树

**GET** `/product/api/category/tree`

**响应:**
```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "name": "分类名称",
      "children": [
        {"id": 2, "name": "子分类"}
      ]
    }
  ]
}
```

---

## 系统管理

### 5.1 获取系统配置

**GET** `/system/api/basic/get`

**响应:**
```json
{
  "code": 0,
  "data": {
    "site_name": "客户管理系统",
    "site_logo": "/uploads/logo.png"
  }
}
```

---

### 5.2 保存系统配置

**POST** `/system/api/basic/save`

**请求体:**
```json
{
  "site_name": "新名称",
  "site_logo": "logo.png"
}
```

---

### 5.3 获取字段配置

**GET** `/system/api/field/list`

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| field_type | string | 字段类型 |

---

### 5.4 获取操作日志

**GET** `/system/api/log_list`

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| page | int | 页码 |
| limit | int | 每页数量 |
| category | string | 操作分类 |
| user_id | int | 用户ID |
| start_date | string | 开始日期 |
| end_date | string | 结束日期 |

**响应:**
```json
{
  "code": 0,
  "count": 100,
  "data": [
    {
      "id": 1,
      "username": "admin",
      "action": "登录系统",
      "category": "login",
      "ip": "10.0.1.100",
      "result": "success",
      "created_at": "2026-03-17 10:00:00"
    }
  ]
}
```

---

## 统计报表

### 6.1 店铺统计

**GET** `/stats/api/shop/summary`

**查询参数:**
| 参数 | 类型 | 说明 |
|------|------|------|
| start_date | string | 开始日期 |
| end_date | string | 结束日期 |

**响应:**
```json
{
  "code": 0,
  "data": {
    "total": 100,
    "active": 80,
    "inactive": 20
  }
}
```

---

### 6.2 订单统计

**GET** `/stats/api/order/summary`

**响应:**
```json
{
  "code": 0,
  "data": {
    "total_orders": 500,
    "pending": 50,
    "processing": 30,
    "completed": 400,
    "cancelled": 20
  }
}
```

---

### 6.3 营收统计

**GET** `/stats/api/revenue/summary`

**响应:**
```json
{
  "code": 0,
  "data": {
    "total_revenue": 50000.00,
    "month_revenue": 10000.00,
    "today_revenue": 500.00
  }
}
```

---

## 通用响应格式

### 成功响应
```json
{
  "code": 0,
  "msg": "成功消息",
  "data": {...}
}
```

### 错误响应
```json
{
  "code": 1,
  "msg": "错误消息"
}
```

### 分页响应
```json
{
  "code": 0,
  "count": 100,
  "data": [...],
  "page": 1,
  "limit": 12
}
```

---

## 错误代码

| code | 说明 |
|------|------|
| 0 | 成功 |
| 1 | 失败/错误 |
| 400 | 请求参数错误 |
| 401 | 未登录 |
| 403 | 没有权限 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |
