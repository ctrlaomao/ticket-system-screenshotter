#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第三方平台对接配置查看脚本
用途：登录票务系统，查找并截图美团、携程、抖音的配置页面
"""

import os
import time
import json
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

# 配置文件路径
CONFIG_FILE = "/workspace/config.json"
SCREENSHOTS_DIR = "/workspace/third_party_test_report/screenshots"
RESULT_FILE = "/workspace/third_party_test_report/test_result.json"

class ThirdPartyPlatformTester:
    def __init__(self):
        # 加载配置
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.login_url = self.config['login']['url']
        self.base_url = self.config['login']['base_url']
        self.username = self.config['login']['username']
        self.password = self.config['login']['password']
        
        # 截图目录
        self.screenshots_dir = Path(SCREENSHOTS_DIR)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        
        # 测试结果
        self.test_results = {
            "test_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tester": self.username,
            "system_url": self.base_url,
            "platforms": []
        }
        
        print(f"初始化完成")
        print(f"系统地址: {self.base_url}")
        print(f"用户名: {self.username}")
        print(f"截图保存目录: {self.screenshots_dir}")
    
    def login(self, page):
        """登录系统"""
        print("\n========== 登录系统 ==========")
        print(f"访问登录页面: {self.login_url}")
        
        page.goto(self.login_url, wait_until="domcontentloaded")
        time.sleep(2)
        
        # 选择简体中文（如果有语言选择）
        try:
            # 尝试查找语言选择器
            language_selectors = [
                "select[name='language']",
                ".language-selector",
                "#language"
            ]
            for selector in language_selectors:
                if page.locator(selector).count() > 0:
                    page.select_option(selector, "zh-CN")
                    print("✓ 已选择简体中文")
                    time.sleep(0.5)
                    break
        except Exception as e:
            print(f"  语言选择未找到，继续...")
        
        # 输入用户名
        try:
            username_input = page.locator("input[type='text']").first
            username_input.fill(self.username)
            print(f"✓ 已输入用户名: {self.username}")
        except Exception as e:
            print(f"✗ 输入用户名失败: {e}")
            return False
        
        # 输入密码
        try:
            password_input = page.locator("input[type='password']").first
            password_input.fill(self.password)
            print(f"✓ 已输入密码")
        except Exception as e:
            print(f"✗ 输入密码失败: {e}")
            return False
        
        time.sleep(1)
        
        # 点击登录按钮
        try:
            login_button = page.locator("button[type='submit']").first
            login_button.click()
            print("✓ 已点击登录按钮")
        except Exception as e:
            print(f"✗ 点击登录按钮失败: {e}")
            return False
        
        # 等待登录完成
        time.sleep(5)
        
        # 关闭可能的欢迎弹窗
        try:
            page.keyboard.press("Escape")
            time.sleep(0.5)
        except:
            pass
        
        # 验证登录
        if page.url != self.login_url:
            print(f"✓ 登录成功！当前页面: {page.url}")
            return True
        else:
            print(f"✗ 登录失败，仍在登录页面")
            return False
    
    def find_platform_config_pages(self, page):
        """查找三个平台的配置页面"""
        print("\n========== 查找配置页面 ==========")
        
        platforms_to_find = {
            "meituan": {"keywords": ["美团", "meituan"], "name": "美团"},
            "ctrip": {"keywords": ["携程", "ctrip", "xiecheng"], "name": "携程"},
            "douyin": {"keywords": ["抖音", "douyin", "tiktok"], "name": "抖音"}
        }
        
        found_configs = {}
        
        # 尝试在常见位置查找配置页面
        potential_menu_paths = [
            "系统设置",
            "系统管理",
            "第三方对接",
            "渠道管理",
            "平台管理",
            "分销管理",
            "对接配置",
            "设置"
        ]
        
        print("开始搜索菜单项...")
        
        # 获取所有菜单项
        menu_items = page.locator("nav li, .sidebar li, aside li, .menu-item, a[href]").all()
        print(f"找到 {len(menu_items)} 个可能的菜单项")
        
        # 遍历查找包含关键词的菜单
        for idx, item in enumerate(menu_items):
            try:
                text = item.inner_text().strip()
                clean_text = ' '.join(text.split()).lower()
                
                # 检查是否包含平台关键词
                for platform_id, platform_info in platforms_to_find.items():
                    if platform_id not in found_configs:
                        for keyword in platform_info['keywords']:
                            if keyword.lower() in clean_text:
                                print(f"  找到可能的{platform_info['name']}配置: {text}")
                                
                                # 尝试点击并截图
                                try:
                                    # 重新获取元素
                                    menu_items_fresh = page.locator("nav li, .sidebar li, aside li, .menu-item, a[href]").all()
                                    if idx < len(menu_items_fresh):
                                        menu_items_fresh[idx].click(timeout=3000)
                                        time.sleep(2)
                                        
                                        # 截图
                                        screenshot_path = self.take_screenshot(page, platform_info['name'])
                                        
                                        if screenshot_path:
                                            found_configs[platform_id] = {
                                                "name": platform_info['name'],
                                                "menu_text": text,
                                                "url": page.url,
                                                "screenshot": screenshot_path,
                                                "found": True
                                            }
                                            print(f"  ✓ {platform_info['name']}配置已截图")
                                            break
                                except Exception as e:
                                    print(f"  ✗ 点击菜单失败: {e}")
            except:
                continue
        
        # 补充未找到的平台
        for platform_id, platform_info in platforms_to_find.items():
            if platform_id not in found_configs:
                found_configs[platform_id] = {
                    "name": platform_info['name'],
                    "found": False,
                    "message": "未在系统中找到相关配置页面"
                }
                print(f"  ⚠ 未找到{platform_info['name']}配置页面")
        
        return found_configs
    
    def search_in_settings(self, page):
        """在系统设置中搜索第三方平台配置"""
        print("\n========== 在系统设置中搜索 ==========")
        
        # 尝试访问系统设置页面
        settings_urls = [
            f"{self.base_url}/SettingManagement",
            f"{self.base_url}/Settings",
            f"{self.base_url}/SystemSettings",
            f"{self.base_url}/Config"
        ]
        
        for url in settings_urls:
            try:
                print(f"尝试访问: {url}")
                page.goto(url, wait_until="domcontentloaded", timeout=10000)
                time.sleep(2)
                
                # 检查页面是否加载成功
                if "404" not in page.content() and "Not Found" not in page.content():
                    print(f"  ✓ 成功访问设置页面")
                    
                    # 在页面中搜索关键词
                    content = page.content().lower()
                    
                    platforms_found = []
                    if "美团" in content or "meituan" in content:
                        platforms_found.append("美团")
                    if "携程" in content or "ctrip" in content:
                        platforms_found.append("携程")
                    if "抖音" in content or "douyin" in content:
                        platforms_found.append("抖音")
                    
                    if platforms_found:
                        print(f"  在设置页面找到: {', '.join(platforms_found)}")
                        screenshot_path = self.take_screenshot(page, "系统设置_第三方平台")
                        return screenshot_path
            except Exception as e:
                print(f"  无法访问: {e}")
                continue
        
        return None
    
    def take_screenshot(self, page, name):
        """截取页面截图"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = self.screenshots_dir / filename
        
        try:
            # 等待页面稳定
            time.sleep(1)
            
            # 截图
            page.screenshot(path=str(filepath), full_page=True)
            print(f"    ✓ 截图已保存: {filename}")
            return filename
        except Exception as e:
            print(f"    ✗ 截图失败: {e}")
            return None
    
    def generate_manual_screenshots(self, page):
        """手动查找并截图三个平台配置"""
        print("\n========== 手动查找配置页面 ==========")
        print("提示：将访问常见的配置路径...")
        
        # 常见的第三方对接路径
        possible_paths = [
            "/ProductModule/Distributors",  # 分销商
            "/ProductModule/DistributorTickets",  # 分销商产品
            "/SettingManagement",  # 系统设置
            "/ThirdParty",  # 第三方
            "/Platform",  # 平台
            "/Channel",  # 渠道
            "/Integration"  # 集成
        ]
        
        results = []
        
        for path in possible_paths:
            try:
                url = f"{self.base_url}{path}"
                print(f"\n尝试访问: {url}")
                page.goto(url, wait_until="domcontentloaded", timeout=10000)
                time.sleep(2)
                
                # 检查页面内容
                content = page.content()
                page_text = page.locator("body").inner_text().lower()
                
                # 检查是否包含目标平台
                platforms_on_page = []
                if "美团" in page_text or "meituan" in page_text:
                    platforms_on_page.append("美团")
                if "携程" in page_text or "ctrip" in page_text or "xiecheng" in page_text:
                    platforms_on_page.append("携程")
                if "抖音" in page_text or "douyin" in page_text:
                    platforms_on_page.append("抖音")
                
                if platforms_on_page:
                    print(f"  ✓ 在此页面找到: {', '.join(platforms_on_page)}")
                    
                    # 截图
                    page_title = page.title() or path.split('/')[-1]
                    screenshot_name = f"配置页面_{page_title}"
                    screenshot_path = self.take_screenshot(page, screenshot_name)
                    
                    results.append({
                        "url": url,
                        "platforms": platforms_on_page,
                        "screenshot": screenshot_path
                    })
                else:
                    print(f"  未找到目标平台配置")
                    
            except Exception as e:
                print(f"  无法访问: {e}")
        
        return results
    
    def save_results(self, platform_configs, manual_results):
        """保存测试结果"""
        print("\n========== 保存测试结果 ==========")
        
        # 整理平台配置信息
        for platform_id, config in platform_configs.items():
            self.test_results["platforms"].append(config)
        
        # 添加手动查找结果
        if manual_results:
            self.test_results["manual_search_results"] = manual_results
        
        # 保存到JSON文件
        with open(RESULT_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 测试结果已保存到: {RESULT_FILE}")
        
        return self.test_results
    
    def run(self):
        """执行测试流程"""
        print("\n" + "="*50)
        print("第三方平台对接配置查看测试")
        print("="*50)
        
        with sync_playwright() as p:
            # 启动浏览器
            browser = p.chromium.launch(headless=True)  # headless模式
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                locale='zh-CN'
            )
            page = context.new_page()
            
            try:
                # 登录
                if not self.login(page):
                    print("\n✗ 登录失败，测试终止")
                    return False
                
                # 查找平台配置
                platform_configs = self.find_platform_config_pages(page)
                
                # 手动搜索常见路径
                manual_results = self.generate_manual_screenshots(page)
                
                # 保存结果
                self.save_results(platform_configs, manual_results)
                
                print("\n" + "="*50)
                print("测试完成！")
                print("="*50)
                print(f"截图保存位置: {self.screenshots_dir}")
                print(f"测试结果文件: {RESULT_FILE}")
                
                return True
                
            except KeyboardInterrupt:
                print("\n用户中断测试")
                return False
            except Exception as e:
                print(f"\n✗ 测试过程出错: {e}")
                import traceback
                traceback.print_exc()
                return False
            finally:
                browser.close()

if __name__ == "__main__":
    tester = ThirdPartyPlatformTester()
    tester.run()
