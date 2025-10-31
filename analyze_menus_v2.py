#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进版菜单分析脚本 - 通过实际点击获取URL
"""

import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

LOGIN_URL = "https://xstest.axioxio.com/Account/login"
USERNAME = "13811458301"
PASSWORD = "4<z%0/RS"
MENU_DATA_FILE = "/workspace/menu_structure_v2.json"
ANALYSIS_RESULT = "/workspace/menu_analysis_result.json"

class MenuAnalyzerV2:
    def __init__(self):
        # 加载已有截图数据
        with open(MENU_DATA_FILE, 'r', encoding='utf-8') as f:
            self.existing_data = json.load(f)
        
        # 已有截图的URL集合
        self.existing_urls = set()
        self.existing_names = {}
        for item in self.existing_data:
            if 'url' in item:
                self.existing_urls.add(item['url'])
                self.existing_names[item['url']] = item['path']
        
        print(f"已加载 {len(self.existing_data)} 个已有截图")
        
        # 存储找到的所有菜单
        self.all_menus = {}  # {url: name}
        
    def login(self, page):
        """登录"""
        print("正在登录...")
        page.goto(LOGIN_URL, wait_until="domcontentloaded")
        time.sleep(3)
        
        page.locator("input[type='text']").first.fill(USERNAME)
        page.locator("input[type='password']").first.fill(PASSWORD)
        time.sleep(1)
        page.locator("button[type='submit']").click()
        time.sleep(5)
        
        try:
            page.keyboard.press("Escape")
            time.sleep(0.5)
        except:
            pass
        
        if page.url != LOGIN_URL:
            print("✓ 登录成功！\n")
            return True
        return False
    
    def traverse_all_clickable_menus(self, page):
        """遍历所有可点击的菜单项"""
        print("开始遍历所有可点击菜单...")
        time.sleep(2)
        
        visited_urls = set()
        menu_items_selector = "nav li, .sidebar li, aside li, .menu-item"
        
        # 记录首页
        initial_url = page.url
        self.all_menus[initial_url] = "首页"
        visited_urls.add(initial_url)
        print(f"记录首页: {initial_url}")
        
        # 多次遍历以确保获取所有菜单
        for iteration in range(3):
            print(f"\n第 {iteration + 1} 轮遍历...")
            
            menu_items = page.locator(menu_items_selector).all()
            print(f"  找到 {len(menu_items)} 个菜单项")
            
            for idx, item in enumerate(menu_items):
                try:
                    # 重新获取元素
                    menu_items_fresh = page.locator(menu_items_selector).all()
                    if idx >= len(menu_items_fresh):
                        continue
                    
                    item = menu_items_fresh[idx]
                    
                    # 获取菜单文本
                    try:
                        text = item.inner_text().strip()
                        clean_text = ' '.join(text.split())
                        
                        # 跳过过长的文本（可能是整个菜单块）
                        if len(clean_text) > 50 or len(clean_text) == 0:
                            continue
                        
                        # 跳过纯符号
                        if clean_text in ['', '>', '<', '+', '-']:
                            continue
                        
                    except:
                        continue
                    
                    # 检查是否可见
                    if not item.is_visible():
                        continue
                    
                    # 记录点击前的URL
                    url_before = page.url
                    
                    # 尝试点击
                    try:
                        item.click(timeout=2000)
                        time.sleep(1)
                        
                        # 关闭可能的弹窗
                        try:
                            page.keyboard.press("Escape")
                            time.sleep(0.3)
                        except:
                            pass
                        
                    except Exception as e:
                        continue
                    
                    # 检查URL是否变化
                    url_after = page.url
                    
                    if url_after != url_before and url_after not in visited_urls:
                        # 发现新页面
                        self.all_menus[url_after] = clean_text
                        visited_urls.add(url_after)
                        print(f"  [{len(self.all_menus)}] {clean_text} -> {url_after}")
                    
                except Exception as e:
                    continue
            
            # 回到首页准备下一轮
            try:
                page.goto(initial_url, wait_until="domcontentloaded", timeout=5000)
                time.sleep(1)
            except:
                pass
        
        print(f"\n共发现 {len(self.all_menus)} 个唯一页面")
        return self.all_menus
    
    def analyze_and_report(self):
        """分析并生成报告"""
        print("\n" + "=" * 60)
        print("菜单分析报告")
        print("=" * 60)
        
        existing_menus = []
        missing_menus = []
        
        for url, name in sorted(self.all_menus.items(), key=lambda x: x[1]):
            has_screenshot = url in self.existing_urls
            
            menu_info = {
                'name': name,
                'url': url,
                'has_screenshot': has_screenshot
            }
            
            if has_screenshot:
                # 使用已有的名称
                menu_info['existing_name'] = self.existing_names.get(url, name)
                existing_menus.append(menu_info)
            else:
                missing_menus.append(menu_info)
        
        print(f"\n✅ 已有截图的菜单: {len(existing_menus)} 个")
        print("-" * 60)
        for idx, menu in enumerate(existing_menus, 1):
            print(f"{idx}. {menu.get('existing_name', menu['name'])}")
        
        print(f"\n" + "=" * 60)
        print(f"❌ 缺失截图的菜单: {len(missing_menus)} 个")
        print("=" * 60)
        for idx, menu in enumerate(missing_menus, 1):
            print(f"\n{idx}. {menu['name']}")
            print(f"   URL: {menu['url']}")
        
        # 保存结果
        result = {
            'total': len(self.all_menus),
            'existing': len(existing_menus),
            'missing': len(missing_menus),
            'existing_menus': existing_menus,
            'missing_menus': missing_menus
        }
        
        with open(ANALYSIS_RESULT, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 详细分析结果已保存到: {ANALYSIS_RESULT}")
        
        return result
    
    def run(self):
        """主函数"""
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                locale='zh-CN'
            )
            
            page = context.new_page()
            
            try:
                if not self.login(page):
                    print("登录失败")
                    return False
                
                # 遍历所有菜单
                self.traverse_all_clickable_menus(page)
                
                # 分析并生成报告
                result = self.analyze_and_report()
                
                print("\n" + "=" * 60)
                print("分析完成！")
                print(f"总菜单数: {result['total']}")
                print(f"已有截图: {result['existing']}")
                print(f"需要补充: {result['missing']}")
                print("=" * 60)
                
                return True
                
            except Exception as e:
                print(f"\n✗ 错误: {str(e)}")
                import traceback
                traceback.print_exc()
                return False
            finally:
                browser.close()

if __name__ == "__main__":
    analyzer = MenuAnalyzerV2()
    analyzer.run()
