#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第三方平台对接测试 - 主运行脚本
"""

import subprocess
import sys
from pathlib import Path

def check_dependencies():
    """检查依赖"""
    print("="*50)
    print("检查依赖...")
    print("="*50)
    
    required_packages = ['playwright', 'docx']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} 已安装")
        except ImportError:
            print(f"✗ {package} 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n缺少依赖包: {', '.join(missing_packages)}")
        print("请运行以下命令安装:")
        print("  pip install playwright python-docx")
        print("  playwright install chromium")
        return False
    
    print("\n所有依赖已就绪！\n")
    return True

def run_test():
    """运行测试"""
    print("="*50)
    print("步骤 1: 登录系统并查找配置")
    print("="*50)
    print()
    
    try:
        result = subprocess.run(
            [sys.executable, "test_third_party_platforms.py"],
            cwd=Path(__file__).parent,
            check=True
        )
        
        if result.returncode != 0:
            print("\n✗ 测试执行失败")
            return False
        
        print("\n✓ 测试执行完成")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 测试执行出错: {e}")
        return False
    except KeyboardInterrupt:
        print("\n\n用户中断测试")
        return False

def generate_report():
    """生成报告"""
    print("\n" + "="*50)
    print("步骤 2: 生成测试报告")
    print("="*50)
    print()
    
    try:
        result = subprocess.run(
            [sys.executable, "generate_test_report.py"],
            cwd=Path(__file__).parent,
            check=True
        )
        
        if result.returncode != 0:
            print("\n✗ 报告生成失败")
            return False
        
        print("\n✓ 报告生成完成")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 报告生成出错: {e}")
        return False

def main():
    """主函数"""
    print("\n" + "="*60)
    print("第三方平台对接配置测试")
    print("="*60)
    print()
    print("测试范围：")
    print("  1. 美团平台配置")
    print("  2. 携程平台配置")
    print("  3. 抖音平台配置")
    print()
    print("="*60)
    print()
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 运行测试
    if not run_test():
        print("\n测试未完成，跳过报告生成")
        return
    
    # 生成报告
    if not generate_report():
        print("\n报告生成失败")
        return
    
    # 完成
    print("\n" + "="*60)
    print("测试完成！")
    print("="*60)
    print()
    print("输出文件：")
    print("  - 测试报告: third_party_test_report/第三方平台对接测试报告.docx")
    print("  - 测试截图: third_party_test_report/screenshots/")
    print("  - 测试数据: third_party_test_report/test_result.json")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n✗ 程序执行出错: {e}")
        import traceback
        traceback.print_exc()
