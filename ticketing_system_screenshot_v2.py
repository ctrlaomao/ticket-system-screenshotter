#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
票务系统自动截图脚本 V2 - 改进版
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
SCREENSHOTS_DIR = "/workspace/screenshots_v2"
MENU_DATA_FILE = "/workspace/menu_structure_v2.json"

class TicketingSystemScreenshot:
    def __init__(self):
        self.screenshots_dir = Path(SCREENSHOTS_DIR)
        self.screenshots_dir.mkdir(exist_ok=True)
        self.menu_structure = []
        self.screenshot_count = 0
        
    def sanitize_filename(self, name):
        """清理文件名，移除非法字符"""
        invalid_chars = '<>:"/\\|?*\n\r\t'
        for char in invalid_chars:
            name = name.replace(char, '_')
        # 限制文件名长度
        name = name.strip()[:100]
        return name if name else "unnamed"
    
    def wait_for_page_load(self, page, timeout=2000):
        """等待页面加载"""
        try:
            page.wait_for_load_state("domcontentloaded", timeout=timeout)
        except:
            pass
        time.sleep(0.5)
    
    def close_all_modals(self, page):
        """关闭所有弹窗"""
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                # 检查是否有swal2弹窗
                if page.locator(".swal2-container").count() > 0:
                    # 尝试多种关闭方式
                    close_selectors = [
                        ".swal2-close",
                        ".swal2-confirm",
                        "button.swal2-confirm",
                        "button.swal2-cancel",
                    ]
                    
                    for selector in close_selectors:
                        try:
                            if page.locator(selector).count() > 0:
                                page.locator(selector).first.click(timeout=1000, force=True)
                                time.sleep(0.3)
                                print("  ✓ 已关闭弹窗")
                                return True
                        except:
                            pass
                    
                    # 如果还有弹窗，按ESC键
                    try:
                        page.keyboard.press("Escape")
                        time.sleep(0.3)
                        print("  ✓ 按ESC关闭弹窗")
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
            # 等待内容加载
            time.sleep(1)
            # 截取全屏
            page.screenshot(path=str(filepath), full_page=False)
            print(f"✓ 截图已保存: {filename}")
            return str(filepath)
        except Exception as e:
            print(f"✗ 截图失败 {menu_path}: {str(e)}")
            return None
    
    def login(self, page):
        """登录系统"""
        print("正在访问登录页面...")
        page.goto(LOGIN_URL, wait_until="domcontentloaded")
        time.sleep(3)
        
        # 首先查找并选择简体中文
        print("查找语言选择器...")
        try:
            # 尝试多种选择器查找语言下拉框
            language_selectors = [
                "select",
                "#Language",
                "[name='Language']",
                ".language-select",
                "select.form-control",
            ]
            
            language_selected = False
            for selector in language_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        print(f"  找到语言选择器: {selector}")
                        # 尝试通过value、label或index选择
                        try:
                            page.select_option(selector, label="简体中文")
                            print("✓ 已通过label选择简体中文")
                            language_selected = True
                            break
                        except:
                            pass
                        
                        try:
                            page.select_option(selector, value="zh-Hans")
                            print("✓ 已通过value选择简体中文")
                            language_selected = True
                            break
                        except:
                            pass
                        
                        try:
                            page.select_option(selector, value="zh-CN")
                            print("✓ 已通过value选择简体中文")
                            language_selected = True
                            break
                        except:
                            pass
                except Exception as e:
                    continue
            
            if language_selected:
                time.sleep(2)
                # 等待页面刷新
                page.wait_for_load_state("domcontentloaded")
                time.sleep(1)
            else:
                print("注意: 未找到语言选择器，继续登录流程")
                
        except Exception as e:
            print(f"语言选择过程出错: {str(e)}")
        
        # 输入用户名
        print("输入登录信息...")
        username_selectors = [
            "#UserNameOrEmailAddress",
            "input[name='UserNameOrEmailAddress']",
            "input[name='username']",
            "input[type='text']",
            "#username",
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
            "button:has-text('登錄')",
            "button:has-text('Login')",
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
        
        # 检查是否登录成功
        if page.url != LOGIN_URL:
            print("✓ 登录成功！")
            # 关闭可能出现的欢迎弹窗
            self.close_all_modals(page)
            return True
        else:
            print("✗ 登录可能失败，请检查")
            page.screenshot(path=str(self.screenshots_dir / "login_failed.png"))
            return False
    
    def click_menu_by_url(self, page, target_urls):
        """通过直接访问URL的方式进行截图"""
        print("\n使用URL直接访问方式补充截图...")
        
        for url_info in target_urls:
            try:
                url = url_info['url']
                name = url_info['name']
                print(f"\n访问: {name}")
                
                page.goto(url, wait_until="domcontentloaded")
                time.sleep(2)
                self.close_all_modals(page)
                time.sleep(1)
                
                screenshot_path = self.take_screenshot(page, name)
                if screenshot_path:
                    self.menu_structure.append({
                        "path": name,
                        "url": url,
                        "screenshot": os.path.basename(screenshot_path),
                        "description": name
                    })
                
            except Exception as e:
                print(f"  ✗ 访问失败: {str(e)}")
                continue
    
    def traverse_menu_improved(self, page):
        """改进的菜单遍历方法 - 通过直接访问已知的URL"""
        print("\n开始遍历系统功能...")
        time.sleep(2)
        
        # 截取首页
        print("\n截取首页...")
        self.take_screenshot(page, "首页_默认页面")
        self.menu_structure.append({
            "path": "首页",
            "screenshot": f"{self.screenshot_count:03d}_首页_默认页面.png",
            "description": "系统首页"
        })
        
        # 基于已知的系统结构，直接访问各个功能页面
        target_pages = [
            # 工作台相关
            {"url": "https://xstest.axioxio.com/OrderModule/CheckOut", "name": "工作台-收银"},
            {"url": "https://xstest.axioxio.com/OrderModule/CheckOut/BindCard", "name": "工作台-发卡"},
            {"url": "https://xstest.axioxio.com/OrderModule/CheckOut/Return", "name": "工作台-还卡"},
            
            # 订单管理
            {"url": "https://xstest.axioxio.com/OrderModule/Orders", "name": "订单管理-订单列表"},
            {"url": "https://xstest.axioxio.com/OrderModule/OrderTickets", "name": "订单管理-票务管理"},
            {"url": "https://xstest.axioxio.com/OrderModule/ReservationOrders", "name": "订单管理-预约订单"},
            {"url": "https://xstest.axioxio.com/OrderModule/DepositOrders", "name": "订单管理-寄存订单"},
            {"url": "https://xstest.axioxio.com/OrderModule/TeachingOrders", "name": "订单管理-教学订单"},
            {"url": "https://xstest.axioxio.com/OrderModule/TeamOrders", "name": "订单管理-团队订单"},
            
            # 票务管理
            {"url": "https://xstest.axioxio.com/ProductModule/ETicketItems", "name": "票务管理-电子券列表"},
            {"url": "https://xstest.axioxio.com/ProductModule/ETickets", "name": "票务管理-电子票初始化"},
            {"url": "https://xstest.axioxio.com/ProductModule/ETicketTemplates", "name": "票务管理-纸制票模板"},
            
            # 通行管理
            {"url": "https://xstest.axioxio.com/OrderModule/FaceImages", "name": "通行管理-人脸库"},
            {"url": "https://xstest.axioxio.com/OrderModule/Gates", "name": "通行管理-闸机配置"},
            {"url": "https://xstest.axioxio.com/OrderModule/Cards", "name": "通行管理-卡片管理"},
            {"url": "https://xstest.axioxio.com/OrderModule/Passages", "name": "通行管理-通行记录"},
            {"url": "https://xstest.axioxio.com/OrderModule/PassageRules", "name": "通行管理-通行规则"},
            
            # 产品控制面板
            {"url": "https://xstest.axioxio.com/ProductModule/Products", "name": "控制面板-产品管理"},
            {"url": "https://xstest.axioxio.com/ProductModule/Categories", "name": "控制面板-产品分类"},
            {"url": "https://xstest.axioxio.com/ProductModule/Holidays", "name": "控制面板-节假日设置"},
            
            # 教练管理
            {"url": "https://xstest.axioxio.com/TeachingModule/Coaches", "name": "控制面板-教练管理"},
            {"url": "https://xstest.axioxio.com/TeachingModule/Comments", "name": "控制面板-教练评论"},
            {"url": "https://xstest.axioxio.com/TeachingModule/Schedules", "name": "控制面板-排班管理"},
            {"url": "https://xstest.axioxio.com/TeachingModule/SportLevels", "name": "控制面板-运动级别"},
            
            # 租赁管理
            {"url": "https://xstest.axioxio.com/DepositModule/DepositItems", "name": "控制面板-租赁物管理"},
            {"url": "https://xstest.axioxio.com/DepositModule/DepositItemCategories", "name": "控制面板-租赁物分类"},
            
            # 分销管理
            {"url": "https://xstest.axioxio.com/DistributionModule/Distributors", "name": "控制面板-分销商管理"},
            {"url": "https://xstest.axioxio.com/DistributionModule/DistributionOrders", "name": "控制面板-分销订单"},
            
            # 报表管理
            {"url": "https://xstest.axioxio.com/ReportModule/TicketReport", "name": "报表管理-票务核销报表"},
            {"url": "https://xstest.axioxio.com/ReportModule/TeachingReport", "name": "报表管理-教学核销报表"},
            {"url": "https://xstest.axioxio.com/ReportModule/TeachingDashboard", "name": "报表管理-教学数据看板"},
            {"url": "https://xstest.axioxio.com/ReportModule/DepositReport", "name": "报表管理-租赁核销报表"},
            {"url": "https://xstest.axioxio.com/ReportModule/DepositItemReport", "name": "报表管理-租赁物明细报表"},
            
            # 系统管理
            {"url": "https://xstest.axioxio.com/FileManagement", "name": "系统管理-文件管理"},
            {"url": "https://xstest.axioxio.com/Identity/OrganizationUnits", "name": "系统管理-组织机构"},
            {"url": "https://xstest.axioxio.com/Identity/Roles", "name": "系统管理-角色管理"},
            {"url": "https://xstest.axioxio.com/Identity/Users", "name": "系统管理-用户管理"},
            {"url": "https://xstest.axioxio.com/AuditLogging/AuditLogs", "name": "系统管理-审计日志"},
            {"url": "https://xstest.axioxio.com/Identity/SecurityLogs", "name": "系统管理-安全日志"},
            {"url": "https://xstest.axioxio.com/TextTemplateManagement/TextTemplates", "name": "系统管理-文本模板"},
            {"url": "https://xstest.axioxio.com/SettingManagement", "name": "系统管理-系统设置"},
            
            # 门店管理
            {"url": "https://xstest.axioxio.com/StoreModule/Stores", "name": "系统管理-门店管理"},
        ]
        
        # 依次访问每个页面并截图
        self.click_menu_by_url(page, target_pages)
        
        print(f"\n✓ 功能页面遍历完成！共生成 {self.screenshot_count} 张截图")
    
    def save_menu_structure(self):
        """保存菜单结构到JSON文件"""
        with open(MENU_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.menu_structure, f, ensure_ascii=False, indent=2)
        print(f"✓ 菜单结构已保存到: {MENU_DATA_FILE}")
    
    def run(self):
        """主运行函数"""
        print("=" * 60)
        print("票务系统自动截图工具 V2")
        print("=" * 60)
        
        with sync_playwright() as p:
            # 启动浏览器
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
                
                # 遍历功能页面并截图
                self.traverse_menu_improved(page)
                
                # 保存菜单结构
                self.save_menu_structure()
                
                print("\n" + "=" * 60)
                print("任务完成！")
                print(f"截图保存目录: {self.screenshots_dir}")
                print(f"菜单结构文件: {MENU_DATA_FILE}")
                print(f"共生成 {self.screenshot_count} 张截图")
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
