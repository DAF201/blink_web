import json

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}
with open('./config/config.json','r')as config:
    config = json.load(config)
    param = config['param']
    cookie = config['cookie']
    enable_general_log = config['general_log']
    enable_admin_log = config['admin_log']
    enable_ban_log = config['ban_log']
    passcode = config['passcode']
    first_cover = config['first_cover']
    second_cover = config['second_cover']
    icon = config['icon']

data_base = 'https://api.bilibili.com/x/dynamic/feed/draw/upload_bfs'
