import random
from time import time, localtime
import cityinfo
from requests import get, post
from datetime import datetime, date
import sys
import os
import http.client, urllib
import json
from zhdate import ZhDate
global false, null, true
false = null = true = ''
def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)


def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token

def get_birthday(birthday, year, today):
    birthday_year = birthday.split("-")[0]
    # 判断是否为农历生日
    if birthday_year[0] == "r":
        r_mouth = int(birthday.split("-")[1])
        r_day = int(birthday.split("-")[2])
        # 今年生日
        birthday = ZhDate(year, r_mouth, r_day).to_datetime().date()
        year_date = birthday


    else:
        # 获取国历生日的今年对应月和日
        birthday_month = int(birthday.split("-")[1])
        birthday_day = int(birthday.split("-")[2])
        # 今年生日
        year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        if birthday_year[0] == "r":
            # 获取农历明年生日的月和日
            r_last_birthday = ZhDate((year + 1), r_mouth, r_day).to_datetime().date()
            birth_date = date((year + 1), r_last_birthday.month, r_last_birthday.day)
        else:
            birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day



def get_weather(province, city):
    # 城市id
    try:
        city_id = cityinfo.cityInfo[province][city]["AREAID"]
    except KeyError:
        print("推送消息失败，请检查省份或城市是否正确")
        os.system("pause")
        sys.exit(1)
    # city_id = 101280101
    # 毫秒级时间戳
    t = (int(round(time() * 1000)))
    headers = {
        "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(city_id),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = "http://d1.weather.com.cn/dingzhi/{}.html?_={}".format(city_id, t)
    response = get(url, headers=headers)
    response.encoding = "utf-8"
    response_data = response.text.split(";")[0].split("=")[-1]
    response_json = eval(response_data)
    # print(response_json)
    weatherinfo = response_json["weatherinfo"]
    # 天气
    weather = weatherinfo["weather"]
    # 最高气温
    temp = weatherinfo["temp"]
    # 最低气温
    tempn = weatherinfo["tempn"]
    return weather, temp, tempn



#词霸每日一句
def get_ciba():
    if (Whether_Eng!=False):
        try:
            url = "http://open.iciba.com/dsapi/"
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
            }
            r = get(url, headers=headers)
            note_en = r.json()["content"]
            note_ch = r.json()["note"]
            return (note_en,note_ch)
        except:
            return ("词霸API调取错误")


#彩虹屁
def caihongpi():
    if (Whether_caihongpi!=False):
        try:
            conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
            params = urllib.parse.urlencode({'key':tianxing_API})
            headers = {'Content-type':'application/x-www-form-urlencoded'}
            conn.request('POST','/saylove/index',params,headers)
            res = conn.getresponse()
            data = res.read()
            data = json.loads(data)
            data = data["newslist"][0]["content"]
            if("XXX" in data):
                data.replace("XXX","蒋蒋")
            return data
        except:
            return ("彩虹屁API调取错误，请检查API是否正确申请或是否填写正确")

#健康小提示API
def health():
    if (Whether_health!=False):
        try:
            conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
            params = urllib.parse.urlencode({'key':tianxing_API})
            headers = {'Content-type':'application/x-www-form-urlencoded'}
            conn.request('POST','/healthtip/index',params,headers)
            res = conn.getresponse()
            data = res.read()
            data = json.loads(data)
            data = data["newslist"][0]["content"]
            return data
        except:
             return ("健康小提示API调取错误，请检查API是否正确申请或是否填写正确")

#星座运势
def lucky():
    if ( Whether_lucky!=False):
        try:
            conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
            params = urllib.parse.urlencode({'key':tianxing_API,'astro':astro})
            headers = {'Content-type':'application/x-www-form-urlencoded'}
            conn.request('POST','/star/index',params,headers)
            res = conn.getresponse()
            data = res.read()
            data = json.loads(data)
            data = "爱情指数："+str(data["newslist"][1]["content"])+"   工作指数："+str(data["newslist"][2]["content"])+"\n今日概述："+str(data["newslist"][8]["content"])
            return data
        except:
            return ("星座运势API调取错误，请检查API是否正确申请或是否填写正确")

