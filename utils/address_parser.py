# 地址解析工具 - 智能补全地址解析
import re
from pypinyin import lazy_pinyin, Style

# 大区映射
REGION_MAP = {
    '华东': ['上海', '江苏', '浙江', '安徽', '福建', '江西', '山东'],
    '华南': ['广东', '广西', '海南'],
    '华北': ['北京', '天津', '河北', '山西', '内蒙古'],
    '华中': ['河南', '湖北', '湖南'],
    '西南': ['重庆', '四川', '贵州', '云南', '西藏'],
    '西北': ['陕西', '甘肃', '青海', '宁夏', '新疆'],
    '东北': ['辽宁', '吉林', '黑龙江'],
}

# 省份 -> 大区
PROVINCE_TO_REGION = {prov: region for region, provinces in REGION_MAP.items() for prov in provinces}

# 常用城市映射（城市名 -> 省份）
CITY_TO_PROVINCE = {
    '广州市': '广东省', '深圳市': '广东省', '东莞市': '广东省', '佛山市': '广东省',
    '珠海市': '广东省', '中山市': '广东省', '惠州市': '广东省', '江门市': '广东省',
    '湛江市': '广东省', '茂名市': '广东省', '肇庆市': '广东省', '梅州市': '广东省',
    '汕尾市': '广东省', '河源市': '广东省', '阳江市': '广东省', '清远市': '广东省',
    '韶关市': '广东省', '揭阳市': '广东省', '潮州市': '广东省', '云浮市': '广东省',
    '杭州市': '浙江省', '宁波市': '浙江省', '温州市': '浙江省', '嘉兴市': '浙江省',
    '湖州市': '浙江省', '绍兴市': '浙江省', '金华市': '浙江省', '衢州市': '浙江省',
    '舟山市': '浙江省', '台州市': '浙江省', '丽水市': '浙江省',
    '南京市': '江苏省', '苏州市': '江苏省', '无锡市': '江苏省', '常州市': '江苏省',
    '镇江市': '江苏省', '扬州市': '江苏省', '泰州市': '江苏省', '南通市': '江苏省',
    '盐城市': '江苏省', '淮安市': '江苏省', '连云港市': '江苏省', '徐州市': '江苏省',
    '宿迁市': '江苏省',
    '成都市': '四川省', '绵阳市': '四川省', '德阳市': '四川省', '宜宾市': '四川省',
    '泸州市': '四川省', '南充市': '四川省', '达州市': '四川省', '乐山市': '四川省',
    '北京市': '北京市', '上海市': '上海市', '天津市': '天津市', '重庆市': '重庆市',
    '武汉市': '湖北省', '长沙市': '湖南省', '郑州市': '河南省', '合肥市': '安徽省',
    '西安市': '陕西省', '济南市': '山东省', '青岛市': '山东省', '沈阳市': '辽宁省',
    '大连市': '辽宁省', '长春市': '吉林省', '哈尔滨市': '黑龙江省', '南昌市': '江西省',
    '厦门市': '福建省', '福州市': '福建省', '昆明市': '云南省', '贵阳市': '贵州省',
    '兰州市': '甘肃省', '乌鲁木齐市': '新疆维吾尔自治区', '呼和浩特市': '内蒙古自治区',
    '南宁市': '广西壮族自治区', '海口市': '海南省', '太原市': '山西省', '石家庄市': '河北省',
}

# 常用区/县映射（区名 -> 城市）
DISTRICT_TO_CITY = {
    '天河区': '广州市', '越秀区': '广州市', '海珠区': '广州市', '荔湾区': '广州市',
    '白云区': '广州市', '黄埔区': '广州市', '番禺区': '广州市', '花都区': '广州市',
    '南沙区': '广州市', '增城区': '广州市', '从化区': '广州市',
    '南山区': '深圳市', '福田区': '深圳市', '罗湖区': '深圳市', '宝安区': '深圳市',
    '龙岗区': '深圳市', '盐田区': '深圳市', '龙华区': '深圳市', '坪山区': '深圳市',
    '西湖区': '杭州市', '拱墅区': '杭州市', '上城区': '杭州市', '滨江区': '杭州市',
    '萧山区': '杭州市', '余杭区': '杭州市', '富阳区': '杭州市', '临安区': '杭州市',
    '朝阳区': '北京市', '海淀区': '北京市', '东城区': '北京市', '西城区': '北京市',
    '丰台区': '北京市', '石景山区': '北京市', '通州区': '北京市', '顺义区': '北京市',
    '昌平区': '北京市', '大兴区': '北京市', '房山区': '北京市', '门头沟区': '北京市',
    '怀柔区': '北京市', '平谷区': '北京市', '密云区': '北京市', '延庆区': '北京市',
    '浦东新区': '上海市', '黄浦区': '上海市', '徐汇区': '上海市', '长宁区': '上海市',
    '静安区': '上海市', '普陀区': '上海市', '虹口区': '上海市', '杨浦区': '上海市',
    '闵行区': '上海市', '宝山区': '上海市', '嘉定区': '上海市', '金山区': '上海市',
    '松江区': '上海市', '青浦区': '上海市', '奉贤区': '上海市', '崇明区': '上海市',
}

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

