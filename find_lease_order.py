#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门查找租赁-订单功能
"""

import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

LOGIN_URL = "https://xstest.axioxio.com/Account/login"
USERNAME = "13811458301"
PASSWORD = "4<z%0/RS"
SCREENSHOTS_DIR = "/workspace/screenshots_v2"
MENU_DATA_FILE = "/workspace/menu_structure_v2.json"

class LeaseOrderFinder:
    def __init__(self):
        self.screenshots_dir = Path(SCREENSHOTS_DIR)
        
        with open(MENU_DATA_FILE, 'r', encoding='utf-8') as f:
            self.menu_data = json.load(f)
        
        self.screenshot_count = 50  # 当前最大编号
        
    def sanitize_filename(self, name):
        """清理文件名"""
        invalid_chars = '<>:"/\\|?*\n\r\t'
        for char in invalid_chars:
            name = name.replace(char, '_')
        return name.strip()[:100]
    
    def close_modal(self, page):
        """关闭弹窗"""
        try:
            page.keyboard.press("Escape")
            time.sleep(0.3)
        except:
            pass
    
    def take_screenshot(self, page, name):
        """截图"""
        self.screenshot_count += 1
        filename = f"{self.screenshot_count:03d}_{self.sanitize_filename(name)}.png"
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
        """登录"""
        print("正在登录...")
        page.goto(LOGIN_URL, wait_until="domcontentloaded")
        time.sleep(3)
        
        username_selectors = ["#UserNameOrEmailAddress", "input[name='UserNameOrEmailAddress']", "input[type='text']"]
        for selector in username_selectors:
            try:
                if page.locator(selector).count() > 0:
                    page.fill(selector, USERNAME)
                    print("✓ 已输入用户名")
                    break
            except:
                continue
        
        password_selectors = ["#Password", "input[name='Password']", "input[type='password']"]
        for selector in password_selectors:
            try:
                if page.locator(selector).count() > 0:
                    page.fill(selector, PASSWORD)
                    print("✓ 已输入密码")
                    break
            except:
                continue
        
        time.sleep(1)
        
        login_selectors = ["button[type='submit']", "button:has-text('登录')", ".btn-primary"]
        for selector in login_selectors:
            try:
                if page.locator(selector).count() > 0:
                    page.click(selector)
                    print("✓ 已点击登录按钮")
                    break
            except:
                continue
        
        time.sleep(5)
        self.close_modal(page)
        
        if page.url != LOGIN_URL:
            print("✓ 登录成功！\n")
            return True
        return False
    
    def find_lease_order_menu(self, page):
        """查找租赁订单菜单"""
        print("开始查找租赁订单菜单...")
        time.sleep(3)
        
        # 先尝试点击"租赁"主菜单
        print("\n步骤1: 查找并点击'租赁'菜单...")
        lease_found = False
        
        # 获取所有可能的菜单元素
        menu_selectors = ["nav li", ".sidebar li", "aside li", ".menu-item"]
        
        for selector in menu_selectors:
            menu_items = page.locator(selector).all()
            if len(menu_items) > 0:
                for item in menu_items:
                    try:
                        text = item.inner_text().strip()
                        # 查找包含"租赁"的菜单
                        if text == "租赁" or "租赁" in text[:10]:  # 只匹配开头的租赁
                            print(f"  找到菜单: {text}")
                            if item.is_visible():
                                item.click(timeout=3000)
                                time.sleep(2)
                                self.close_modal(page)
                                lease_found = True
                                print("  ✓ 已点击租赁菜单")
                                break
                    except:
                        continue
                if lease_found:
                    break
        
        if not lease_found:
            print("  ✗ 未找到租赁主菜单")
            return None
        
        # 查找租赁下的所有链接
        print("\n步骤2: 查找租赁模块下的所有子菜单...")
        time.sleep(2)
        
        all_links = page.locator("nav a, .sidebar a, aside a").all()
        lease_links = []
        
        for link in all_links:
            try:
                text = link.inner_text().strip()
                href = link.get_attribute('href')
                
                if href and href.startswith('http'):
                    # 查找包含"订单"的链接
                    if "订单" in text:
                        lease_links.append({
                            'text': text,
                            'href': href
                        })
                        print(f"  找到: {text} -> {href}")
            except:
                continue
        
        # 如果没找到，尝试直接搜索所有包含"订单"的链接
        if not lease_links:
            print("\n步骤3: 在所有菜单中搜索包含'订单'的链接...")
            all_menu_items = page.locator("nav a, .sidebar a, aside a").all()
            
            for link in all_menu_items:
                try:
                    text = link.inner_text().strip()
                    href = link.get_attribute('href')
                    
                    if href and href.startswith('http') and "订单" in text:
                        # 检查URL中是否包含租赁相关的关键词
                        if any(keyword in href.lower() for keyword in ['lease', 'deposit', 'rental']):
                            lease_links.append({
                                'text': text,
                                'href': href
                            })
                            print(f"  找到: {text} -> {href}")
                except:
                    continue
        
        # 尝试访问找到的链接
        if lease_links:
            print(f"\n步骤4: 找到 {len(lease_links)} 个可能的链接，尝试访问...")
            
            for link_info in lease_links:
                text = link_info['text']
                href = link_info['href']
                
                print(f"\n尝试访问: {text}")
                print(f"  URL: {href}")
                
                try:
                    page.goto(href, wait_until="domcontentloaded", timeout=10000)
                    time.sleep(2)
                    self.close_modal(page)
                    time.sleep(1)
                    
                    # 检查页面是否有效
                    content = page.content().lower()
                    if '404' not in content and 'not found' not in content:
                        # 找到有效页面，截图
                        screenshot_file = self.take_screenshot(page, "租赁-订单")
                        
                        if screenshot_file:
                            # 更新数据
                            self.menu_data.append({
                                "path": "租赁-订单",
                                "url": href,
                                "screenshot": screenshot_file,
                                "description": "租赁-订单"
                            })
                            
                            with open(MENU_DATA_FILE, 'w', encoding='utf-8') as f:
                                json.dump(self.menu_data, f, ensure_ascii=False, indent=2)
                            
                            print(f"\n✓ 成功找到租赁-订单功能！")
                            print(f"  URL: {href}")
                            return href
                    else:
                        print("  ✗ 页面返回404")
                        
                except Exception as e:
                    print(f"  ✗ 访问失败: {str(e)}")
                    continue
        
        print("\n✗ 未能找到租赁-订单功能")
        return None
    
    def run(self):
        """主函数"""
        print("=" * 60)
        print("查找租赁-订单功能")
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
                
                result = self.find_lease_order_menu(page)
                
                print("\n" + "=" * 60)
                if result:
                    print("任务完成！成功找到租赁-订单")
                else:
                    print("任务完成！但未找到租赁-订单功能")
                    print("可能该功能在当前账号权限下不可访问")
                print("=" * 60)
                
                return result is not None
                
            except Exception as e:
                print(f"\n✗ 错误: {str(e)}")
                import traceback
                traceback.print_exc()
                return False
            finally:
                browser.close()

if __name__ == "__main__":
    finder = LeaseOrderFinder()
    finder.run()