#励志名言
def lizhi():
    if (Whether_lizhi!=False):
        try:
            conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
            params = urllib.parse.urlencode({'key':tianxing_API})
            headers = {'Content-type':'application/x-www-form-urlencoded'}
            conn.request('POST','/lzmy/index',params,headers)
            res = conn.getresponse()
            data = res.read()
            data = json.loads(data)
            return data["newslist"][0]["saying"]
        except:
            return ("励志古言API调取错误，请检查API是否正确申请或是否填写正确")
        

#下雨概率和建议
def tip():
    if (Whether_tip!=False):
        try:
            conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
            params = urllib.parse.urlencode({'key':tianxing_API,'city':city})
            headers = {'Content-type':'application/x-www-form-urlencoded'}
            conn.request('POST','/tianqi/index',params,headers)
            res = conn.getresponse()
            data = res.read()
            data = json.loads(data)
            pop = data["newslist"][0]["pop"]
            tips = data["newslist"][0]["tips"]
            return pop,tips
        except:
            return ("天气预报API调取错误，请检查API是否正确申请或是否填写正确"),""

#推送信息
def send_message(to_user, access_token, city_name, weather, max_temperature, min_temperature, pipi, lizhi, pop, tips, note_en, note_ch, health_tip, lucky_):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 获取在一起的日子的日期格式
    love_year = int(config["love_date"].split("-")[0])
    love_month = int(config["love_date"].split("-")[1])
    love_day = int(config["love_date"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    # 获取所有生日数据
    birthdays = {}
    for k, v in config.items():
        if k[0:5] == "birth":
            birthdays[k] = v
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": get_color()
            },
            "city": {
                "value": city_name,
                "color": get_color()
            },
            "weather": {
                "value": weather,
                "color": get_color()
            },
            "min_temperature": {
                "value": min_temperature,
                "color": get_color()
            },
            "max_temperature": {
                "value": max_temperature,
                "color": get_color()
            },
            "love_day": {
                "value": love_days,
                "color": get_color()
            },
            "note_en": {
                "value": note_en,
                "color": get_color()
            },
            "note_ch": {
                "value": note_ch,
                "color": get_color()
            },

            "pipi": {
                "value": pipi,
                "color": get_color()
            },

            "lucky": {
                "value": lucky_,
                "color": get_color()
            },

            "lizhi": {
                "value": lizhi,
                "color": get_color()
            },

            "pop": {
                "value": pop,
                "color": get_color()
            },

            "health": {
                "value": health_tip,
                "color": get_color()
            },

            "tips": {
                "value": tips,
                "color": get_color()
            }
        }
    }
    for key, value in birthdays.items():
        # 获取距离下次生日的时间
        birth_day = get_birthday(value, year, today)
        # 将生日数据插入data
        data["data"][key] = {"value": birth_day, "color": get_color()}
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)
# 推送server酱
def push_wx(sckey, desp=""):
    """
    推送消息到微信
    """
    if sckey == '':
        print("[注意] 未提供sckey，不进行推送！")
    else:
        server_url = f"https://sc.ftqq.com/{sckey}.send"
        params = {
            "text": '小米运动 步数修改',
            "desp": desp
        }
 
        response = requests.get(server_url, params=params)
        json_data = response.json()
 
        if json_data['errno'] == 0:
            print(f"[{now}] 推送成功。")
        else:
            print(f"[{now}] 推送失败：{json_data['errno']}({json_data['errmsg']})")

# 推送server
def push_server(sckey, desp=""):
    """
    推送消息到微信
    """
    if sckey == '':
        print("[注意] 未提供sckey，不进行微信推送！")
    else:
        server_url = f"https://sctapi.ftqq.com/{sckey}.send"
        params = {
            "title": '小米运动 步数修改',
            "desp": desp
        }
 
        response = requests.get(server_url, params=params)
        json_data = response.json()
 
        if json_data['code'] == 0:
            print(f"[{now}] 推送成功。")
        else:
            print(f"[{now}] 推送失败：{json_data['code']}({json_data['message']})")

