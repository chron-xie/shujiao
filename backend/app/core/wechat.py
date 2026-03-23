import httpx
from typing import Optional, Dict
from app.core.config import settings


class WeChatAPI:
    """微信小程序API"""

    BASE_URL = "https://api.weixin.qq.com"

    @staticmethod
    async def code2session(code: str) -> Dict:
        """
        通过code获取微信用户信息
        https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/login/auth.code2Session.html

        Args:
            code: wx.login()返回的code

        Returns:
            {
                "openid": "用户唯一标识",
                "session_key": "会话密钥",
                "unionid": "用户在开放平台的唯一标识（可选）"
            }
        """
        url = f"{WeChatAPI.BASE_URL}/sns/jscode2session"
        params = {
            "appid": settings.WECHAT_APP_ID,
            "secret": settings.WECHAT_APP_SECRET,
            "js_code": code,
            "grant_type": "authorization_code",
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()

            if "errcode" in data and data["errcode"] != 0:
                raise Exception(f"微信登录失败: {data.get('errmsg', '未知错误')}")

            return data

    @staticmethod
    async def get_access_token() -> str:
        """
        获取access_token（用于调用其他微信API）
        https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/access-token/auth.getAccessToken.html
        """
        url = f"{WeChatAPI.BASE_URL}/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": settings.WECHAT_APP_ID,
            "secret": settings.WECHAT_APP_SECRET,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()

            if "errcode" in data and data["errcode"] != 0:
                raise Exception(f"获取access_token失败: {data.get('errmsg', '未知错误')}")

            return data["access_token"]


class WeChatPay:
    """微信支付API"""

    BASE_URL = "https://api.mch.weixin.qq.com"

    @staticmethod
    async def unified_order(
        out_trade_no: str,
        total_fee: int,
        body: str,
        openid: str,
        notify_url: str
    ) -> Dict:
        """
        统一下单接口
        https://pay.weixin.qq.com/wiki/doc/api/wxa/wxa_api.php?chapter=9_1

        Args:
            out_trade_no: 商户订单号
            total_fee: 订单金额（单位：分）
            body: 商品描述
            openid: 用户openid
            notify_url: 支付回调URL

        Returns:
            {
                "prepay_id": "预支付交易会话标识",
                ...
            }
        """
        # TODO: 实现微信支付统一下单逻辑
        # 1. 构建XML参数
        # 2. 生成签名
        # 3. 发起POST请求
        # 4. 解析XML响应
        # 5. 返回prepay_id等参数

        raise NotImplementedError("微信支付功能待实现")

    @staticmethod
    def generate_payment_params(prepay_id: str) -> Dict:
        """
        生成小程序支付参数
        用于前端调用 wx.requestPayment()

        Args:
            prepay_id: 统一下单返回的prepay_id

        Returns:
            {
                "timeStamp": "时间戳",
                "nonceStr": "随机字符串",
                "package": "prepay_id=xxx",
                "signType": "RSA",
                "paySign": "签名"
            }
        """
        # TODO: 实现支付参数生成逻辑
        raise NotImplementedError("微信支付功能待实现")

    @staticmethod
    def verify_notify(xml_data: str) -> Dict:
        """
        验证支付回调签名并解析数据

        Args:
            xml_data: 微信支付回调的XML数据

        Returns:
            解析后的支付结果
        """
        # TODO: 实现支付回调验证逻辑
        raise NotImplementedError("微信支付功能待实现")
