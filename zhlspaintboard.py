# ZHLSpaintboard v1.0.0
import requests
from PIL import Image
import time

def get_pixel_data(image_path):
    image = Image.open(image_path)
    pixels = image.load()
    width, height = image.size
    return pixels, width, height

def convert_color_to_decimal(color):
    # 将 RGB 转换为十进制
    return color[0] * 0x10000 + color[1] * 0x100 + color[2]

def paint_pixel(x, y, color, uid, token):
    url = "https://paintboard.ayakacraft.com/api/paintboard/paint"  # 替换为实际的服务器地址
    payload = {
        "x": x,
        "y": y,
        "color": color,  # 确保是十进制
        "uid": uid,
        "token": token
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # 检查 HTTP 错误

        # 检查响应是否是 JSON 格式
        if response.headers.get('Content-Type') == 'application/json':
            response_data = response.json()
            print(f"成功绘制像素 ({x}, {y})")
        else:
            print("非 JSON 响应:", response.text)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 错误: {http_err} - 状态码: {response.status_code}")
        print("响应内容:", response.text)
    except requests.exceptions.RequestException as req_err:
        print(f"请求错误: {req_err}")
    except ValueError as json_err:
        print("JSON 解码错误:", json_err)
        print("响应内容:", response.text)

def main(image_path, start_x, start_y, uid, token, cooldown=30):
    pixels, width, height = get_pixel_data(image_path)
    for y in range(height):
        for x in range(width):
            color = pixels[x, y][:3]  # 获取 RGB 值
            paint_pixel(start_x + x, start_y + y, color, uid, token)
            time.sleep(cooldown)  # 冷却时间

if __name__ == "__main__":
    image_path = ""  # 替换为实际的图片路径
    start_x = 0  # 用户指定的起始 x 坐标
    start_y = 0  # 用户指定的起始 y 坐标
    uid = 0  # 替换为实际的用户 ID
    token = ""  # 替换为实际的 token
    main(image_path, start_x, start_y, uid, token)
