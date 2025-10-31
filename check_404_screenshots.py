#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查并删除404截图
"""

import os
import json
from pathlib import Path
from PIL import Image

SCREENSHOTS_DIR = "/workspace/screenshots_v2"
MENU_DATA_FILE = "/workspace/menu_structure_v2.json"

def check_screenshot_for_404(image_path):
    """
    检查截图是否包含404错误
    通过图片大小和简单的像素分析
    """
    try:
        # 检查文件大小，404页面通常比较小
        file_size = os.path.getsize(image_path)
        
        # 打开图片
        img = Image.open(image_path)
        
        # 方法1：检查文件大小（404页面通常小于60KB）
        if file_size < 60000:
            # 进一步检查图片内容
            # 转换为RGB
            img_rgb = img.convert('RGB')
            # 获取中心区域的像素
            width, height = img.size
            center_x, center_y = width // 2, height // 2
            
            # 采样一些像素点看是否主要是白色背景（404页面特征）
            white_count = 0
            sample_points = [
                (center_x, center_y),
                (center_x - 100, center_y),
                (center_x + 100, center_y),
                (center_x, center_y - 100),
                (center_x, center_y + 100),
            ]
            
            for x, y in sample_points:
                if 0 <= x < width and 0 <= y < height:
                    r, g, b = img_rgb.getpixel((x, y))
                    # 检查是否接近白色
                    if r > 240 and g > 240 and b > 240:
                        white_count += 1
            
            # 如果大部分采样点是白色，可能是404页面
            if white_count >= 3:
                return True, "小文件且主要是白色背景"
        
        return False, "正常截图"
        
    except Exception as e:
        return False, f"检查出错: {str(e)}"

def main():
    print("=" * 60)
    print("检查404截图...")
    print("=" * 60)
    
    screenshots_dir = Path(SCREENSHOTS_DIR)
    screenshots = sorted(screenshots_dir.glob("*.png"))
    
    screenshots_404 = []
    
    for screenshot in screenshots:
        is_404, reason = check_screenshot_for_404(screenshot)
        
        file_size = os.path.getsize(screenshot) / 1024  # KB
        
        if is_404:
            print(f"❌ {screenshot.name} - {file_size:.1f}KB - {reason}")
            screenshots_404.append(screenshot.name)
        else:
            print(f"✓ {screenshot.name} - {file_size:.1f}KB - {reason}")
    
    print("\n" + "=" * 60)
    print(f"发现 {len(screenshots_404)} 个可能的404截图")
    print("=" * 60)
    
    if screenshots_404:
        print("\n可能是404的截图：")
        for name in screenshots_404:
            print(f"  - {name}")
        
        # 保存结果
        with open("/workspace/404_screenshots.json", "w", encoding="utf-8") as f:
            json.dump(screenshots_404, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 结果已保存到: /workspace/404_screenshots.json")
    else:
        print("\n✓ 未发现404截图")

if __name__ == "__main__":
    main()
