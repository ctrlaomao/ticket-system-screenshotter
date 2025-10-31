#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查重复或404截图（通过文件hash）
"""

import os
import json
import hashlib
from pathlib import Path
from PIL import Image

SCREENSHOTS_DIR = "/workspace/screenshots_v2"
MENU_DATA_FILE = "/workspace/menu_structure_v2.json"

def get_file_hash(filepath):
    """计算文件的MD5哈希值"""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def check_if_blank_or_404(image_path):
    """检查图片是否是空白页或404页面"""
    try:
        img = Image.open(image_path)
        img_rgb = img.convert('RGB')
        width, height = img.size
        
        # 采样多个区域
        samples = []
        for x in range(100, width-100, 200):
            for y in range(100, height-100, 200):
                r, g, b = img_rgb.getpixel((x, y))
                samples.append((r, g, b))
        
        # 检查是否大部分像素都是浅色（白色或浅灰色）
        light_pixels = sum(1 for r, g, b in samples if r > 230 and g > 230 and b > 230)
        
        if light_pixels > len(samples) * 0.8:
            return True, "大部分是白色背景"
        
        return False, "正常内容"
        
    except Exception as e:
        return False, f"检查出错: {str(e)}"

def main():
    print("=" * 60)
    print("检查重复和404截图...")
    print("=" * 60)
    
    screenshots_dir = Path(SCREENSHOTS_DIR)
    screenshots = sorted(screenshots_dir.glob("*.png"))
    
    # 按hash分组
    hash_groups = {}
    file_info = {}
    
    for screenshot in screenshots:
        file_hash = get_file_hash(screenshot)
        file_size = os.path.getsize(screenshot)
        
        if file_hash not in hash_groups:
            hash_groups[file_hash] = []
        hash_groups[file_hash].append(screenshot.name)
        
        file_info[screenshot.name] = {
            'hash': file_hash,
            'size': file_size
        }
    
    # 找出重复的文件
    duplicates = {h: files for h, files in hash_groups.items() if len(files) > 1}
    
    print(f"\n共有 {len(screenshots)} 个截图文件")
    print(f"发现 {len(duplicates)} 组重复文件\n")
    
    screenshots_to_remove = []
    
    for hash_val, files in duplicates.items():
        print(f"\n重复组（共{len(files)}个文件）:")
        first_file = screenshots_dir / files[0]
        is_blank, reason = check_if_blank_or_404(first_file)
        
        for f in files:
            file_size = file_info[f]['size'] / 1024
            print(f"  - {f} ({file_size:.1f}KB)")
        
        print(f"  状态: {reason}")
        
        if is_blank:
            print(f"  ❌ 这是空白/404页面，标记删除")
            screenshots_to_remove.extend(files)
        else:
            # 即使不是空白页，如果有重复，也只保留第一个
            print(f"  ⚠️  虽然不是404，但存在重复，保留第一个，删除其余")
            screenshots_to_remove.extend(files[1:])
    
    # 检查单独的可疑文件
    print("\n" + "=" * 60)
    print("检查所有文件是否为404...")
    print("=" * 60)
    
    for screenshot in screenshots:
        if screenshot.name not in screenshots_to_remove:
            is_blank, reason = check_if_blank_or_404(screenshot)
            if is_blank:
                print(f"❌ {screenshot.name} - {reason}")
                screenshots_to_remove.append(screenshot.name)
    
    print("\n" + "=" * 60)
    print(f"需要删除的截图: {len(screenshots_to_remove)} 个")
    print("=" * 60)
    
    if screenshots_to_remove:
        print("\n待删除的文件：")
        for name in sorted(set(screenshots_to_remove)):
            print(f"  - {name}")
        
        # 保存结果
        with open("/workspace/screenshots_to_remove.json", "w", encoding="utf-8") as f:
            json.dump(sorted(set(screenshots_to_remove)), f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 结果已保存到: /workspace/screenshots_to_remove.json")
    else:
        print("\n✓ 所有截图都正常")

if __name__ == "__main__":
    main()
