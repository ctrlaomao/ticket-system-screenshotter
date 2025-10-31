#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面分析系统菜单，找出所有未截图的功能
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

class MenuAnalyzer:
    def __init__(self):
        # 加载已有截图数据
        with open(MENU_DATA_FILE, 'r', encoding='utf-8') as f:
            self.existing_data = json.load(f)
        
        # 已有截图的URL集合
        self.existing_urls = set()
        for item in self.existing_data:
            if 'url' in item:
                self.existing_urls.add(item['url'])
        
        print(f"已加载 {len(self.existing_data)} 个已有截图")
        
        # 存储找到的所有菜单
        self.all_menus = []
        
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
        
        # 关闭弹窗
        try:
            page.keyboard.press("Escape")
            time.sleep(0.5)
        except:
            pass
        
        if page.url != LOGIN_URL:
            print("✓ 登录成功！\n")
            return True
        return False
    
    def get_all_menu_links(self, page):
        """获取所有菜单链接"""
        print("开始收集所有菜单链接...")
        time.sleep(2)
        
        # 查找所有可能的菜单链接
        link_selectors = ["nav a", ".sidebar a", "aside a", ".menu a"]
        
        all_links = {}
        
        for selector in link_selectors:
            try:
                links = page.locator(selector).all()
                if len(links) > 0:
                    print(f"使用选择器 {selector} 找到 {len(links)} 个链接")
                    
                    for link in links:
                        try:
                            text = link.inner_text().strip()
                            href = link.get_attribute('href')
                            
                            # 只收集有效的HTTP链接
                            if text and href and href.startswith('http'):
                                # 去除多余的空白字符和换行
                                clean_text = ' '.join(text.split())
                                
                                # 避免重复
                                if href not in all_links:
                                    all_links[href] = clean_text
                        except:
                            continue
                    break  # 找到一个有效的选择器就停止
            except:
                continue
        
        return all_links
    
    def expand_and_collect(self, page):
        """展开菜单并收集子菜单"""
        print("\n尝试展开主菜单收集子菜单...")
        
        # 需要展开的主菜单关键词
        main_menus = ["票务", "工作台", "订单", "预约", "教练", "培训", "营地", 
                      "次卡", "营期", "租赁", "分销", "报表", "管理", "小程序"]
        
        collected_links = {}
        
        # 获取所有菜单项
        menu_items = page.locator("nav li, .sidebar li, aside li").all()
        
        for item in menu_items:
            try:
                text = item.inner_text().strip()
                clean_text = ' '.join(text.split())
                
                # 检查是否是主菜单
                is_main_menu = False
                for menu_keyword in main_menus:
                    if clean_text.startswith(menu_keyword) and len(clean_text) < 20:
                        is_main_menu = True
                        break
                
                if is_main_menu:
                    print(f"\n展开主菜单: {clean_text}")
                    
                    try:
                        if item.is_visible():
                            # 点击展开
                            item.click(timeout=2000)
                            time.sleep(1.5)
                            
                            # 收集当前展开后的所有链接
                            current_links = page.locator("nav a, .sidebar a, aside a").all()
                            for link in current_links:
                                try:
                                    link_text = link.inner_text().strip()
                                    link_href = link.get_attribute('href')
                                    
                                    if link_text and link_href and link_href.startswith('http'):
                                        clean_link_text = ' '.join(link_text.split())
                                        if link_href not in collected_links:
                                            collected_links[link_href] = clean_link_text
                                            print(f"  找到: {clean_link_text} -> {link_href}")
                                except:
                                    continue
                    except:
                        pass
            except:
                continue
        
        return collected_links
    
    def analyze_menus(self, page):
        """分析所有菜单"""
        print("=" * 60)
        print("开始全面分析系统菜单")
        print("=" * 60)
        
        # 第一轮：收集直接可见的链接
        direct_links = self.get_all_menu_links(page)
        print(f"\n第一轮收集到 {len(direct_links)} 个直接链接")
        
        # 第二轮：展开菜单收集子菜单
        expanded_links = self.expand_and_collect(page)
        print(f"\n第二轮收集到 {len(expanded_links)} 个展开后的链接")
        
        # 合并所有链接
        all_links = {**direct_links, **expanded_links}
        
        print(f"\n" + "=" * 60)
        print(f"总共找到 {len(all_links)} 个唯一菜单链接")
        print("=" * 60)
        
        # 分析每个链接是否已有截图
        missing_menus = []
        existing_menus = []
        
        for url, text in sorted(all_links.items(), key=lambda x: x[1]):
            has_screenshot = url in self.existing_urls
            
            menu_info = {
                'name': text,
                'url': url,
                'has_screenshot': has_screenshot
            }
            
            if has_screenshot:
                existing_menus.append(menu_info)
            else:
                missing_menus.append(menu_info)
            
            self.all_menus.append(menu_info)
        
        return existing_menus, missing_menus
    
    def generate_report(self, existing_menus, missing_menus):
        """生成分析报告"""
        print("\n" + "=" * 60)
        print("菜单分析报告")
        print("=" * 60)
        
        print(f"\n已有截图的菜单: {len(existing_menus)} 个")
        print("-" * 60)
        for idx, menu in enumerate(existing_menus, 1):
            print(f"{idx}. ✅ {menu['name']}")
            print(f"   {menu['url']}")
        
        print(f"\n" + "=" * 60)
        print(f"缺失截图的菜单: {len(missing_menus)} 个")
        print("=" * 60)
        for idx, menu in enumerate(missing_menus, 1):
            print(f"{idx}. ❌ {menu['name']}")
            print(f"   {menu['url']}\n")
        
        # 保存到文件
        result = {
            'total': len(self.all_menus),
            'existing': len(existing_menus),
            'missing': len(missing_menus),
            'existing_menus': existing_menus,
            'missing_menus': missing_menus,
            'all_menus': self.all_menus
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
                
                # 分析菜单
                existing_menus, missing_menus = self.analyze_menus(page)
                
                # 生成报告
                result = self.generate_report(existing_menus, missing_menus)
                
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
    analyzer = MenuAnalyzer()
    analyzer.run()
