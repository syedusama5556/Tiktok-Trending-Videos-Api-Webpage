import socks
import json
import requests

# Set the location coordinates (latitude and longitude)
latitude = 37.7749
longitude = -122.4194


# Set up the SOCKS5 proxy
proxy_host = "localhost"
proxy_port = 5566

# Set the proxy settings for the SOCKS5 proxy
proxies = {
    "http": f"socks5://{proxy_host}:{proxy_port}",
    "https": f"socks5://{proxy_host}:{proxy_port}",
}

# Create a requests Session with SOCKS5 proxy settings
session = requests.Session()
session.proxies = proxies

useProxy = False


def fetch_and_save_tiktok_data(
    count=30, region="CA", priority_region="CA", language="pt", sys_region="CA"
):
    url = "https://www.tiktok.com/api/item_list"
    params = {
        "aid": 1988,
        "app_name": "tiktok_web",
        "device_platform": "web",
        "referer": "",
        "root_referer": "",
        "user_agent": "Mozilla/5.0 (Linux; Android 10;TXY567) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/8399.0.9993.96 Mobile Safari/599.36",
        "cookie_enabled": "true",
        "screen_width": 1080,
        "screen_height": 1920,
        "browser_language": "en-us",
        "browser_platform": "Linux",
        "browser_name": "chrome",
        "browser_version": 8399,
        "browser_online": "true",
        "ac": "4g",
        "timezone_name": "UTC+05",
        "appId": 1233,
        "appType": "m",
        "isAndroid": "true",
        "isMobile": "true",
        "isIOS": "false",
        "OS": "windows",
        "count": count,
        "id": 1,
        "secUid": "",
        "maxCursor": 30,
        "minCursor": 0,
        "sourceType": 12,
        "region": region,
        "priority_region": priority_region,
        "language": language,
        "sys_region": sys_region,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    }

    response = requests.get(url, headers=headers, params=params)

    try:
        # Check if the response status is 200 OK
        if response.status_code == 200:
            data = json.loads(response.text)
            video_list = []

            for item in data["items"]:
                video_url = item["video"]["bitrateInfo"][0]["CodecType"]
                description = item["desc"]
                print(f"Video URL: {video_url}")
                print(f"Description: {description}")
                print()
                video_list.append(item)

            with open("jsonresponse.json", "w", encoding="utf-8") as f:
                json.dump(video_list, f, ensure_ascii=False)
        else:
            print(
                "Error fetching data from TikTok API. Status Code:",
                response.status_code,
            )

    except requests.exceptions.JSONDecodeError as e:
        print("Error decoding JSON response:", e)


def fetch_and_save_tiktok_data_method2(
    count=30, region="US", priority_region="TW", language="en"
):
    url = "https://www.tiktok.com/api/recommend/item_list/"

    params = {
        "aid": 1988,
        "app_language": "en",
        "app_name": "tiktok_web",
        "browser_language": "en-US",
        "browser_name": "Mozilla",
        "browser_online": "true",
        "browser_platform": "Linux x86_64",
        "browser_version": "5.0 (X11)",
        "channel": "tiktok_web",
        "cookie_enabled": "true",
        "count": 30,
        "device_id": "7163916748088903169",
        "device_platform": "web_pc",
        "focus_state": "false",
        "from_page": "fyp",
        "history_len": 5,
        "is_fullscreen": "false",
        "is_page_visible": "true",
        "os": "linux",
        "priority_region": priority_region,
        "referer": "",
        "region": priority_region,
        "screen_height": 1080,
        "screen_width": 1920,
        "tz_name": "Asia/Tokyo",
        "webcast_language": "en",
    }

    # url = "https://www.tiktok.com/api/item_list/"
    # params = {
    #     'count': count,
    #     'id': 1,
    #     'type': 5,
    #     'secUid': '',
    #     'maxCursor': 0,
    #     'minCursor': 0,
    #     'sourceType': 12,
    #     'appId': 1233,
    #     'region': region,
    #     'language': 'en'
    # }

    proxy_servers = {
        "http": "http://proxy.sample.com:8080",
        "https": "http://secureproxy.sample.com:8080",
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Cookie": "_abck=2CF8F8BC23F4CB9FB5F911FF2C0176D0~-1~YAAQl7h3by5vOzKGAQAAmRfKgglVcAbrJyqRuPiwQfAC4UB/pUpfWk5Y6p2MI0xPjNLKc3J6U6w07gMDZwmhcEzr1vgWghrjHehRXMBl192l4RhT/SB6Bhx18TFAsMh/TDVSS9JYqrDaMLbWYEq/A6NfgFx9Qzy6TsK/v6mO17m2stPjAm+8embQBqe8Ou4yoNwlYrnCvQzdz4w0xzORuwvdZOa364E25SI4vlCTwsEiYNBUMeZXw+tEjpLs6kCQxrfSXNF5+TwCTiZvm6l/E6+ayuZC1fx1q2JFwiy4TVAicaxU5Uhj/seqgJ4Q2o+Yuq4RJVDlpQkLRHY+vF01BaDAk4ULL8o8fKXJUMsYdsQKSmY6Z55Cve+zg8UHX7okM0iBI0NybA==~-1~-1~-1; msToken=Hhug6t0n_f207IR3X2GsFI3peBWe0rwXYtDQ-AzUyChhmoCasV2kVA6-i0LAT2QZHp15v-sS43Zp33j_j1pT7sPTRMOm-6VKuOcGDAJy5BcAPXgmCwRgPN4Hy8hcDFgeg1PEMV77ydoF2g==; ttwid=1%7Ccc6x517cmVJj7I4zCjOKzG7cZ7mlkfoqyo0VICCSNzI%7C1676396167%7Cf9fd4baeb5e24fa71da2eedfe90cf39a58a6a9ff2d95cc3e1aa0c45dc0473046",
    }

    global useProxy

    if useProxy:
        response = session.get(url, headers=headers, params=params)
    else:
        response = requests.get(url, headers=headers, params=params)

    # print(response.text)
    try:
        # Check if the response status is 200 OK
        if response.status_code == 200:
            data = json.loads(response.text)
            video_list = []

            if "itemList" in data:
                for item in data["itemList"]:
                    video_url = item["video"]["bitrateInfo"][0]["CodecType"]
                    description = item["desc"]
                    print(f"Video URL: {video_url}")
                    print(f"Description: {description}")
                    print()
                    video_list.append(item)

            else:
                for item in data["items"]:
                    video_url = item["video"]["bitrateInfo"][0]["CodecType"]
                    description = item["desc"]
                    print(f"Video URL: {video_url}")
                    print(f"Description: {description}")
                    print()
                    video_list.append(item)

            with open("jsonresponse.json", "w", encoding="utf-8") as f:
                json.dump(video_list, f, ensure_ascii=False)
        else:
            print(
                "Error fetching data from TikTok API. Status Code:",
                response.status_code,
            )

    except requests.exceptions.JSONDecodeError as e:
        print("Error decoding JSON response:", e)


# fetch_and_save_tiktok_data_method2()
