/**
 * 店铺管理页面脚本
 */

// 全局变量
var currentPage = 1;
var currentShopId = null;
var businessModelColors = {};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 等待权限加载完成
    var checkCount = 0;
    var checkPermissions = function() {
        checkCount++;
        var perms = window.userPermissions || [];
        
        // 隐藏添加按钮（需要shop_add权限）
        if (perms.length > 0 && !perms.includes('shop_add')) {
            var addBtn = document.getElementById('addCustomerBtn');
            if (addBtn) addBtn.style.display = 'none';
        }
        
        // 刷新表格数据
        if (typeof loadData === 'function') {
            loadData(1);
        }
    };
    checkPermissions();
});

// 监听权限加载完成
document.addEventListener('permissionsLoaded', function() {
    if (typeof loadData === 'function') {
        loadData(1);
    }
});

// ==================== Toast 提示 ====================
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast-item alert alert-${type} alert-dismissible`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    toastContainer.appendChild(toast);
    
    // 3秒后自动消失
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// ==================== 加载数据 ====================
function loadData(page) {
    if (page !== undefined) {
        currentPage = page;
    }
    
    const search = document.getElementById('searchInput').value;
    const searchId = document.getElementById('searchIdInput').value;
    
    let businessModel = '';
    const activeBtn = document.querySelector('.business-model-btn.active');
    if (activeBtn && activeBtn.textContent !== '全部') {
        businessModel = activeBtn.value;
    }
    
    const params = new URLSearchParams({
        status: 1,
        page: page,
        limit: 12,
        search: search,
        search_id: searchId,
        business_model: businessModel
    });
    
    fetch(`/shop/api/list?${params}`)
        .then(res => res.json())
        .then(data => {
            if (data.code === 0) {
                document.getElementById('totalCount').textContent = `共 ${data.count} 个店铺`;
                renderTable(data.data);
                renderPagination(data.count, page);
            }
        });
}

// ==================== 渲染表格 ====================
function renderTable(data) {
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = '';
    
    const columnSettings = getColumnSettings();
    const visibleColumns = Object.values(columnSettings).filter(v => v).length;
    
    if (data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="${visibleColumns}" class="text-center text-muted py-4"><i class="bi bi-inbox" style="font-size: 2rem;"></i><p class="mt-2">暂无数据</p></td></tr>`;
        return;
    }
    
    // 搜索关键词高亮
    const searchKeyword = document.getElementById('searchInput').value;
    
    data.forEach(item => {
        const addressParts = [item.region, item.province, item.city, item.district, item.address].filter(Boolean);
        const address = addressParts.join(' ');
        
        const tr = document.createElement('tr');
        tr.style.cursor = 'pointer';
        tr.ondblclick = function() {
            showOrderModal(item.id, item.shop_name);
        };
        
        // 经营模式背景色
        const businessModel = item.business_model;
        if (businessModel && businessModelColors[businessModel]) {
            const colorClass = businessModelColors[businessModel];
            let bgColor = getColorBg(colorClass);
            if (bgColor && bgColor !== 'transparent') {
                tr.style.setProperty('background-color', bgColor, 'important');
            }
        }
        // 如果没有经营模式或没有配置颜色，背景色保持默认白色（不处理）
        
        let html = '';
        
        if (columnSettings.id) html += `<td>${item.id}</td>`;
        if (columnSettings.shop_name) html += `<td>${highlightKeyword(item.shop_name || '', searchKeyword)}</td>`;
        if (columnSettings.phone) html += `<td>${item.phone || ''}</td>`;
        if (columnSettings.address) html += `<td>${highlightKeyword(address, searchKeyword)}</td>`;
        if (columnSettings.order_count) html += `<td>${item.order_count || 0}</td>`;
        if (columnSettings.total_amount) html += `<td>¥${parseFloat(item.total_amount || 0).toFixed(2)}</td>`;
        if (columnSettings.last_order_time) html += `<td>${item.last_order_time || ''}</td>`;
        if (columnSettings.created_at) html += `<td>${item.created_at || ''}</td>`;
        if (columnSettings.updated_at) html += `<td>${item.updated_at || ''}</td>`;
        if (columnSettings.remark) html += `<td>${item.remark || ''}</td>`;
        
        // 操作按钮
        let actionHtml = `<td>
            <div class="btn-group btn-group-sm">
                <button class="btn btn-outline-primary" onclick="editShop(${item.id})" title="编辑">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-outline-danger" onclick="deleteShop(${item.id})" title="删除">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        </td>`;
        
        html += actionHtml;
        tr.innerHTML = html;
        tbody.appendChild(tr);
    });
}

// ==================== 搜索关键词高亮 ====================
function highlightKeyword(text, keyword) {
    if (!keyword || !text) return text;
    const regex = new RegExp(`(${keyword})`, 'gi');
    return text.replace(regex, '<mark class="bg-warning">$1</mark>');
}

