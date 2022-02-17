import json
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}
with open('./config/config.json')as config:
    config = json.load(config)
    param = config['param']
    cookie = config['cookie']
    request_log = config['request_log']
    admin_log = config['admin_log']
    ban_log = config['ban_log']

data_base = 'https://api.bilibili.com/x/dynamic/feed/draw/upload_bfs'
