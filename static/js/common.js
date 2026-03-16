/**
 * 客户管理系统 - 公共工具函数
 * 包含分页、表格、弹窗等通用功能
 */

// 全局配置
const DEFAULT_PAGE_SIZE = 12;
const MAX_PAGE_SIZE = 100;

/**
 * 获取分页参数
 */
function getPaginationParams() {
    return {
        page: parseInt(document.getElementById('currentPage')?.textContent) || 1,
        limit: DEFAULT_PAGE_SIZE
    };
}

/**
 * 生成分页 HTML
 * @param {number} total - 总记录数
 * @param {number} currentPage - 当前页码
 * @param {number} pageSize - 每页数量
 * @param {function} onPageChange - 页码变更回调
 */
function renderPaginationHTML(total, currentPage, pageSize, onPageChange = null) {
    const totalPages = Math.ceil(total / pageSize);
    if (totalPages <= 1) {
        return '';
    }

    let html = '';
    
    // 上一页
    if (currentPage > 1) {
        html += `<li class="page-item"><a class="page-link" href="javascript:void(0)" onclick="goToPage(${currentPage - 1})">上一页</a></li>`;
    } else {
        html += `<li class="page-item disabled"><span class="page-link">上一页</span></li>`;
    }
    
    // 页码
    const maxPages = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxPages / 2));
    let endPage = Math.min(totalPages, startPage + maxPages - 1);
    
    if (endPage - startPage < maxPages - 1) {
        startPage = Math.max(1, endPage - maxPages + 1);
    }
    
    if (startPage > 1) {
        html += `<li class="page-item"><a class="page-link" href="javascript:void(0)" onclick="goToPage(1)">1</a></li>`;
        if (startPage > 2) {
            html += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
        }
    }
    
    for (let i = startPage; i <= endPage; i++) {
        if (i === currentPage) {
            html += `<li class="page-item active"><span class="page-link">${i}</span></li>`;
        } else {
            html += `<li class="page-item"><a class="page-link" href="javascript:void(0)" onclick="goToPage(${i})">${i}</a></li>`;
        }
    }
    
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            html += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
        }
        html += `<li class="page-item"><a class="page-link" href="javascript:void(0)" onclick="goToPage(${totalPages})">${totalPages}</a></li>`;
    }
    
    // 下一页
    if (currentPage < totalPages) {
        html += `<li class="page-item"><a class="page-link" href="javascript:void(0)" onclick="goToPage(${currentPage + 1})">下一页</a></li>`;
    } else {
        html += `<li class="page-item disabled"><span class="page-link">下一页</span></li>`;
    }
    
    return html;
}

/**
 * 生成分页组件（带回调）
 */
function createPagination(total, page, limit, callback) {
    const container = document.getElementById('pagination');
    if (!container) return;
    
    container.innerHTML = renderPaginationHTML(total, page, limit, callback);
}

/**
 * 空状态 HTML
 */
function renderEmptyState(message = '暂无数据') {
    return `<tr><td colspan="100" class="text-center text-muted py-5"><i class="bi bi-inbox" style="font-size: 2rem;"></i><p class="mt-2">${message}</p></td></tr>`;
}

/**
 * 加载骨架屏
 */
function renderLoading() {
    return `<tr><td colspan="100" class="text-center text-muted py-4"><div class="spinner-border spinner-border-sm me-2"></div>加载中...</td></tr>`;
}

/**
 * 通用列表加载函数
 * @param {string} url - API URL
 * @param {object} params - 查询参数
 * @param {function} renderFn - 渲染回调
 * @param {function} completeFn - 完成回调
 */
function loadListData(url, params, renderFn, completeFn) {
    const queryString = new URLSearchParams(params).toString();
    
    fetch(`${url}?${queryString}`)
        .then(res => res.json())
        .then(data => {
            if (data.code === 0) {
                renderFn(data);
            } else {
                Swal.fire({
                    icon: 'error',
                    title: '加载失败',
                    text: data.msg || '未知错误'
                });
            }
        })
        .catch(err => {
            console.error('加载数据失败:', err);
            Swal.fire({
                icon: 'error',
                title: '加载失败',
                text: '网络错误，请稍后重试'
            });
        })
        .finally(() => {
            if (completeFn) completeFn();
        });
}

/**
 * 通用删除确认
 */
function confirmDelete(title = '确定要删除吗？', text = '此操作不可恢复') {
    return Swal.fire({
        icon: 'warning',
        title: title,
        text: text,
        showCancelButton: true,
        confirmButtonText: '确定',
        cancelButtonText: '取消'
    });
}

/**
 * 通用保存数据
 */
function saveData(url, data, successMsg = '保存成功') {
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => {
        if (data.code === 0) {
            Swal.fire({
                icon: 'success',
                title: '成功',
                text: successMsg,
                timer: 1500,
                showConfirmButton: false
            });
            return data;
        } else {
            Swal.fire({
                icon: 'error',
                title: '失败',
                text: data.msg
            });
            throw new Error(data.msg);
        }
    });
}

/**
 * 关闭弹窗
 */
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        const bsModal = bootstrap.Modal.getInstance(modal);
        if (bsModal) {
            bsModal.hide();
        }
    }
}

/**
 * 打开弹窗
 */
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    }
}

/**
 * 重置表单
 */
function resetForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
    }
}

/**
 * 获取表单数据
 */
function getFormData(formId) {
    const form = document.getElementById(formId);
    if (!form) return {};
    
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    return data;
}

/**
 * Debounce 函数
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * 节流函数
 */
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * 主题切换功能
 */
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    
    // 更新按钮状态
    const lightBtn = document.getElementById('themeLight');
    const darkBtn = document.getElementById('themeDark');
    if (lightBtn && darkBtn) {
        lightBtn.classList.toggle('active', theme === 'light');
        darkBtn.classList.toggle('active', theme === 'dark');
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    setTheme(currentTheme === 'light' ? 'dark' : 'light');
}

// 初始化主题
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
});

// 导出到全局
window.renderPaginationHTML = renderPaginationHTML;
window.createPagination = createPagination;
window.renderEmptyState = renderEmptyState;
window.renderLoading = renderLoading;
window.loadListData = loadListData;
window.confirmDelete = confirmDelete;
window.saveData = saveData;
window.closeModal = closeModal;
window.openModal = openModal;
window.resetForm = resetForm;
window.getFormData = getFormData;
window.debounce = debounce;
window.throttle = throttle;
window.setTheme = setTheme;
window.toggleTheme = toggleTheme;