// ==================== 渲染分页 ====================
function renderPagination(total, page) {
    const limit = 12;
    const totalPages = Math.ceil(total / limit);
    const pagination = document.getElementById('pagination');
    
    if (totalPages <= 1) {
        pagination.innerHTML = '';
        return;
    }
    
    pagination.innerHTML = '';
    
    // 上一页
    if (page > 1) {
        pagination.innerHTML += `<li class="page-item"><a class="page-link" href="javascript:loadData(${page - 1})">上一页</a></li>`;
    } else {
        pagination.innerHTML += `<li class="page-item disabled"><span class="page-link">上一页</span></li>`;
    }
    
    // 页码
    for (let i = 1; i <= totalPages; i++) {
        if (i === page) {
            pagination.innerHTML += `<li class="page-item active"><span class="page-link">${i}</span></li>`;
        } else {
            pagination.innerHTML += `<li class="page-item"><a class="page-link" href="javascript:loadData(${i})">${i}</a></li>`;
        }
    }
    
    // 下一页
    if (page < totalPages) {
        pagination.innerHTML += `<li class="page-item"><a class="page-link" href="javascript:loadData(${page + 1})">下一页</a></li>`;
    } else {
        pagination.innerHTML += `<li class="page-item disabled"><span class="page-link">下一页</span></li>`;
    }
}

// ==================== 列设置 ====================
var defaultColumnSettings = {
    id: true,
    shop_name: true,
    phone: true,
    address: true,
    order_count: true,
    total_amount: true,
    last_order_time: true,
    created_at: true,
    updated_at: true,
    remark: true
};

function getColumnSettings() {
    const saved = localStorage.getItem('shopListColumns');
    return saved ? JSON.parse(saved) : {...defaultColumnSettings};
}

function saveColumnSettings(settings) {
    localStorage.setItem('shopListColumns', JSON.stringify(settings));
}

function applyColumnSettings(settings) {
    document.querySelectorAll('#tableBody tr').forEach(tr => {
        const cells = tr.querySelectorAll('td');
        const keys = Object.keys(settings);
        cells.forEach((cell, index) => {
            if (index < keys.length) {
                cell.style.display = settings[keys[index]] ? '' : 'none';
            }
        });
    });
    
    // 表头
    document.querySelectorAll('#tableHead th').forEach((th, index) => {
        const col = th.dataset.col;
        th.style.display = settings[col] !== false ? '' : 'none';
    });
}

function resetColumnSettings() {
    localStorage.removeItem('shopListColumns');
    const settings = {...defaultColumnSettings};
    updateColumnCheckboxes(settings);
    applyColumnSettings(settings);
}

function updateColumnCheckboxes(settings) {
    document.querySelectorAll('.column-toggle').forEach(cb => {
        const col = cb.id.replace('col_', '');
        cb.checked = settings[col] !== false;
    });
}

function initColumnSettings() {
    const settings = getColumnSettings();
    updateColumnCheckboxes(settings);
    applyColumnSettings(settings);
    
    document.querySelectorAll('.column-toggle').forEach(cb => {
        cb.addEventListener('change', function() {
            const settings = getColumnSettings();
            const col = this.id.replace('col_', '');
            settings[col] = this.checked;
            saveColumnSettings(settings);
        });
    });
}

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    initColumnSettings();
    initBusinessModelColors();
});

// ==================== 加载骨架屏 ====================
function showLoadingSkeleton() {
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = `
        <tr>
            <td colspan="11">
                <div class="skeleton-table">
                    <div class="skeleton skeleton-text" style="width: 30%"></div>
                    <div class="skeleton skeleton-text" style="width: 60%"></div>
                    <div class="skeleton skeleton-text" style="width: 45%"></div>
                </div>
            </td>
        </tr>
    `;
}

// ==================== 颜色辅助 ====================
function getColorBg(colorName) {
    const colors = {
        'bg-purple': 'rgba(155, 89, 182, 0.1)',
        'bg-orange': 'rgba(230, 126, 34, 0.1)',
        'bg-cyan': 'rgba(23, 162, 184, 0.1)',
        'bg-green': 'rgba(40, 167, 69, 0.1)',
        'bg-red': 'rgba(220, 53, 69, 0.1)',
        'bg-blue': 'rgba(0, 123, 255, 0.1)'
    };
    return colors[colorName] || null;
}

// ==================== 经营模式按钮颜色 ====================
function initBusinessModelColors() {
    businessModelColors = {
        '批发': 'bg-purple',
        '零售': 'bg-orange',
        '电商': 'bg-cyan'
    };
}

// ==================== 导出函数到全局 ====================
window.loadData = loadData;
window.highlightKeyword = highlightKeyword;
window.renderPagination = renderPagination;
window.getColumnSettings = getColumnSettings;
window.saveColumnSettings = saveColumnSettings;
window.applyColumnSettings = applyColumnSettings;
window.resetColumnSettings = resetColumnSettings;
window.updateColumnCheckboxes = updateColumnCheckboxes;
window.initColumnSettings = initColumnSettings;
window.showLoadingSkeleton = showLoadingSkeleton;
window.showToast = showToast;
