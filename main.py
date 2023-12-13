import os
import json
import requests

pushplus_token = os.environ.get('pushplus_token')
token = os.environ.get('token')

# 公共请求头
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Linux; Android 11; M2007J3SC Build/SKQ1.220213.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3224 MMWEBSDK/20210902 Mobile Safari/537.36 MMWEBID/6170 MicroMessenger/8.0.15.2020(0x28000F30) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
    "token": token,
}

# 请求青年大学习信息
def get_info():
    info_url = "https://dxx.scyol.com/api/stages/currentInfo"
    info_response = requests.post(info_url, headers=headers)
    info_data = info_response.json()
    return info_data

# 提交学习记录
def commit_study_record(info_data):
    orgName = info_data.get("data", {}).get("studentVO", {}).get("orgName")
    org = info_data.get("data", {}).get("studentVO", {}).get("org")
    allOrgName = info_data.get("data", {}).get("studentVO", {}).get("allOrgName")
    name = info_data.get("data", {}).get("studentVO", {}).get("name")
    lastOrg = info_data.get("data", {}).get("studentVO", {}).get("lastOrg")
    tel = info_data.get("data", {}).get("studentVO", {}).get("tel")

    study_payload = {
        "orgName": orgName,
        "org": org,
        "allOrgName": allOrgName,
        "name": name,
        "lastOrg": lastOrg,
        "tel": tel
    }

    study_url = "https://dxx.scyol.com/api/student/commit"
    study_response = requests.post(study_url, headers=headers, json=study_payload)
    study_data = study_response.json()
    return study_data


# 发送推送通知
def send_notification(title, content):
    if not pushplus_token:
        print("未填写推送令牌，请填写有效的推送令牌")
        return

    pushplus_url = "https://www.pushplus.plus/send"
    pushplus_payload = {
        "token": pushplus_token,
        "title": title,
        "content": content
    }

    try:
        requests.post(pushplus_url, data=pushplus_payload)
        print("推送通知发送成功")
    except Exception as e:
        print(f"推送请求出错：{e}")


# 获取截图URL
def get_screenshot_url(video_url):
    return video_url.replace('m.html', 'images/end.jpg')

# 获取推送通知内容
def get_notification_content(info_data, snum, name, orgName, video_url):
    image_url = get_screenshot_url(video_url)
    content = f"{snum}青年大学习已完成\n{name} {orgName}\n<a href='{video_url}' />点击观看青年大学习视频</a><br/><img src='{image_url}' />"
    return content

# 主函数
def main():
    info_data = get_info()

    if info_data.get("code") == 403:
        print("用户token无效或已过期，请重新填写")
        send_notification("青年大学习", "用户token无效或已过期，请重新填写")
        return

    snum = info_data.get("data", {}).get("currentStages", {}).get("snum")
    name = info_data.get("data", {}).get("studentVO", {}).get("name")
    orgName = info_data.get("data", {}).get("studentVO", {}).get("orgName")
    video_url = info_data.get("data", {}).get("currentStages", {}).get("url")

    study_data = commit_study_record(info_data)
    study_msg = study_data.get("msg")
    if study_data.get("code") not in [200, 2]:
        print("学习记录提交失败，" + study_msg)
        send_notification("青年大学习", f"学习记录提交失败，{study_msg}")
        return

    content = get_notification_content(info_data, snum, name, orgName, video_url)
    send_notification("青年大学习", content)

    print("学习记录提交成功")


if __name__ == "__main__":
    main()
