from PIL import Image, ImageDraw
import requests
from io import BytesIO
import matplotlib.pyplot as plt
from constant import *

# 10个图片的URL列表
image_urls = [
    pic_url,
    pic_url,
    pic_url,
    pic_url,
    # 添加其他8个URL
]

# 创建一个横向的图像
width = 1600  # 图片总宽度
height = 800  # 图片高度
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

# 分割线的位置
line_position = width // 2

# 每个区域的宽度
image_width = line_position // len(image_urls)

# 逐个绘制左边的图片
for i, url in enumerate(image_urls):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    # 调整图片大小以适应宽度
    img = img.resize((image_width, int(height / 3)))

    # 将图片粘贴到左侧区域上
    image.paste(img, (i * image_width, 0))
    text = "汉字"  # 替换为你想要的汉字
    draw.text((i * image_width, height - 40), text, fill="black")


# 在中间添加分割线
draw.line([(line_position, 0), (line_position, height * 2)], fill="red", width=20)

# 逐个绘制右边的图片
for i, url in enumerate(image_urls, start=len(image_urls)):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    # 调整图片大小以适应宽度
    img = img.resize((image_width, int(height / 3)))

    # 将图片粘贴到右侧区域上
    image.paste(img, (line_position + 20 + (i - len(image_urls)) * image_width, 0))

# 显示绘制结果
plt.imshow(image)
plt.axis("off")  # 关闭坐标轴
plt.show()
