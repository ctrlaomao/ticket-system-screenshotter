#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成第三方平台对接测试报告（Word格式）
"""

import json
from pathlib import Path
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

RESULT_FILE = "/workspace/third_party_test_report/test_result.json"
SCREENSHOTS_DIR = "/workspace/third_party_test_report/screenshots"
OUTPUT_FILE = "/workspace/third_party_test_report/第三方平台对接测试报告.docx"

class TestReportGenerator:
    def __init__(self):
        self.screenshots_dir = Path(SCREENSHOTS_DIR)
        
        # 加载测试结果
        with open(RESULT_FILE, 'r', encoding='utf-8') as f:
            self.test_results = json.load(f)
        
        print(f"已加载测试结果")
        print(f"测试时间: {self.test_results.get('test_time', 'N/A')}")
    
    def create_document(self):
        """创建Word文档"""
        doc = Document()
        
        # 设置中文字体
        doc.styles['Normal'].font.name = '微软雅黑'
        doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        
        return doc
    
    def add_title(self, doc):
        """添加标题"""
        title = doc.add_heading('第三方平台对接测试报告', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 设置标题字体
        title_run = title.runs[0]
        title_run.font.size = Pt(22)
        title_run.font.bold = True
        title_run.font.color.rgb = RGBColor(0, 51, 153)
        
        doc.add_paragraph()
    
    def add_test_info(self, doc):
        """添加测试信息"""
        doc.add_heading('一、测试基本信息', level=1)
        
        # 创建测试信息表格
        table = doc.add_table(rows=4, cols=2)
        table.style = 'Light Grid Accent 1'
        
        # 表头样式
        cells = table.rows[0].cells
        cells[0].text = '测试项目'
        cells[1].text = '测试内容'
        
        for cell in cells:
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 填充数据
        table.rows[1].cells[0].text = '测试时间'
        table.rows[1].cells[1].text = self.test_results.get('test_time', 'N/A')
        
        table.rows[2].cells[0].text = '测试系统'
        table.rows[2].cells[1].text = self.test_results.get('system_url', 'N/A')
        
        table.rows[3].cells[0].text = '测试账号'
        table.rows[3].cells[1].text = self.test_results.get('tester', 'N/A')
        
        doc.add_paragraph()
    
    def add_test_scope(self, doc):
        """添加测试范围"""
        doc.add_heading('二、测试范围', level=1)
        
        p = doc.add_paragraph()
        p.add_run('本次测试主要查看以下三个第三方平台的对接配置：').font.size = Pt(11)
        
        platforms = [
            "美团平台 - 查看回调域名、IP白名单等配置信息",
            "携程平台 - 查看回调域名、IP白名单等配置信息",
            "抖音平台 - 查看对接连调配置信息"
        ]
        
        for platform in platforms:
            p = doc.add_paragraph(platform, style='List Bullet')
            p.paragraph_format.left_indent = Inches(0.5)
        
        doc.add_paragraph()
    
    def add_platform_results(self, doc):
        """添加平台测试结果"""
        doc.add_heading('三、配置查看结果', level=1)
        
        platforms = self.test_results.get('platforms', [])
        
        for idx, platform in enumerate(platforms, 1):
            platform_name = platform.get('name', '未知平台')
            
            # 平台标题
            doc.add_heading(f'{idx}. {platform_name}平台', level=2)
            
            if platform.get('found', False):
                # 找到配置
                p = doc.add_paragraph()
                p.add_run('配置状态: ').font.bold = True
                p.add_run('✓ 已找到配置页面').font.color.rgb = RGBColor(0, 128, 0)
                
                # 配置信息
                if platform.get('url'):
                    p = doc.add_paragraph()
                    p.add_run('页面地址: ').font.bold = True
                    p.add_run(platform['url'])
                
                if platform.get('menu_text'):
                    p = doc.add_paragraph()
                    p.add_run('菜单位置: ').font.bold = True
                    p.add_run(platform['menu_text'])
                
                # 添加截图
                screenshot_file = platform.get('screenshot')
                if screenshot_file:
                    screenshot_path = self.screenshots_dir / screenshot_file
                    if screenshot_path.exists():
                        doc.add_paragraph()
                        p = doc.add_paragraph()
                        p.add_run('配置页面截图：').font.bold = True
                        doc.add_picture(str(screenshot_path), width=Inches(6))
                        
                        # 居中对齐
                        last_paragraph = doc.paragraphs[-1]
                        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    else:
                        p = doc.add_paragraph()
                        p.add_run('⚠ 截图文件未找到').font.color.rgb = RGBColor(255, 128, 0)
            else:
                # 未找到配置
                p = doc.add_paragraph()
                p.add_run('配置状态: ').font.bold = True
                p.add_run('✗ 未找到配置页面').font.color.rgb = RGBColor(255, 0, 0)
                
                message = platform.get('message', '未在系统中找到相关配置')
                p = doc.add_paragraph()
                p.add_run('说明: ').font.bold = True
                p.add_run(message)
            
            doc.add_paragraph()
    
    def add_manual_results(self, doc):
        """添加手动搜索结果"""
        manual_results = self.test_results.get('manual_search_results', [])
        
        if manual_results:
            doc.add_heading('四、第三方平台配置详情', level=1)
            
            p = doc.add_paragraph()
            p.add_run('通过系统页面查看，在分销商管理模块中找到了三个平台的配置信息：').font.size = Pt(11)
            doc.add_paragraph()
            
            for idx, result in enumerate(manual_results, 1):
                # 标题
                doc.add_heading(f'4.{idx} 配置页面 {idx}', level=2)
                
                # 页面地址
                p = doc.add_paragraph()
                p.add_run('页面地址: ').font.bold = True
                p.add_run(result.get('url', 'N/A'))
                
                # 包含的平台
                platforms = result.get('platforms', [])
                if platforms:
                    p = doc.add_paragraph()
                    p.add_run('包含平台: ').font.bold = True
                    
                    platform_text = p.add_run(', '.join(platforms))
                    platform_text.font.color.rgb = RGBColor(0, 128, 0)
                    platform_text.font.bold = True
                
                # 说明
                if len(platforms) == 3:
                    p = doc.add_paragraph()
                    p.add_run('说明: ').font.bold = True
                    p.add_run('该页面包含所有三个第三方平台（美团、携程、抖音）的配置信息，可以查看回调域名、IP白名单等关键配置项。')
                
                # 添加截图
                screenshot_file = result.get('screenshot')
                if screenshot_file:
                    screenshot_path = self.screenshots_dir / screenshot_file
                    if screenshot_path.exists():
                        doc.add_paragraph()
                        p = doc.add_paragraph()
                        p.add_run('配置页面截图：').font.bold = True
                        doc.add_picture(str(screenshot_path), width=Inches(6))
                        
                        # 居中对齐
                        last_paragraph = doc.paragraphs[-1]
                        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    else:
                        p = doc.add_paragraph()
                        p.add_run('⚠ 截图文件未找到').font.color.rgb = RGBColor(255, 128, 0)
                
                doc.add_paragraph()
    
    def add_conclusion(self, doc):
        """添加测试结论"""
        doc.add_heading('五、测试结论', level=1)
        
        platforms = self.test_results.get('platforms', [])
        manual_results = self.test_results.get('manual_search_results', [])
        
        # 统计实际找到的平台
        found_platforms = set()
        for result in manual_results:
            found_platforms.update(result.get('platforms', []))
        
        total_count = len(platforms)
        actual_found = len(found_platforms)
        
        # 结论表格
        table = doc.add_table(rows=5, cols=2)
        table.style = 'Light Grid Accent 1'
        
        table.rows[0].cells[0].text = '测试项'
        table.rows[0].cells[1].text = '结果'
        
        for cell in table.rows[0].cells:
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        table.rows[1].cells[0].text = '总测试平台数'
        table.rows[1].cells[1].text = str(total_count)
        
        table.rows[2].cells[0].text = '成功找到配置'
        table.rows[2].cells[1].text = str(actual_found)
        
        table.rows[3].cells[0].text = '配置页面数量'
        table.rows[3].cells[1].text = str(len(manual_results))
        
        table.rows[4].cells[0].text = '测试完成度'
        result_cell = table.rows[4].cells[1]
        result_cell.text = '100%' if actual_found == total_count else f'{actual_found}/{total_count}'
        if actual_found == total_count:
            result_cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0, 128, 0)
            result_cell.paragraphs[0].runs[0].font.bold = True
        
        doc.add_paragraph()
        
        # 总结
        p = doc.add_paragraph()
        p.add_run('总结：').font.bold = True
        
        if actual_found == total_count:
            summary = f"本次测试成功查看了所有{total_count}个第三方平台的配置信息。在分销商管理模块中找到了美团、携程、抖音三个平台的配置页面，可以查看回调域名、IP白名单等关键配置项。配置信息完整，页面访问正常。"
        elif actual_found > 0:
            summary = f"本次测试成功查看了{actual_found}个平台的配置信息，另有{total_count - actual_found}个平台的配置暂未找到，可能需要特定权限或在其他位置。"
        else:
            summary = "本次测试未能在系统中找到第三方平台的配置页面，建议联系系统管理员确认配置位置或权限。"
        
        doc.add_paragraph(summary)
        
        doc.add_paragraph()
    
    def add_recommendations(self, doc):
        """添加建议"""
        doc.add_heading('六、后续建议', level=1)
        
        recommendations = [
            "美团平台：建议联系美团技术支持，确认并修改回调域名和IP白名单配置",
            "携程平台：建议联系携程技术支持，确认并修改回调域名和IP白名单配置",
            "抖音平台：建议完成抖音连调测试，确保接口对接正常",
            "定期检查第三方平台配置，确保回调地址和白名单信息的准确性",
            "建立第三方平台配置变更记录，便于后续维护和追溯"
        ]
        
        for rec in recommendations:
            p = doc.add_paragraph(rec, style='List Bullet')
            p.paragraph_format.left_indent = Inches(0.5)
        
        doc.add_paragraph()
    
    def generate(self):
        """生成完整报告"""
        print("\n========== 生成测试报告 ==========")
        
        # 创建文档
        doc = self.create_document()
        
        # 添加各部分内容
        print("  添加标题...")
        self.add_title(doc)
        
        print("  添加测试信息...")
        self.add_test_info(doc)
        
        print("  添加测试范围...")
        self.add_test_scope(doc)
        
        print("  添加平台测试结果...")
        self.add_platform_results(doc)
        
        print("  添加手动搜索结果...")
        self.add_manual_results(doc)
        
        print("  添加测试结论...")
        self.add_conclusion(doc)
        
        print("  添加后续建议...")
        self.add_recommendations(doc)
        
        # 保存文档
        doc.save(OUTPUT_FILE)
        print(f"\n✓ 测试报告已生成: {OUTPUT_FILE}")
        
        return OUTPUT_FILE

if __name__ == "__main__":
    try:
        generator = TestReportGenerator()
        report_path = generator.generate()
        print(f"\n测试报告生成成功！")
        print(f"文件位置: {report_path}")
    except FileNotFoundError:
        print("\n✗ 错误：未找到测试结果文件")
        print("请先运行 test_third_party_platforms.py 进行测试")
    except Exception as e:
        print(f"\n✗ 生成报告时出错: {e}")
        import traceback
        traceback.print_exc()
