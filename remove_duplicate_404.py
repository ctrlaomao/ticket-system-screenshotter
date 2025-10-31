#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除重复的404/空白截图并更新文档
"""

import os
import json
from pathlib import Path

SCREENSHOTS_DIR = "/workspace/screenshots_v2"
MENU_DATA_FILE = "/workspace/menu_structure_v2.json"

# 这些是重复的文件（除了第一个，其他都删除）
DUPLICATE_FILES = [
    "007_订单管理-预约订单.png",
    "008_订单管理-寄存订单.png",
    "009_订单管理-教学订单.png",
    "010_订单管理-团队订单.png",
    "016_通行管理-卡片管理.png",
    "017_通行管理-通行记录.png",
    "018_通行管理-通行规则.png",
    "022_控制面板-教练管理.png",
    "023_控制面板-教练评论.png",
    "024_控制面板-排班管理.png",
    "025_控制面板-运动级别.png",
    "026_控制面板-租赁物管理.png",
    "027_控制面板-租赁物分类.png",
    "028_控制面板-分销商管理.png",
    "029_控制面板-分销订单.png",
    "030_报表管理-票务核销报表.png",
    "031_报表管理-教学核销报表.png",
    "032_报表管理-教学数据看板.png",
    "033_报表管理-租赁核销报表.png",
    "034_报表管理-租赁物明细报表.png",
    "039_系统管理-审计日志.png",
    "041_系统管理-文本模板.png",
    "043_系统管理-门店管理.png",
]

def main():
    print("=" * 60)
    print("删除重复/404截图并更新数据...")
    print("=" * 60)
    
    screenshots_dir = Path(SCREENSHOTS_DIR)
    
    # 删除截图文件
    deleted_count = 0
    for filename in DUPLICATE_FILES:
        filepath = screenshots_dir / filename
        if filepath.exists():
            filepath.unlink()
            print(f"✓ 已删除: {filename}")
            deleted_count += 1
        else:
            print(f"- 文件不存在: {filename}")
    
    print(f"\n共删除 {deleted_count} 个文件")
    
    # 更新menu_structure_v2.json
    with open(MENU_DATA_FILE, 'r', encoding='utf-8') as f:
        menu_data = json.load(f)
    
    # 移除已删除的截图对应的记录
    original_count = len(menu_data)
    menu_data = [item for item in menu_data if item['screenshot'] not in DUPLICATE_FILES]
    new_count = len(menu_data)
    
    # 保存更新后的数据
    with open(MENU_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(menu_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 已更新菜单结构文件")
    print(f"  原有记录: {original_count} 条")
    print(f"  删除记录: {original_count - new_count} 条")
    print(f"  剩余记录: {new_count} 条")
    
    print("\n" + "=" * 60)
    print("清理完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
