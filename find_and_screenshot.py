#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通过菜单查找并截图
"""

import os
import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

LOGIN_URL = "https://xstest.axioxio.com/Account/login"
USERNAME = "13811458301"
PASSWORD = "4<z%0/RS"
SCREENSHOTS_DIR = "/workspace/screenshots_v2"
MENU_DATA_FILE = "/workspace/menu_structure_v2.json"

class MenuScreenshots:
    def __init__(self):
        self.screenshots_dir = Path(SCREENSHOTS_DIR)
        
        with open(MENU_DATA_FILE, 'r', encoding='utf-8') as f:
            self.menu_data = json.load(f)
        
        self.screenshot_count = 42
        
    def sanitize_filename(self, name):
        """清理文件名"""
        invalid_chars = '<>:"/\\|?*\n\r\t'
        for char in invalid_chars:
            name = name.replace(char, '_')
        return name.strip()[:100]
    
    def close_all_modals(self, page):
        """关闭所有弹窗"""
        try:
            if page.locator(".swal2-container").count() > 0:
                try:
                    page.keyboard.press("Escape")
                    time.sleep(0.3)
                except:
                    pass
        except:
            pass
    
    def take_screenshot(self, page, menu_path):
        """截图并保存"""
        self.screenshot_count += 1
        filename = f"{self.screenshot_count:03d}_{self.sanitize_filename(menu_path)}.png"
        filepath = self.screenshots_dir / filename
        
        try:
            time.sleep(1.5)
            page.screenshot(path=str(filepath), full_page=False)
            print(f"✓ 截图已保存: {filename}")
            return filename
        except Exception as e:
            print(f"✗ 截图失败: {str(e)}")
            return None
    
    def login(self, page):
        """登录系统"""
        print("正在登录...")
        page.goto(LOGIN_URL, wait_until="domcontentloaded")
        time.sleep(3)
        
        page.fill("#UserNameOrEmailAddress", USERNAME)
        page.fill("#Password", PASSWORD)
        time.sleep(1)
        page.click("button[type='submit']")
        time.sleep(5)
        
        if page.url != LOGIN_URL:
            print("✓ 登录成功！")
            self.close_all_modals(page)
            return True
        return False
    
    def find_and_click_menu(self, page, keywords):
        """查找并点击包含关键词的菜单"""
        try:
            # 等待菜单加载
            time.sleep(2)
            
            # 尝试多种菜单选择器
            menu_selectors = [
                "nav li",
                ".sidebar li",
                ".menu-item",
                "aside li"
            ]
            
            for selector in menu_selectors:
                menu_items = page.locator(selector).all()
                if len(menu_items) > 0:
                    for item in menu_items:
                        try:
                            text = item.inner_text().strip()
                            # 检查是否匹配任何关键词
                            if any(keyword in text for keyword in keywords):
                                print(f"  找到菜单: {text}")
                                # 尝试点击
                                if item.is_visible():
                                    item.click(timeout=3000)
                                    time.sleep(2)
                                    self.close_all_modals(page)
                                    time.sleep(1)
                                    return True, text
                        except:
                            continue
                    break
            
            return False, None
        except Exception as e:
            print(f"  查找菜单出错: {str(e)}")
            return False, None
    
    def explore_menu_tree(self, page):
        """探索菜单树结构"""
        print("\n开始探索菜单...")
        
        # 要寻找的功能
        targets = [
            {"keywords": ["租赁", "订单"], "name": "租赁-订单"},
            {"keywords": ["租赁", "产品"], "name": "租赁-产品"},
            {"keywords": ["小程序", "首页"], "name": "小程序-首页装修"},
            {"keywords": ["报表", "票务"], "name": "报表-票务核销报表"},
            {"keywords": ["报表", "教学"], "name": "报表-教学核销报表"},
            {"keywords": ["报表", "租赁"], "name": "报表-租赁核销报表"},
        ]
        
        new_items = []
        
        for target in targets:
            print(f"\n查找: {target['name']}")
            found, menu_text = self.find_and_click_menu(page, target['keywords'])
            
            if found:
                # 检查页面内容
                current_url = page.url
                print(f"  URL: {current_url}")
                
                # 检查是否是有效页面
                try:
                    page.wait_for_load_state("domcontentloaded", timeout=3000)
                    time.sleep(1)
                    
                    # 简单检查页面是否有内容
                    content = page.content()
                    if len(content) > 1000:  # 有实质内容
                        screenshot_file = self.take_screenshot(page, target['name'])
                        if screenshot_file:
                            new_items.append({
                                "path": target['name'],
                                "url": current_url,
                                "screenshot": screenshot_file,
                                "description": target['name']
                            })
                except:
                    pass
            else:
                print(f"  ✗ 未找到相关菜单")
        
        # 更新数据
        if new_items:
            self.menu_data.extend(new_items)
            with open(MENU_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.menu_data, f, ensure_ascii=False, indent=2)
            print(f"\n✓ 新增 {len(new_items)} 个截图")
        else:
            print("\n⚠️ 未找到新的有效页面")
        
        return len(new_items)
    
    def run(self):
        """主函数"""
        print("=" * 60)
        print("通过菜单查找并补充截图")
        print("=" * 60)
        
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
                
                count = self.explore_menu_tree(page)
                
                print("\n" + "=" * 60)
                print(f"任务完成！新增 {count} 个截图")
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
    scraper = MenuScreenshots()
    scraper.run()
