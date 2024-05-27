# -*- coding: utf-8 -*-
import requests

# 目标URL，感谢IPDB项目
url = 'https://ipdb.api.030101.xyz/?type=bestproxy'



# 添加请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://google.com',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}

# 网页上只有IP可以通过这种方式获取IP
try:
    # 发起请求获取网页内容
    response = requests.get(url)
    response.raise_for_status()  # 如果响应状态码不是200，抛出HTTPError
    ip_addresses = response.text.split('\n')  # 将每行的IP地址分割为一个列表
except requests.exceptions.RequestException as e:
    print(f"HTTP请求失败: {e}")
    exit()  # 请求失败时，退出程序

# 删除旧的 A 记录并统计删除的数量
deleted_count = 0

def delete_old_a_records():
    global deleted_count
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=A&name={domain}"

    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data["success"]:
            for record in data["result"]:
                delete_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record['id']}"
                delete_response = requests.delete(delete_url, headers=headers)
                delete_response.raise_for_status()
                print(f"成功删除A记录: {record['name']} -> {record['content']}")
                deleted_count += 1
        else:
            print(f"获取A记录失败: {data['errors']}")
    except requests.exceptions.RequestException as e:
        print(f"HTTP请求失败: {e}")


# 增加新的 A 记录
def add_a_record(ip):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }

    record = {
        "type": "A",
        "name": domain,
        "content": ip,
        "ttl": 1,  # 使用'1'表示自动TTL
        "proxied": False
    }

    try:
        response = requests.post(url, headers=headers, json=record)
        response.raise_for_status()
        data = response.json()
        if data["success"]:
            print(f"成功添加A记录: {ip}")
        else:
            print(f"无法添加A记录: {ip}")
            print(f"错误消息: {data['errors']}")
    except requests.exceptions.RequestException as e:
        print(f"HTTP请求失败: {e}")


# 发送 Telegram 消息
def send_telegram_message(text):
    telegram_url = f"https://api.telegram.org/bot{telegram_api_token}/sendMessage"
    payload = {
        "chat_id": telegram_chat_id,
        "text": text
    }
    try:
        response = requests.post(telegram_url, json=payload)
        response.raise_for_status()
        print(f"成功发送Telegram消息: {text}")
    except requests.exceptions.RequestException as e:
        print(f"Telegram消息发送失败: {e}")


# 删除旧的子域名A记录
delete_old_a_records()

# 输出所有移动的IP地址并为每个IP添加A记录
for ip in ip_addresses:
    print(ip)
    add_a_record(ip)

# 输出总共找到的IP地址数量
total_ips = len(ip_addresses)
print("Total IP Addresses Found:", total_ips)

# 发送Telegram提醒消息
message = f"{domain} 优选成功，共添加 {total_ips} 个IP，删除 {deleted_count} 个IP。"
send_telegram_message(message)