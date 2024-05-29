# -*- coding: utf-8 -*-
import requests
import socket
from sys import exit

# 目标URL，感谢IPDB项目
url = 'https://ipdb.api.030101.xyz/?type=bestproxy'

# Telegram 机器人 API 配置
telegram_api_token = 'your_api_token'
telegram_chat_id = 'your_chat_id'  # 用你的Chat ID，不是机器人的Chat ID

# Cloudflare 信息
api_key = "your_api_key"
email = "your_email"
zone_id = "your_zone_id"
domain = "your_domain"  # 确保这是完整的域名（如cf.111111.xyz）
ports = [80,443]  # 添加端口变量，如 ports = [80,443] 代表80和443都通

# 添加请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://google.com',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}

def check_ports(ip, ports):
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)  # 设置超时时间
        result = sock.connect_ex((ip, port))
        sock.close()
        if result != 0:
            return False
    return True

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

# 获取IP地址并检查端口
try:
    response = requests.get(url)
    response.raise_for_status()
    ip_addresses = response.text.split('\n')
except requests.exceptions.RequestException as e:
    print(f"HTTP请求失败: {e}")
    exit()

# 检查所有IP+端口的可达性
valid_ips = []
for ip in ip_addresses:
    if check_ports(ip, ports):
        print(f"在 {ip} 上所有端口都可访问")
        valid_ips.append(ip)
    else:
        print(f"在 {ip} 上某些端口不可访问")

# 如果没有可用的IP，退出程序
if not valid_ips:
    print("没有可用的IP，退出程序")
    exit()

# 删除旧的子域名A记录
deleted_count = 0
delete_old_a_records()

# 为每个可用的IP添加A记录
for ip in valid_ips:
    add_a_record(ip)

# 输出总共找到的IP地址数量
total_ips = len(valid_ips)
print("Total IP Addresses Found:", total_ips)

# 发送Telegram提醒消息
message = f"{domain} 优选成功，共添加 {total_ips} 个IP，删除 {deleted_count} 个IP。"
send_telegram_message(message)
