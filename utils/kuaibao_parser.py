# 智能地址解析工具
import http.client
import urllib.parse
import hashlib
import time
import json
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context

# 快宝API配置
KUAIBAO_APP_ID = os.environ.get('KUAIBAO_APP_ID', '105511')
KUAIBAO_APP_KEY = os.environ.get('KUAIBAO_APP_KEY', '8e42e7b5d1c9ba99923e4aa7fb5f1c2416e779f8')
KUAIBAO_METHOD = 'cloud.address.cleanse'

def determine_region(province):
    """根据省份确定大区"""
    regions = {
        "华北": ["北京市", "天津市", "河北省", "山西省", "内蒙古自治区"],
        "华中": ["河南省", "湖北省", "湖南省"],
        "华南": ["广东省", "广西壮族自治区", "海南省"],
        "华东": ["上海市", "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省"],
        "西北": ["陕西省", "甘肃省", "青海省", "宁夏回族自治区", "新疆维吾尔自治区"],
        "西南": ["重庆市", "四川省", "贵州省", "云南省", "西藏自治区"],
        "东北": ["辽宁省", "吉林省", "黑龙江省"]
    }
    for region, provinces in regions.items():
        if province in provinces:
            return region
    return "未知区域"


def clear_address(addinfo, app_id=None, app_key=None):
    """调用快宝API解析地址"""
    if not addinfo:
        return {'error': '请输入地址'}
    
    _app_id = app_id or KUAIBAO_APP_ID
    _app_key = app_key or KUAIBAO_APP_KEY
    
    ts = int(time.time())
    signStr = _app_id + KUAIBAO_METHOD + str(ts) + _app_key
    sign = hashlib.md5(signStr.encode('utf8')).hexdigest()
    data = '{"multimode":true,"address":"' + addinfo + '","cleanTown":true}'
    
    payload_list = {
        'app_id': _app_id,
        'method': KUAIBAO_METHOD,
        'ts': str(ts),
        'sign': sign,
        'data': data
    }
    payload = urllib.parse.urlencode(payload_list)
    headers = {'content-type': "application/x-www-form-urlencoded"}
    
    conn = http.client.HTTPSConnection("kop.kuaidihelp.com")
    conn.request("POST", "/api", payload, headers)
    res = conn.getresponse()
    result = res.read().decode("utf-8")
    conn.close()
    
    data_json = json.loads(result)
    
    if data_json['code'] == 0:
        if len(data_json['data']) == 1:
            addr_data = data_json['data'][0]
            if addr_data['province'] == '':
                return {'error': '未获取到信息'}
            
            bigqu = determine_region(addr_data['province'])
            return {
                'region': bigqu,
                'province': addr_data['province'],
                'city': addr_data['city'],
                'district': addr_data['county'],
                'town': addr_data.get('town', ''),
                'detail': addr_data['address']
            }
        else:
            return {'error': f'只能解析一个地址，当前解析了{len(data_json["data"])}个'}
    else:
        return {'error': f'错误代码：{data_json["code"]}，错误信息：{data_json["msg"]}'}


# 如果直接运行则测试
if __name__ == '__main__':
    test_addresses = ["深圳市南山区科技园", "广东省深圳市南山区科技园南路88号", "杭州市西湖区"]
    for addr in test_addresses:
        print(f"地址: {addr}")
        print(f"结果: {clear_address(addr)}")
        print("-" * 50)
