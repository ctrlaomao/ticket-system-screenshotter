#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
票务系统自动截图脚本
"""

import os
import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# 配置信息
LOGIN_URL = "https://xstest.axioxio.com/Account/login"
USERNAME = "13811458301"
PASSWORD = "4<z%0/RS"
SCREENSHOTS_DIR = "/workspace/screenshots"
MENU_DATA_FILE = "/workspace/menu_structure.json"

class TicketingSystemScreenshot:
    def __init__(self):
        self.screenshots_dir = Path(SCREENSHOTS_DIR)
        self.screenshots_dir.mkdir(exist_ok=True)
        self.menu_structure = []
        self.screenshot_count = 0
        
    def sanitize_filename(self, name):
        """清理文件名，移除非法字符"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        return name.strip()
    
    def wait_for_page_load(self, page, timeout=3000):
        """等待页面加载"""
        try:
            page.wait_for_load_state("networkidle", timeout=timeout)
        except:
            pass
        time.sleep(1)  # 额外等待确保内容渲染完成
    
    def close_modal(self, page):
        """关闭弹窗"""
        try:
            # 尝试关闭swal2弹窗
            close_selectors = [
                ".swal2-close",
                ".swal2-confirm",
                ".swal2-cancel",
                "button:has-text('确定')",
                "button:has-text('关闭')",
                "button:has-text('取消')",
            ]
            
            for selector in close_selectors:
                if page.locator(selector).count() > 0:
                    try:
                        page.locator(selector).first.click(timeout=1000)
                        time.sleep(0.5)
                        print("  ✓ 已关闭弹窗")
                        return True
                    except:
                        pass
        except:
            pass
        return False
    
    def take_screenshot(self, page, menu_path, description=""):
        """截图并保存"""
        self.screenshot_count += 1
        filename = f"{self.screenshot_count:03d}_{self.sanitize_filename(menu_path)}.png"
        filepath = self.screenshots_dir / filename
        
        try:
            # 截取右侧内容区域（如果可能的话全屏截图）
            page.screenshot(path=str(filepath), full_page=True)
            print(f"✓ 截图已保存: {filename}")
            return str(filepath)
        except Exception as e:
            print(f"✗ 截图失败 {menu_path}: {str(e)}")
            return None
    
    def login(self, page):
        """登录系统"""
        print("正在访问登录页面...")
        page.goto(LOGIN_URL, wait_until="networkidle")
        time.sleep(2)
        
        # 选择简体中文
        print("选择简体中文...")
        try:
            # 尝试多种方式找到语言选择器
            language_selectors = [
                "select[name='language']",
                "select#language",
                ".language-selector",
                "select",
            ]
            
            for selector in language_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.select_option(selector, label="简体中文")
                        print("✓ 已选择简体中文")
                        time.sleep(1)
                        break
                except:
                    continue
        except Exception as e:
            print(f"注意: 无法自动选择语言: {str(e)}")
        
        # 输入用户名
        print("输入登录信息...")
        username_selectors = [
            "input[name='username']",
            "input[type='text']",
            "input#username",
            "input[placeholder*='用户名']",
            "input[placeholder*='手机']",
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
            "input[name='password']",
            "input[type='password']",
            "input#password",
        ]
        
        for selector in password_selectors:
            try:
                if page.locator(selector).count() > 0:
                    page.fill(selector, PASSWORD)
                    print("✓ 已输入密码")
                    break
            except:
                continue
        
        # 点击登录按钮
        login_button_selectors = [
            "button[type='submit']",
            "button:has-text('登录')",
            "button:has-text('登錄')",
            "input[type='submit']",
            ".login-button",
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
        
        # 检查是否登录成功（检查URL变化或者左侧菜单是否出现）
        if page.url != LOGIN_URL:
            print("✓ 登录成功！")
            return True
        else:
            print("✗ 登录可能失败，请检查")
            return False
    
    def find_menu_items(self, page):
        """查找左侧菜单项"""
        menu_selectors = [
            ".sidebar .menu-item",
            ".side-menu li",
            ".el-menu-item",
            ".ant-menu-item",
            "aside li",
            ".sidebar li",
            "nav li",
        ]
        
        for selector in menu_selectors:
            items = page.locator(selector).all()
            if len(items) > 0:
                print(f"✓ 找到 {len(items)} 个菜单项 (使用选择器: {selector})")
                return items, selector
        
        # 如果没找到，尝试更通用的方式
        print("尝试通用方式查找菜单...")
        items = page.locator("aside li, .sidebar li, nav li").all()
        return items, "aside li, .sidebar li, nav li"
    
    def extract_menu_text(self, element):
        """提取菜单文本"""
        try:
            text = element.inner_text().strip()
            return text if text else None
        except:
            return None
    
    def traverse_menu(self, page):
        """遍历所有菜单并截图"""
        print("\n开始遍历菜单...")
        time.sleep(3)  # 等待页面完全加载
        
        # 截取首页
        print("\n截取首页...")
        self.take_screenshot(page, "首页_默认页面")
        self.menu_structure.append({
            "path": "首页",
            "screenshot": f"{self.screenshot_count:03d}_首页_默认页面.png",
            "description": "系统首页"
        })
        
        # 尝试多种方式查找菜单
        menu_items, selector = self.find_menu_items(page)
        
        if not menu_items or len(menu_items) == 0:
            print("✗ 未找到菜单项，尝试手动分析页面结构...")
            page.screenshot(path=str(self.screenshots_dir / "debug_page_structure.png"))
            return
        
        print(f"\n共找到 {len(menu_items)} 个可能的菜单项")
        
        # 遍历每个菜单项
        visited_urls = set()
        current_url = page.url
        visited_urls.add(current_url)
        
        for i, item in enumerate(menu_items):
            try:
                # 重新获取菜单项（避免stale element）
                menu_items_fresh, _ = self.find_menu_items(page)
                if i >= len(menu_items_fresh):
                    continue
                    
                item = menu_items_fresh[i]
                menu_text = self.extract_menu_text(item)
                
                if not menu_text or len(menu_text) == 0:
                    continue
                
                print(f"\n[{i+1}/{len(menu_items)}] 处理菜单: {menu_text}")
                
                # 检查是否可点击
                if not item.is_visible():
                    print(f"  跳过：菜单项不可见")
                    continue
                
                # 记录点击前的URL
                url_before = page.url
                
                # 点击菜单项
                try:
                    item.click(timeout=5000)
                    print(f"  ✓ 已点击")
                except Exception as e:
                    print(f"  ✗ 点击失败: {str(e)}")
                    continue
                
                # 等待页面变化
                time.sleep(2)
                self.wait_for_page_load(page, timeout=3000)
                
                # 检查URL或内容是否变化
                url_after = page.url
                
                if url_after != url_before or url_after not in visited_urls:
                    # 页面有变化，截图
                    screenshot_path = self.take_screenshot(page, menu_text)
                    if screenshot_path:
                        self.menu_structure.append({
                            "path": menu_text,
                            "url": url_after,
                            "screenshot": os.path.basename(screenshot_path),
                            "description": menu_text
                        })
                        visited_urls.add(url_after)
                else:
                    print(f"  - 页面无变化，跳过截图")
                
                # 短暂等待
                time.sleep(1)
                
            except Exception as e:
                print(f"  ✗ 处理失败: {str(e)}")
                continue
        
        print(f"\n✓ 菜单遍历完成！共生成 {self.screenshot_count} 张截图")
    
    def save_menu_structure(self):
        """保存菜单结构到JSON文件"""
        with open(MENU_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.menu_structure, f, ensure_ascii=False, indent=2)
        print(f"✓ 菜单结构已保存到: {MENU_DATA_FILE}")
    
    def run(self):
        """主运行函数"""
        print("=" * 60)
        print("票务系统自动截图工具")
        print("=" * 60)
        
        with sync_playwright() as p:
            # 启动浏览器（使用无头模式）
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
                # 登录
                if not self.login(page):
                    print("登录失败，退出程序")
                    return False
                
                # 遍历菜单并截图
                self.traverse_menu(page)
                
                # 保存菜单结构
                self.save_menu_structure()
                
                print("\n" + "=" * 60)
                print("任务完成！")
                print(f"截图保存目录: {self.screenshots_dir}")
                print(f"菜单结构文件: {MENU_DATA_FILE}")
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
    scraper = TicketingSystemScreenshot()
    scraper.run()