def parse_address(full_address):
    """解析地址，自动补全大区、省份、市、区、详细地址"""
    if not full_address:
        return {}
    
    result = {
        'region': '',
        'province': '',
        'city': '',
        'district': '',
        'address': full_address,
        'address_pinyin': '',
        'address_initial': ''
    }
    
    address = full_address.strip()
    
    # 去除常见前缀
    address = re.sub(r'^(中国|中华人民共和国|全国|收货地址|发货地址|地址：|地址:)', '', address)
    address = address.strip()
    
    # ============ 第一步：提取省份 ============
    province = ''
    # 检查直辖市
    for city in ['北京', '上海', '天津', '重庆']:
        if address.startswith(city):
            province = city + '市'
            address = address[len(city):]
            break
    
    # 检查自治区
    if not province:
        for region in ['内蒙古', '广西', '西藏', '宁夏', '新疆']:
            if address.startswith(region):
                province = region + '自治区'
                address = address[len(region):]
                break
    
    # 检查省份（包含简称）
    if not province:
        # 省份全称
        provinces = ['广东省', '浙江省', '江苏省', '山东省', '河南省', '湖北省', '湖南省', 
                    '四川省', '贵州省', '云南省', '陕西省', '甘肃省', '青海省', '安徽省',
                    '福建省', '江西省', '河北省', '山西省', '辽宁省', '吉林省', '黑龙江省',
                    '海南省', '台湾省', '香港特别行政区', '澳门特别行政区']
        for prov in provinces:
            if address.startswith(prov):
                province = prov
                address = address[len(prov):]
                break
        
        # 省份简称
        if not province:
            alias_map = {'粤': '广东省', '浙': '浙江省', '苏': '江苏省', '鲁': '山东省',
                        '豫': '河南省', '鄂': '湖北省', '湘': '湖南省', '川': '四川省',
                        '贵': '贵州省', '滇': '云南省', '陕': '陕西省', '甘': '甘肃省',
                        '青': '青海省', '皖': '安徽省', '闽': '福建省', '赣': '江西省',
                        '冀': '河北省', '晋': '山西省', '辽': '辽宁省', '吉': '吉林省',
                        '黑': '黑龙江省', '琼': '海南省', '京': '北京市', '沪': '上海市',
                        '津': '天津市', '渝': '重庆市', '桂': '广西壮族自治区', '蒙': '内蒙古自治区'}
            for alias, full in alias_map.items():
                if address.startswith(alias):
                    province = full
                    address = address[1:]
                    break
    
    # 如果识别到省份，设置大区
    if province:
        prov_short = province.replace('省', '').replace('市', '').replace('自治区', '').replace('特别行政区', '')
        if prov_short in PROVINCE_TO_REGION:
            result['province'] = province
            result['region'] = PROVINCE_TO_REGION[prov_short]
    
    # ============ 第二步：提取城市 ============
    city = ''
    if result['province']:
        # 在剩余地址中查找城市
        for c in CITY_TO_PROVINCE:
            if c in address[:10]:  # 城市名通常在地址前面
                city = c
                address = address.replace(c, '', 1)
                break
    else:
        # 没有省份，根据城市反推省份
        for c, p in CITY_TO_PROVINCE.items():
            if c in address[:10]:
                city = c
                province = p
                prov_short = province.replace('省', '').replace('市', '')
                result['province'] = province
                result['region'] = PROVINCE_TO_REGION.get(prov_short, '')
                address = address.replace(c, '', 1)
                break
    
    # ============ 第三步：提取区/县 ============
    district = ''
    if city:
        # 在剩余地址中查找区
        for d in DISTRICT_TO_CITY:
            if d in address[:15]:
                district = d
                address = address.replace(d, '', 1)
                break
    
    if not district:
        # 通用区/县匹配
        match = re.match(r'^(.+?(?:区|县|旗|市|特区|新区|工业园区|高新技术区))', address)
        if match:
            district = match.group(1)
            address = address[len(district):]
    
    # 清理地址
    address = re.sub(r'^[,\-\s\-—]+', '', address).strip()
    
    # ============ 第四步：补全信息 ============
    # 1. 如果有省份没城市，尝试从区反推
    if result['province'] and not city and district:
        for d, c in DISTRICT_TO_CITY.items():
            if d == district:
                city = c
                break
    
    # 2. 如果有城市没省份，从城市反推
    if city and not result['province']:
        if city in CITY_TO_PROVINCE:
            result['province'] = CITY_TO_PROVINCE[city]
            prov_short = result['province'].replace('省', '').replace('市', '')
            result['region'] = PROVINCE_TO_REGION.get(prov_short, '')
    
    # 3. 补全大区（如果有省份的话）
    if result['province'] and not result['region']:
        prov_short = result['province'].replace('省', '').replace('市', '').replace('自治区', '')
        result['region'] = PROVINCE_TO_REGION.get(prov_short, '')
    
    # 4. 详细地址 = 剩余地址，如果没有识别出任何信息，则用原始地址
    if address:
        result['address'] = address
    elif district:
        result['address'] = district
    elif city:
        result['address'] = city
    
    # 5. 如果某个字段为空，用上一级填充
    if not result['province'] and city:
        result['province'] = city.replace('市', '') + '省'
    if not city and district:
        city = district.replace('区', '').replace('县', '') + '市'
        result['city'] = city
    
    # 6. 最终检查：如果区为空，用详细地址填充
    if not district and result['address']:
        # 尝试从详细地址提取区
        match = re.match(r'^(.+?(?:区|县))', result['address'])
        if match:
            result['district'] = match.group(1)
    
    # 7. 如果详细地址为空，用区填充
    if not result['address'] and district:
        result['address'] = district
    
    # 8. 特殊处理：直辖市
    if result['province'] in ['北京市', '上海市', '天津市', '重庆市']:
        if not result['city']:
            result['city'] = result['province'].replace('市', '')
        if not result['region']:
            result['region'] = '华北'
    
    # ============ 第五步：生成拼音 ============
    # 拼接完整地址（无空格）
    full_addr = (result['region'] or '') + (result['province'] or '') + (result['city'] or '') + (result['district'] or '') + (result['address'] or '')
    result['address_pinyin'] = get_pinyin(full_addr)
    result['address_initial'] = get_pinyin_initial(full_addr)
    
    return result
