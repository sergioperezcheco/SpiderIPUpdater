# SpiderIPUpdater
一款优选IP工具，集爬虫、CF解析、tg通知一条龙，可以部署在vps上定时优选IP

## 使用教程
0.下载脚本
```
git clone https://github.com/sergioperezcheco/SpiderIPUpdater.git
cd SpiderIPUpdater
```
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

3.运行脚本
```
python3 345673.py
```

## 定时任务（推荐）
1.打卡crontab编辑器
```
crontab -e
```
2.添加定时任务
```
0 */2 * * * /usr/bin/python3 /SpiderIPUpdater/345673.py
# 0：每个小时的第0分钟，即整点时刻。
# */2：每两小时执行一次。
# *：分别代表每一天、每一个月以及每一个星期。
# /usr/bin/python3：Python 3的实际路径。
# /SpiderIPUpdater/345673.py：你的Python脚本的绝对路径。
```
3.保存并退出（类似vim）
4.赋予权限
```
chmod +x /SpiderIPUpdater/345673.py
```

## 致谢
感谢https://345673.xyz、https://ipdb.api.030101.xyz等项目提供的优选IP



