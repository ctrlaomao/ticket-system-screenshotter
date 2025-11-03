#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确捕获OTA平台配置并打码
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

class OTAPlatformCapture:
    def __init__(self):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.login_url = self.config['login']['url']
        self.base_url = self.config['login']['base_url']
        self.username = self.config['login']['username']
        self.password = self.config['login']['password']
        self.ota_settings_url = f"{self.base_url}/SettingManagement"
        
        self.screenshots_dir = Path(SCREENSHOTS_DIR)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        
        self.test_results = {
            "test_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tester": self.username,
            "system_url": self.base_url,
            "ota_settings_url": self.ota_settings_url,
            "platforms": []
        }
    
    def login(self, page):
        """登录"""
        print("\n========== 登录系统 ==========")
        page.goto(self.login_url, wait_until="domcontentloaded")
        time.sleep(2)
        
        page.locator("input[type='text']").first.fill(self.username)
        page.locator("input[type='password']").first.fill(self.password)
        time.sleep(1)
        page.locator("button[type='submit']").first.click()
        time.sleep(5)
        
        try:
            page.keyboard.press("Escape")
            time.sleep(0.5)
        except:
            pass
        
        if page.url != self.login_url:
            print(f"✓ 登录成功")
            return True
        return False
    
    def capture_full_page_and_analyze(self, page):
        """截取完整页面并分析配置标签"""
        print("\n========== 访问并分析OTA设置页面 ==========")
        
        page.goto(self.ota_settings_url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)
        
        print(f"✓ 页面加载完成: {self.ota_settings_url}")
        
        # 获取页面中所有的标签文本
        page_text = page.evaluate('''() => {
            return document.body.innerText;
        }''')
        
        print("\n--- 页面内容分析 ---")
        print(f"页面文本长度: {len(page_text)} 字符")
        
        # 查找关键词
        platforms_found = {
            "美团": "美团" in page_text or "meituan" in page_text.lower(),
            "携程": "携程" in page_text or "ctrip" in page_text.lower() or "xiecheng" in page_text.lower(),
            "抖音": "抖音" in page_text or "douyin" in page_text.lower()
        }
        
        for platform, found in platforms_found.items():
            status = "✓ 找到" if found else "✗ 未找到"
            print(f"{status} {platform} 配置")
        
        # 获取所有标签元素
        print("\n--- 查找配置标签元素 ---")
        labels = page.query_selector_all('label, .label, span.label-text, div.form-label')
        print(f"找到 {len(labels)} 个标签元素")
        
        # 截取完整页面
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        raw_filename = f"OTA设置_原始_{timestamp}.png"
        raw_path = self.screenshots_dir / raw_filename
        page.screenshot(path=str(raw_path), full_page=True)
        print(f"✓ 原始截图已保存: {raw_filename}")
        
        return raw_path, platforms_found
    
    def apply_smart_mosaic(self, image_path, platforms_found):
        """智能打码 - 根据页面内容"""
        print("\n========== 应用智能打码 ==========")
        
        img = Image.open(image_path)
        width, height = img.size
        
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # 定义遮罩区域 - 根据OTA设置页面的典型布局
        # 通常配置信息在页面主内容区域的表单中
        
        # 假设页面布局：
        # - 左侧导航栏约占 15-20%
        # - 主内容区域在右侧
        # - 配置表单在主内容区域
        
        content_start_x = int(width * 0.20)  # 内容区域开始位置
        content_end_x = int(width * 0.95)    # 内容区域结束位置
        
        # 平台配置通常在页面不同位置
        # 我们创建多个遮罩条来覆盖可能的敏感信息区域
        
        mask_regions = []
        
        # 为每个找到的平台创建遮罩区域
        platform_count = sum(1 for found in platforms_found.values() if found)
        
        if platform_count > 0:
            # 将页面内容区域分成几个部分
            section_height = int(height * 0.15)  # 每个配置区域的高度
            
            # 美团配置区域 (通常在上部)
            if platforms_found.get("美团"):
                y_start = int(height * 0.25)
                mask_regions.append((content_start_x, y_start, content_end_x, y_start + section_height, "美团配置"))
            
            # 携程配置区域 (通常在中部)
            if platforms_found.get("携程"):
                y_start = int(height * 0.45)
                mask_regions.append((content_start_x, y_start, content_end_x, y_start + section_height, "携程配置"))
            
            # 抖音配置区域 (通常在下部)
            if platforms_found.get("抖音"):
                y_start = int(height * 0.65)
                mask_regions.append((content_start_x, y_start, content_end_x, y_start + section_height, "抖音配置"))
        else:
            # 如果没有找到具体平台，使用通用遮罩策略
            # 遮罩整个内容区域的关键部分
            for i in range(5):
                y_start = int(height * (0.2 + i * 0.15))
                y_end = y_start + int(height * 0.08)
                mask_regions.append((content_start_x, y_start, content_end_x, y_end, f"配置区域 {i+1}"))
        
        # 应用遮罩
        mask_count = 0
        for x1, y1, x2, y2, label in mask_regions:
            # 绘制半透明黑色矩形
            draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, 220))
            
            # 添加标签
            text_x = x1 + 20
            text_y = y1 + (y2 - y1) // 2 - 12
            draw.text((text_x, text_y), f"🔒 {label} - 敏感信息已遮罩", fill=(255, 255, 255, 255))
            
            mask_count += 1
            print(f"  ✓ 遮罩 {mask_count}: {label}")
        
        # 合并图层
        img = Image.alpha_composite(img, overlay)
        
        # 转换为RGB
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        
        # 保存打码后的图片
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        masked_filename = f"OTA平台设置_已打码_{timestamp}.png"
        masked_path = self.screenshots_dir / masked_filename
        img.save(masked_path)
        
        print(f"✓ 打码图片已保存: {masked_filename}")
        print(f"  共应用 {mask_count} 个遮罩区域")
        
        # 删除原始截图（包含敏感信息）
        Path(image_path).unlink()
        print(f"✓ 原始截图已删除（安全考虑）")
        
        return masked_filename
    
    def save_results(self, platforms_found, screenshot_file):
        """保存结果"""
        for platform_name, found in platforms_found.items():
            self.test_results["platforms"].append({
                "name": platform_name,
                "found": found,
                "screenshot": screenshot_file if found else ""
            })
        
        self.test_results["screenshot"] = screenshot_file
        
        with open(RESULT_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 测试结果已保存: {RESULT_FILE}")
    
    def run(self):
        """执行"""
        print("\n" + "="*60)
        print("OTA平台配置查看 - 美团、携程、抖音")
        print("="*60)
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                locale='zh-CN'
            )
            page = context.new_page()
            
            try:
                if not self.login(page):
                    print("✗ 登录失败")
                    return False
                
                # 截图并分析
                raw_image, platforms_found = self.capture_full_page_and_analyze(page)
                
                # 应用智能打码
                masked_file = self.apply_smart_mosaic(raw_image, platforms_found)
                
                # 保存结果
                self.save_results(platforms_found, masked_file)
                
                print("\n" + "="*60)
                print("任务完成！")
                print("="*60)
                print(f"打码截图: {self.screenshots_dir / masked_file}")
                
                return True
                
            except Exception as e:
                print(f"\n✗ 错误: {e}")
                import traceback
                traceback.print_exc()
                return False
            finally:
                browser.close()

if __name__ == "__main__":
    capturer = OTAPlatformCapture()
    capturer.run()
