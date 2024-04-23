import hashlib
import time
from urllib.parse import parse_qs, urlencode, urlparse

from django.conf import settings

# 星球参数
app_id = settings.XQ_APP_ID  # 星球应用ID
group_number = settings.XQ_GROUP_NUMBER  # 星球号
extra = settings.XQ_EXTRA  # 额外参数
redirect_url = settings.XQ_REDIRECT_URL  # 跳转地址
secret = settings.XQ_SECRET  # 密钥


def get_login_url():
    # 构造未签名的参数字典
    params = {
        "app_id": app_id,
        "group_number": group_number,
        "extra": extra,
        "redirect_url": redirect_url,  # 这里先不进行URL编码，params会自动处理
        "timestamp": int(time.time()),  # 时间戳
    }

    # 对query_string中的redirect_url进行URL编码
    query_string = urlencode(dict(sorted(params.items()))) + f"&secret={secret}"

    # 计算签名
    signature = hashlib.sha1(query_string.encode()).hexdigest()
    # 添加签名到请求参数中
    params["signature"] = signature

    # 拼接成URL参数
    params = urlencode(params)
    # 输出res重定向后的地址
    return f"https://wx.zsxq.com/connector/crm/identify_member.html?{params}"


# 验证
def verify_url_signature(url):
    # 解析URL
    parsed_url = urlparse(url)

    # 解析查询字符串中的参数
    query_params = parse_qs(parsed_url.query)
    query_params = {k: v[0] for k, v in query_params.items()}

    if "signature" not in query_params:return False

    # 提取并删除signature
    signature = query_params.pop("signature")
    # 重新拼接回去
    query_string = urlencode(query_params) + f"&secret={secret}"
    # 计算签名
    new_signature = hashlib.sha1(query_string.encode()).hexdigest()
    # 验证签名
    if new_signature == signature:
        if "signature" in query_params: query_params.pop("signature")
        if "app_id" in query_params: query_params.pop("app_id")
        if "timestamp" in query_params: query_params.pop("timestamp")
        return query_params
    else:
        return False
