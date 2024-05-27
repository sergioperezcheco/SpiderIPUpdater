# SpiderIPUpdater
一款优选IP工具，集爬虫、CF解析、tg通知一条龙，可以部署在vps上定时优选IP

## 使用教程
1.安装requests与bs4
```
pip install requests beautifulsoup4
```
或
```
pip3 install requests beautifulsoup4
```

2.将代码中的下列信息换成自己的
```
# Telegram 机器人 API 配置
telegram_api_token = 'your_api_token'
telegram_chat_id = 'your_chat_id'  # 用你的Chat ID，不是机器人的Chat ID

# Cloudflare 信息
api_key = "your_api_key"
email = "your_email"
zone_id = "your_zone_id"
domain = "your_domain"  # 确保这是完整的域名（如cf.111111.xyz）
```
