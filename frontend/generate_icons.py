#!/usr/bin/env python3
from PIL import Image, ImageDraw
import os

# 图标尺寸
SIZE = 81
ICON_DIR = "src/assets/icons"

# 颜色配置
INACTIVE_COLOR = "#999999"  # 未激活颜色（灰色）
ACTIVE_COLOR = "#1890ff"    # 激活颜色（蓝色）

def create_home_icon(color, filename):
    """创建首页图标（房子）"""
    img = Image.new('RGBA', (SIZE, SIZE), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # 绘制房子屋顶
    roof = [(20, 40), (40, 20), (60, 40)]
    draw.polygon(roof, fill=color)

    # 绘制房子主体
    draw.rectangle([25, 40, 55, 65], fill=color)

    # 绘制门
    draw.rectangle([35, 50, 45, 65], fill='white')

    img.save(os.path.join(ICON_DIR, filename))

def create_search_icon(color, filename):
    """创建搜索图标（放大镜）"""
    img = Image.new('RGBA', (SIZE, SIZE), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # 绘制放大镜圆圈
    draw.ellipse([20, 20, 50, 50], outline=color, width=4)

    # 绘制放大镜手柄
    draw.line([(47, 47), (60, 60)], fill=color, width=4)

    img.save(os.path.join(ICON_DIR, filename))

def create_template_icon(color, filename):
    """创建模板图标（文档）"""
    img = Image.new('RGBA', (SIZE, SIZE), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # 绘制文档外框
    draw.rectangle([25, 15, 55, 65], outline=color, width=3)

    # 绘制文档折角
    draw.polygon([(55, 15), (55, 25), (45, 15)], fill=color)

    # 绘制文档内容线条
    draw.line([(30, 30), (50, 30)], fill=color, width=2)
    draw.line([(30, 38), (50, 38)], fill=color, width=2)
    draw.line([(30, 46), (50, 46)], fill=color, width=2)
    draw.line([(30, 54), (45, 54)], fill=color, width=2)

    img.save(os.path.join(ICON_DIR, filename))

def create_profile_icon(color, filename):
    """创建个人中心图标（用户头像）"""
    img = Image.new('RGBA', (SIZE, SIZE), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # 绘制头部（圆形）
    draw.ellipse([30, 20, 50, 40], fill=color)

    # 绘制身体（半圆）
    draw.pieslice([20, 40, 60, 70], 0, 180, fill=color)

    img.save(os.path.join(ICON_DIR, filename))

# 确保目录存在
os.makedirs(ICON_DIR, exist_ok=True)

# 生成所有图标
print("生成图标文件...")

# 首页图标
create_home_icon(INACTIVE_COLOR, "home.png")
create_home_icon(ACTIVE_COLOR, "home-active.png")
print("✓ 首页图标已生成")

# 搜索图标
create_search_icon(INACTIVE_COLOR, "search.png")
create_search_icon(ACTIVE_COLOR, "search-active.png")
print("✓ 搜索图标已生成")

# 模板图标
create_template_icon(INACTIVE_COLOR, "template.png")
create_template_icon(ACTIVE_COLOR, "template-active.png")
print("✓ 模板图标已生成")

# 个人中心图标
create_profile_icon(INACTIVE_COLOR, "profile.png")
create_profile_icon(ACTIVE_COLOR, "profile-active.png")
print("✓ 个人中心图标已生成")

print("\n所有图标已生成完毕！")
