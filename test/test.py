import requests

PHONE_NUMBER = "your_phone_number"
PASSWORD = "your_password"
PUSHPLUS_TOKEN = "your_pushplus_token"

USER_AGENT = "Mozilla/5.0 (Linux; Android 11; M2007J3SC Build/SKQ1.220213.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3224 MMWEBSDK/20210902 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.15.2020(0x28000F30) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64"

def login_and_get_token(phone_number, password):
    login_data = {
        "phoneNumber": phone_number,
        "password": password
    }
    login_headers = {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT
    }
    login_url = "https://tfqny.scyol.com/cloud/applet/api/phone/login"
    response = requests.post(login_url, headers=login_headers, json=login_data)

    if response.status_code == 200:
        login_data = response.json()
        token = login_data.get("data", {}).get("token")
        if token:
            return token
    return None

def get_authcode(token):
    authcode_url = "https://tfqny.scyol.com/cloud/applet/api/sign/getAuthorizationCode?moduleID=6"
    authcode_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": USER_AGENT,
        "Authorization": token,
    }
    authcode_response = requests.get(authcode_url, headers=authcode_headers)
    authcode_data = authcode_response.json()
    authcode = authcode_data.get("data", {})
    if authcode:
        return authcode
    return None

def get_last_signature():
    signature_url = "https://h5.cyol.com/special/weixin/sign.json"
    signature_response = requests.get(signature_url)
    signature_data = signature_response.json()
    signatures = [value.get('signature') for key, value in signature_data.items() if isinstance(value, dict)]
    return signatures[-1] if signatures else None

def v_prod(authcode, signature):
    v_prod_url = f"https://dxx.scyol.com/v_prod6.0.2/?code={signature}&state={authcode}"
    v_prod_response = requests.get(v_prod_url)
    v_prod_data = v_prod_response.text
    
    new_url = "https://dxx.scyol.com/api/wechat/share"
    payload = {"url":v_prod_url}
    new_url_response = requests.post(new_url,json=payload)
    new_url_data = new_url_response.json()
    return new_url_data.get("data",{}).get("jsapi_ticket",{})

def get_info(token):
    info_url = "https://dxx.scyol.com/api/stages/currentInfo"
    info_headers = {
    "Content-Type": "application/json",
    "User-Agent": USER_AGENT,
    "token": token,
    }
    info_response = requests.post(info_url, headers=info_headers)
    info_data = info_response.json()
    print("获取信息接口返回数据:", info_data)
    return info_data

def wx_auth(jsapi_ticket, authcode):
    wx_auth_url = f"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx7e7fdbc0cc711044&redirect_uri=https://dxx.scyol.com/v_prod6.0.2&response_type=code&scope=snsapi_userinfo&state={authcode}&md=true&uin=MTQ4NjkwNzM2Mg==&key={key}&version={version}&exportkey={exportkey}&pass_ticket={jsapi_ticket}==&wx_header=0"
    wx_auth_headers = {
        "User-Agent": USER_AGENT,
    }
    wx_auth_response = requests.get(wx_auth_url, headers=wx_auth_headers)
    wx_auth_data = wx_auth_response.text

    redirect_url = f"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx7e7fdbc0cc711044&redirect_uri=https://dxx.scyol.com/v_prod6.0.2/&response_type=code&scope=snsapi_userinfo&state={authcode}&connect_redirect=1"
    redirect_response = requests.get(redirect_url, headers=wx_auth_headers)
    redirect_data = redirect_response.text

def verify_auth_code_to_login(authcode, signature, token):
    verify_auth_code_to_login_url = f"https://dxx.scyol.com/api/cloudPlatformToDock/verifyAuthCodeToLogin?code={authcode}&wxCode={signature}"
    verify_auth_code_to_login_headers = {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
    }
    verify_auth_code_to_login_payload = {}
    verify_auth_code_to_login_response = requests.post(verify_auth_code_to_login_url, headers=verify_auth_code_to_login_headers, data=verify_auth_code_to_login_payload)
    verify_auth_code_to_login_data = verify_auth_code_to_login_response.json()
    new_token = verify_auth_code_to_login_data.get("data", {}).get("token", {})
    
    return new_token if new_token else None

def main():
    token = login_and_get_token(PHONE_NUMBER, PASSWORD)
    if not token:
        print("登录失败或无法获取token")
        return

    authcode = get_authcode(token)
    if not authcode:
        print("无法获取authcode")
        return

    signature = get_last_signature()
    if not signature:
        print("无法获取最后的签名")
        return

    jsapi_ticket = v_prod(authcode, signature)
    if not jsapi_ticket:
        print("无法获取jsapi_ticket")
        return

    info_data = get_info(token)

    wx_auth(jsapi_ticket, authcode)

    new_token = verify_auth_code_to_login(authcode, signature, token)
    if not new_token:
        print("无法验证或登录AuthCode")
        return

if __name__ == "__main__":
    main()
