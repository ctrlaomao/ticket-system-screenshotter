#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对截图添加马赛克遮罩 - 遮盖敏感信息
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def add_mosaic_mask(image_path, output_path=None, mask_regions=None):
    """
    为截图添加马赛克遮罩
    
    参数:
        image_path: 输入图片路径
        output_path: 输出图片路径（如果为None，则覆盖原图）
        mask_regions: 需要遮罩的区域列表 [(x1, y1, x2, y2, label), ...]
    """
    
    if output_path is None:
        output_path = image_path
    
    try:
        # 打开图片
        img = Image.open(image_path)
        width, height = img.size
        
        print(f"处理图片: {Path(image_path).name}")
        print(f"  尺寸: {width}x{height}")
        
        # 转换为RGBA模式以支持透明度
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 创建绘图对象
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # 如果未指定遮罩区域，使用默认策略
        if mask_regions is None:
            # 默认遮罩策略：假设敏感信息在页面右侧中下部
            # 这些区域通常包含配置输入框
            mask_regions = [
                # 格式: (x1, y1, x2, y2, label)
                # 需要根据实际截图调整
                
                # 示例：遮盖页面右侧可能包含密钥的区域
                (int(width * 0.4), int(height * 0.3), int(width * 0.95), int(height * 0.35), "AppID/密钥"),
                (int(width * 0.4), int(height * 0.4), int(width * 0.95), int(height * 0.45), "AppSecret/密钥"),
                (int(width * 0.4), int(height * 0.5), int(width * 0.95), int(height * 0.55), "Token/令牌"),
                (int(width * 0.4), int(height * 0.6), int(width * 0.95), int(height * 0.65), "回调地址"),
                (int(width * 0.4), int(height * 0.7), int(width * 0.95), int(height * 0.75), "其他密钥"),
            ]
        
        # 添加遮罩
        mask_count = 0
        for region in mask_regions:
            if len(region) >= 4:
                x1, y1, x2, y2 = region[:4]
                label = region[4] if len(region) > 4 else "敏感信息"
                
                # 绘制半透明黑色矩形
                draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, 200))
                
                # 添加标签文字
                try:
                    # 在遮罩中间添加提示文字
                    text_x = x1 + 10
                    text_y = y1 + (y2 - y1) // 2 - 10
                    draw.text((text_x, text_y), f"● {label}已遮盖", fill=(255, 255, 255, 255))
                except:
                    pass
                
                mask_count += 1
                print(f"  ✓ 添加遮罩 {mask_count}: {label} at ({x1},{y1})-({x2},{y2})")
        
        # 合并图层
        img = Image.alpha_composite(img, overlay)
        
        # 转换回RGB模式保存
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        
        # 保存处理后的图片
        img.save(output_path)
        print(f"✓ 打码后的图片已保存: {Path(output_path).name}")
        print(f"  共添加 {mask_count} 个遮罩区域\n")
        
        return output_path
        
    except Exception as e:
        print(f"✗ 处理失败: {e}")
        return None

def process_all_screenshots(screenshots_dir, suffix="_masked"):
    """
    批量处理截图目录中的所有图片
    """
    screenshots_dir = Path(screenshots_dir)
    
    if not screenshots_dir.exists():
        print(f"✗ 目录不存在: {screenshots_dir}")
        return
    
    # 查找所有PNG文件
    image_files = list(screenshots_dir.glob("*.png"))
    
    # 过滤掉已经打码的文件
    image_files = [f for f in image_files if suffix not in f.stem]
    
    if not image_files:
        print("未找到需要处理的截图文件")
        return
    
    print(f"找到 {len(image_files)} 个截图需要处理\n")
    print("="*60)
    
    for img_file in image_files:
        # 生成输出文件名
        output_file = screenshots_dir / f"{img_file.stem}{suffix}{img_file.suffix}"
        
        # 处理图片
        add_mosaic_mask(str(img_file), str(output_file))
        
        print("="*60)
    
    print(f"\n✓ 所有截图处理完成！")
    print(f"  打码后的文件保存在: {screenshots_dir}")

def main():
    """主函数"""
    screenshots_dir = "/workspace/third_party_test_report/screenshots"
    
    print("\n" + "="*60)
    print("截图打码工具 - 遮盖敏感信息")
    print("="*60 + "\n")
    
    # 处理所有截图
    process_all_screenshots(screenshots_dir)

if __name__ == "__main__":
    main()
