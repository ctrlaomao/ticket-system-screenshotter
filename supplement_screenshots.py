#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补充缺失功能的截图
"""

import os
import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

# 配置信息
LOGIN_URL = "https://xstest.axioxio.com/Account/login"
USERNAME = "13811458301"
PASSWORD = "4<z%0/RS"
SCREENSHOTS_DIR = "/workspace/screenshots_v2"
MENU_DATA_FILE = "/workspace/menu_structure_v2.json"

class SupplementScreenshots:
    def __init__(self):
        self.screenshots_dir = Path(SCREENSHOTS_DIR)
        self.screenshots_dir.mkdir(exist_ok=True)
        
        # 加载现有数据
        with open(MENU_DATA_FILE, 'r', encoding='utf-8') as f:
            self.menu_data = json.load(f)
        
        # 获取当前最大编号
        self.screenshot_count = 0
        for item in self.menu_data:
            screenshot = item['screenshot']
            # 提取编号 例如 "001_xxx.png" -> 1
            try:
                num = int(screenshot.split('_')[0])
                if num > self.screenshot_count:
                    self.screenshot_count = num
            except:
                pass
        
        print(f"当前截图编号从 {self.screenshot_count} 开始")
        
    def sanitize_filename(self, name):
        """清理文件名"""
        invalid_chars = '<>:"/\\|?*\n\r\t'
        for char in invalid_chars:
            name = name.replace(char, '_')
        return name.strip()[:100]
    
    def wait_for_page_load(self, page, timeout=2000):
        """等待页面加载"""
        try:
            page.wait_for_load_state("domcontentloaded", timeout=timeout)
        except:
            pass
        time.sleep(1)
    
    def close_all_modals(self, page):
        """关闭所有弹窗"""
        try:
            if page.locator(".swal2-container").count() > 0:
                close_selectors = [".swal2-close", ".swal2-confirm", "button.swal2-confirm"]
                for selector in close_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.locator(selector).first.click(timeout=1000, force=True)
                            time.sleep(0.3)
                            return True
                    except:
                        pass
                try:
                    page.keyboard.press("Escape")
                    time.sleep(0.3)
                    return True
                except:
                    pass
        except:
            pass
        return False
    
    def take_screenshot(self, page, menu_path):
        """截图并保存"""
        self.screenshot_count += 1
        filename = f"{self.screenshot_count:03d}_{self.sanitize_filename(menu_path)}.png"
        filepath = self.screenshots_dir / filename
        
        try:
            time.sleep(1)
            page.screenshot(path=str(filepath), full_page=False)
            print(f"✓ 截图已保存: {filename}")
            return filename
        except Exception as e:
            print(f"✗ 截图失败 {menu_path}: {str(e)}")
            return None
    
    def login(self, page):
        """登录系统"""
        print("正在访问登录页面...")
        page.goto(LOGIN_URL, wait_until="domcontentloaded")
        time.sleep(3)
        
        # 输入用户名
        username_selectors = [
            "#UserNameOrEmailAddress",
            "input[name='UserNameOrEmailAddress']",
            "input[name='username']",
            "input[type='text']",
        ]
        
        for selector in username_selectors:
            try:
                if page.locator(selector).count() > 0:
                    page.fill(selector, USERNAME)
                    print("✓ 已输入用户名")
                    break
            except:
                continue
        
        # 输入密码
        password_selectors = [
            "#Password",
            "input[name='Password']",
            "input[name='password']",
            "input[type='password']",
        ]
        
        for selector in password_selectors:
            try:
                if page.locator(selector).count() > 0:
                    page.fill(selector, PASSWORD)
                    print("✓ 已输入密码")
                    break
            except:
                continue
        
        time.sleep(1)
        
        # 点击登录按钮
        login_button_selectors = [
            "button[type='submit']",
            "button:has-text('登录')",
            ".btn-primary",
        ]
        
        for selector in login_button_selectors:
            try:
                if page.locator(selector).count() > 0:
                    page.click(selector)
                    print("✓ 已点击登录按钮")
                    break
            except:
                continue
        
        # 等待登录完成
        print("等待登录完成...")
        time.sleep(5)
        
        if page.url != LOGIN_URL:
            print("✓ 登录成功！")
            self.close_all_modals(page)
            return True
        else:
            print("✗ 登录失败")
            return False
    
    def supplement_screenshots(self, page):
        """补充缺失的截图"""
        print("\n开始补充截图...")
        
        # 需要补充的功能页面
        supplement_pages = [
            # 票务-产品（已有，但重新确认）
            {"url": "https://xstest.axioxio.com/ProductModule/Products", "name": "票务-产品-产品管理"},
            {"url": "https://xstest.axioxio.com/ProductModule/Categories", "name": "票务-产品-产品分类"},
            
            # 租赁-订单
            {"url": "https://xstest.axioxio.com/DepositModule/DepositOrders", "name": "租赁-订单"},
            
            # 租赁-产品
            {"url": "https://xstest.axioxio.com/DepositModule/DepositItems", "name": "租赁-产品-产品管理"},
            {"url": "https://xstest.axioxio.com/DepositModule/DepositItemCategories", "name": "租赁-产品-产品分类"},
            
            # 小程序
            {"url": "https://xstest.axioxio.com/MiniProgram/HomeDecoration", "name": "小程序-首页装修"},
            {"url": "https://xstest.axioxio.com/MiniProgramModule/HomeDecoration", "name": "小程序-首页装修-备用"},
            
            # 报表
            {"url": "https://xstest.axioxio.com/ReportModule/TicketReport", "name": "报表-票务核销报表"},
            {"url": "https://xstest.axioxio.com/ReportModule/TeachingReport", "name": "报表-教学核销报表"},
            {"url": "https://xstest.axioxio.com/ReportModule/DepositReport", "name": "报表-租赁核销报表"},
        ]
        
        new_items = []
        
        for page_info in supplement_pages:
            url = page_info['url']
            name = page_info['name']
            
            print(f"\n访问: {name}")
            print(f"  URL: {url}")
            
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=10000)
                time.sleep(2)
                self.close_all_modals(page)
                time.sleep(1)
                
                # 检查页面是否有效（不是404）
                page_content = page.content().lower()
                if '404' in page_content or 'not found' in page_content:
                    print(f"  ⚠️ 页面可能是404，跳过")
                    continue
                
                screenshot_file = self.take_screenshot(page, name)
                if screenshot_file:
                    new_items.append({
                        "path": name,
                        "url": url,
                        "screenshot": screenshot_file,
                        "description": name
                    })
                
            except Exception as e:
                print(f"  ✗ 访问失败: {str(e)}")
                continue
        
        # 合并到现有数据
        self.menu_data.extend(new_items)
        
        # 保存更新后的数据
        with open(MENU_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.menu_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 补充完成！新增 {len(new_items)} 个截图")
        print(f"✓ 总计 {len(self.menu_data)} 个功能截图")
        
        return len(new_items)
    
    def run(self):
        """主运行函数"""
        print("=" * 60)
        print("补充功能截图")
        print("=" * 60)
        
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
            )
            
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                locale='zh-CN',
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            
            page = context.new_page()
            
            try:
                # 登录
                if not self.login(page):
                    print("登录失败，退出程序")
                    return False
                
                # 补充截图
                count = self.supplement_screenshots(page)
                
                print("\n" + "=" * 60)
                print("任务完成！")
                print(f"新增截图: {count} 个")
                print("=" * 60)
                
                return True
                
            except Exception as e:
                print(f"\n✗ 发生错误: {str(e)}")
                import traceback
                traceback.print_exc()
                return False
            finally:
                browser.close()

if __name__ == "__main__":
    scraper = SupplementScreenshots()
    scraper.run()
