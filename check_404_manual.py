#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动查看截图内容判断404
"""

from PIL import Image
import sys

def analyze_screenshot(image_path):
    """详细分析截图"""
    img = Image.open(image_path)
    print(f"\n分析: {image_path}")
    print(f"尺寸: {img.size}")
    print(f"模式: {img.mode}")
    
    # 检查中心区域
    img_rgb = img.convert('RGB')
    width, height = img.size
    center_x, center_y = width // 2, height // 2
    
    # 采样中心区域的多个点
    print("\n中心区域像素采样:")
    for i in range(-5, 6):
        for j in range(-5, 6):
            x = center_x + i * 50
            y = center_y + j * 50
            if 0 <= x < width and 0 <= y < height:
                r, g, b = img_rgb.getpixel((x, y))
                if not (r > 200 and g > 200 and b > 200):  # 如果不是白色
                    print(f"  位置({x},{y}): RGB({r},{g},{b})")

# 对比两张不同的截图
print("=" * 60)
analyze_screenshot("/workspace/screenshots_v2/005_订单管理-订单列表.png")
print("\n" + "=" * 60)
analyze_screenshot("/workspace/screenshots_v2/007_订单管理-预约订单.png")
print("\n" + "=" * 60)