# 推送pushplus
def push_pushplus(token, content=""):
    """
    推送消息到pushplus
    """
    if token == '':
        print("[注意] 未提供token，不进行pushplus推送！")
    else:
        server_url = f"http://www.pushplus.plus/send"
        params = {
            "token": token,
            "title": '小米运动 步数修改',
            "content": content
        }
 
        response = requests.get(server_url, params=params)
        json_data = response.json()
 
        if json_data['code'] == 200:
            print(f"[{now}] 推送成功。")
        else:
            print(f"[{now}] 推送失败：{json_data['code']}({json_data['message']})")

# 推送tg
def push_tg(token, chat_id, desp=""):
    """
    推送消息到TG
    """
    if token == '':
        print("[注意] 未提供token，不进行tg推送！")
    elif chat_id == '':
        print("[注意] 未提供chat_id，不进行tg推送！")
    else:
        server_url = f"https://api.telegram.org/bot{token}/sendmessage"
        params = {
            "text": '小米运动 步数修改\n\n' + desp,
            "chat_id": chat_id
        }
 
        response = requests.get(server_url, params=params)
        json_data = response.json()
 
        if json_data['ok'] == True:
            print(f"[{now}] 推送成功。")
        else:
            print(f"[{now}] 推送失败：{json_data['error_code']}({json_data['description']})")
# 企业微信推送
def wxpush(msg, usr, corpid, corpsecret, agentid=1000002):
    base_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'
    req_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='
    corpid = corpid
    corpsecret = corpsecret
    agentid = agentid

    if agentid == 0:
        agentid = 1000002

    #获取access_token，每次的access_token都不一样，所以需要运行一次请求一次
    def get_access_token(base_url, corpid, corpsecret):
        urls = base_url + 'corpid=' + corpid + '&corpsecret=' + corpsecret
        resp = requests.get(urls).json()
        access_token = resp['access_token']
        return access_token

    def send_message(msg, usr):
        data = get_message(msg, usr)
        req_urls = req_url + get_access_token(base_url, corpid, corpsecret)
        res = requests.post(url=req_urls, data=data)
        ret = res.json()
        if ret["errcode"] == 0:
            print(f"[{now}] 企业微信推送成功")
        else:
            print(f"[{now}] 推送失败：{ret['errcode']} 错误信息：{ret['errmsg']}")

    def get_message(msg, usr):
        data = {
            "touser": usr,
            "toparty": "@all",
            "totag": "@all",
            "msgtype": "text",
            "agentid": agentid,
            "text": {
                "content": msg
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        data = json.dumps(data)
        return data

    msg = msg
    usr = usr
    if corpid == '':
        print("[注意] 未提供corpid，不进行企业微信推送！")
    elif corpsecret == '':
        print("[注意] 未提供corpsecret，不进行企业微信推送！")
    else:
        send_message(msg, usr)


if __name__ == "__main__":
    try:
        with open("./config.json", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)

    # 获取accessToken
    accessToken = get_access_token()
    # 接收的用户
    users = config["user"]
    # 传入省份和市获取天气信息
    province, city = config["province"], config["city"]
    weather, max_temperature, min_temperature = get_weather(province, city)
    #获取天行API
    tianxing_API=config["tianxing_API"]
    #是否开启天气预报API
    Whether_tip=config["Whether_tip"]
    #是否启用词霸每日一句
    Whether_Eng=config["Whether_Eng"]
    #是否启用星座API
    Whether_lucky=config["Whether_lucky"]
    #是否启用励志古言API
    Whether_lizhi=config["Whether_lizhi"]
    #是否启用彩虹屁API
    Whether_caihongpi=config["Whether_caihongpi"]
    #是否启用健康小提示API
    Whether_health=config["Whether_health"]
    #获取星座
    astro = config["astro"]
    # 获取词霸每日金句
    note_ch, note_en = get_ciba()
    #彩虹屁
    pipi = caihongpi()
    #健康小提示
    health_tip = health()
    #下雨概率和建议
    pop,tips = tip()
    #励志名言
    lizhi = lizhi()
    #星座运势
    lucky_ = lucky()
    # 公众号推送消息
    for user in users:
        send_message(user, accessToken, city, weather, max_temperature, min_temperature, pipi, lizhi,pop,tips, note_en, note_ch, health_tip, lucky_)
    import time
    time_duration = 3.5
    time.sleep(time_duration)
