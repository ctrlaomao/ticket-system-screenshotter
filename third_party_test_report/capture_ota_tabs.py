#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OTA平台Tab截图脚本 - 分别截取美团、携程、抖音设置
"""

import time
import json
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw

CONFIG_FILE = "/workspace/config.json"
SCREENSHOTS_DIR = "/workspace/third_party_test_report/screenshots"
RESULT_FILE = "/workspace/third_party_test_report/test_result.json"

class OTATabCapture:
    def __init__(self):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.login_url = self.config['login']['url']
        self.base_url = self.config['login']['base_url']
        self.username = self.config['login']['username']
        self.password = self.config['login']['password']
        self.settings_url = f"{self.base_url}/SettingManagement"
        
        self.screenshots_dir = Path(SCREENSHOTS_DIR)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        
        self.test_results = {
            "test_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tester": self.username,
            "system_url": self.base_url,
            "settings_url": self.settings_url,
            "platforms": []
        }
        
        print(f"初始化完成")
        print(f"系统地址: {self.base_url}")
        print(f"设置页面: {self.settings_url}")
    
    def login(self, page):
        """登录系统"""
        print("\n========== 登录系统 ==========")
        page.goto(self.login_url, wait_until="domcontentloaded")
        time.sleep(2)
        
        page.locator("input[type='text']").first.fill(self.username)
        print(f"✓ 已输入用户名")
        
        page.locator("input[type='password']").first.fill(self.password)
        print(f"✓ 已输入密码")
        
        time.sleep(1)
        page.locator("button[type='submit']").first.click()
        print("✓ 已点击登录")
        
        time.sleep(5)
        
        try:
            page.keyboard.press("Escape")
            time.sleep(0.5)
        except:
            pass
        
        if page.url != self.login_url:
            print(f"✓ 登录成功！")
            return True
        return False
    
    def navigate_to_settings(self, page):
        """访问设置页面"""
        print("\n========== 访问设置页面 ==========")
        page.goto(self.settings_url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)
        print(f"✓ 设置页面加载完成")
        return True
    
    def find_and_click_ota_option(self, page):
        """查找并点击OTA平台选项"""
        print("\n========== 查找OTA平台选项 ==========")
        
        # 尝试多种选择器查找OTA平台选项
        ota_selectors = [
            "text=OTA平台",
            "text=OTA",
            "span:has-text('OTA平台')",
            "span:has-text('OTA')",
            "div:has-text('OTA平台')",
            "a:has-text('OTA平台')",
            "a:has-text('OTA')",
            ".nav-item:has-text('OTA')",
            "li:has-text('OTA平台')",
            "li:has-text('OTA')"
        ]
        
        for selector in ota_selectors:
            try:
                element = page.locator(selector).first
                if element.is_visible(timeout=2000):
                    print(f"  找到OTA选项: {selector}")
                    element.click()
                    time.sleep(2)
                    print(f"✓ 已点击OTA平台选项")
                    return True
            except:
                continue
        
        print("⚠ 未找到明确的OTA平台选项，尝试查找页面中的所有链接...")
        
        # 打印页面中包含OTA的所有文本
        page_text = page.evaluate('''() => {
            return document.body.innerText;
        }''')
        
        if "OTA" in page_text or "ota" in page_text.lower():
            print("✓ 页面包含OTA相关内容")
        else:
            print("⚠ 页面不包含OTA文字")
        
        return False
    
    def capture_platform_tabs(self, page):
        """依次点击并截取三个平台的tab"""
        print("\n========== 截取平台Tab ==========")
        
        platforms = [
            {"name": "美团", "keywords": ["美团设置", "美团", "Meituan", "meituan"]},
            {"name": "抖音", "keywords": ["抖音设置", "抖音", "Douyin", "douyin", "TikTok"]},
            {"name": "携程", "keywords": ["携程设置", "携程", "Ctrip", "ctrip", "携程旅行"]}
        ]
        
        screenshots = {}
        
        for platform in platforms:
            print(f"\n--- 截取 {platform['name']} 设置 ---")
            
            found_tab = False
            
            # 尝试查找并点击tab
            for keyword in platform['keywords']:
                tab_selectors = [
                    f"text={keyword}",
                    f"[role='tab']:has-text('{keyword}')",
                    f".tab:has-text('{keyword}')",
                    f".nav-link:has-text('{keyword}')",
                    f"a:has-text('{keyword}')",
                    f"button:has-text('{keyword}')",
                    f"span:has-text('{keyword}')",
                    f"div[role='tab']:has-text('{keyword}')"
                ]
                
                for selector in tab_selectors:
                    try:
                        tab = page.locator(selector).first
                        if tab.is_visible(timeout=2000):
                            print(f"  找到tab: {keyword}")
                            tab.click()
                            time.sleep(2)
                            print(f"  ✓ 已点击 {keyword} tab")
                            found_tab = True
                            break
                    except:
                        continue
                
                if found_tab:
                    break
            
            if not found_tab:
                print(f"  ⚠ 未找到 {platform['name']} 的tab，尝试截取当前页面")
            
            # 截图
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{platform['name']}_设置_原始_{timestamp}.png"
            filepath = self.screenshots_dir / filename
            
            try:
                # 等待内容加载
                time.sleep(1)
                
                # 全页截图
                page.screenshot(path=str(filepath), full_page=True)
                print(f"  ✓ 原始截图已保存: {filename}")
                
                # 应用打码
                masked_filename = self.apply_mosaic(filepath, platform['name'])
                
                screenshots[platform['name']] = {
                    "found": found_tab,
                    "screenshot": masked_filename,
                    "timestamp": timestamp
                }
                
                # 添加到结果
                self.test_results["platforms"].append({
                    "name": platform['name'],
                    "found": found_tab,
                    "screenshot": masked_filename
                })
                
            except Exception as e:
                print(f"  ✗ 截图失败: {e}")
        
        return screenshots
    
    def apply_mosaic(self, image_path, platform_name):
        """对截图应用打码"""
        print(f"  应用打码处理...")
        
        try:
            img = Image.open(image_path)
            width, height = img.size
            
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            # 定义需要打码的区域
            # 假设配置信息在页面右侧中部区域
            content_start_x = int(width * 0.25)
            content_end_x = int(width * 0.95)
            
            # 创建多个遮罩条
            mask_regions = [
                (content_start_x, int(height * 0.25), content_end_x, int(height * 0.32), "AppID/应用ID"),
                (content_start_x, int(height * 0.35), content_end_x, int(height * 0.42), "AppSecret/密钥"),
                (content_start_x, int(height * 0.45), content_end_x, int(height * 0.52), "Token/令牌"),
                (content_start_x, int(height * 0.55), content_end_x, int(height * 0.62), "回调地址"),
                (content_start_x, int(height * 0.65), content_end_x, int(height * 0.72), "其他配置信息"),
            ]
            
            # 应用遮罩
            for x1, y1, x2, y2, label in mask_regions:
                draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, 220))
                
                # 添加标签
                text_x = x1 + 20
                text_y = y1 + (y2 - y1) // 2 - 10
                draw.text((text_x, text_y), f"🔒 {label} 已遮罩", fill=(255, 255, 255, 255))
            
            # 合并图层
            img = Image.alpha_composite(img, overlay)
            
            # 转换为RGB
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            
            # 保存打码后的图片
            masked_filename = Path(image_path).stem.replace('_原始_', '_已打码_') + '.png'
            masked_path = self.screenshots_dir / masked_filename
            img.save(masked_path)
            
            print(f"  ✓ 打码图片已保存: {masked_filename}")
            
            # 删除原始截图
            Path(image_path).unlink()
            print(f"  ✓ 原始截图已删除")
            
            return masked_filename
            
        except Exception as e:
            print(f"  ✗ 打码失败: {e}")
            return Path(image_path).name
    
    def save_results(self):
        """保存测试结果"""
        with open(RESULT_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        print(f"\n✓ 测试结果已保存: {RESULT_FILE}")
    
    def run(self):
        """执行测试"""
        print("\n" + "="*60)
        print("OTA平台Tab截图 - 美团/携程/抖音")
        print("="*60)
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                locale='zh-CN'
            )
            page = context.new_page()
            
            try:
                # 登录
                if not self.login(page):
                    print("✗ 登录失败")
                    return False
                
                # 访问设置页面
                if not self.navigate_to_settings(page):
                    print("✗ 无法访问设置页面")
                    return False
                
                # 查找并点击OTA平台选项
                self.find_and_click_ota_option(page)
                
                # 等待页面加载
                time.sleep(2)
                
                # 截取三个平台的tab
                screenshots = self.capture_platform_tabs(page)
                
                # 保存结果
                self.save_results()
                
                print("\n" + "="*60)
                print("任务完成！")
                print("="*60)
                print(f"截图保存位置: {self.screenshots_dir}")
                print(f"\n已截取的平台:")
                for platform_name, info in screenshots.items():
                    status = "✓" if info['found'] else "○"
                    print(f"  {status} {platform_name}: {info['screenshot']}")
                
                return True
                
            except Exception as e:
                print(f"\n✗ 错误: {e}")
                import traceback
                traceback.print_exc()
                return False
            finally:
                browser.close()

if __name__ == "__main__":
    capturer = OTATabCapture()
    capturer.run()
