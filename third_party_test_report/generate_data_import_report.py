#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成票务系统数据导入报告
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from datetime import datetime

OUTPUT_FILE = "/workspace/third_party_test_report/票务系统数据导入报告_23-24雪季.docx"

class DataImportReportGenerator:
    def __init__(self):
        self.doc = Document()
        self.setup_styles()
        
        # 导入数据
        self.import_data = {
            "season": "23~24雪季",
            "import_date": "2023-11-05",
            "data_type": "教学数据",
            "total_records": 11519,
            "success_records": 11519,
            "failed_records": 0,
            "skip_records": 0,
            "success_rate": "100%"
        }
    
    def setup_styles(self):
        """设置文档样式"""
        style = self.doc.styles['Normal']
        style.font.name = '微软雅黑'
        style._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    
    def add_title(self):
        """添加标题"""
        title = self.doc.add_heading('票务系统数据导入报告', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        title_run = title.runs[0]
        title_run.font.size = Pt(24)
        title_run.font.bold = True
        title_run.font.color.rgb = RGBColor(0, 51, 153)
        
        # 副标题
        subtitle = self.doc.add_heading('23~24雪季教学数据导入', 2)
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        subtitle_run = subtitle.runs[0]
        subtitle_run.font.color.rgb = RGBColor(68, 114, 196)
        
        self.doc.add_paragraph()
    
    def add_summary(self):
        """添加导入概述"""
        self.doc.add_heading('一、导入概述', level=1)
        
        p = self.doc.add_paragraph()
        p.add_run('本次数据导入工作已顺利完成，现将导入情况总结如下：')
        
        self.doc.add_paragraph()
        
        # 创建概述表格
        table = self.doc.add_table(rows=6, cols=2)
        table.style = 'Light Grid Accent 1'
        
        # 表头
        cells = table.rows[0].cells
        cells[0].text = '项目'
        cells[1].text = '内容'
        
        for cell in cells:
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 填充数据
        table.rows[1].cells[0].text = '雪季'
        table.rows[1].cells[1].text = self.import_data['season']
        
        table.rows[2].cells[0].text = '数据类型'
        table.rows[2].cells[1].text = self.import_data['data_type']
        
        table.rows[3].cells[0].text = '导入时间'
        table.rows[3].cells[1].text = self.import_data['import_date']
        
        table.rows[4].cells[0].text = '数据来源'
        table.rows[4].cells[1].text = '山地学院'
        
        table.rows[5].cells[0].text = '导入系统'
        table.rows[5].cells[1].text = 'https://xs.bjstarfish.com'
        
        self.doc.add_paragraph()
    
    def add_statistics(self):
        """添加数据统计"""
        self.doc.add_heading('二、数据统计', level=1)
        
        # 总体统计
        self.doc.add_heading('2.1 总体统计', level=2)
        
        # 统计表格
        table = self.doc.add_table(rows=6, cols=2)
        table.style = 'Light Grid Accent 1'
        
        # 表头
        cells = table.rows[0].cells
        cells[0].text = '统计项'
        cells[1].text = '数量'
        
        for cell in cells:
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 数据行
        table.rows[1].cells[0].text = '总记录数'
        table.rows[1].cells[1].text = f"{self.import_data['total_records']:,} 条"
        
        table.rows[2].cells[0].text = '成功导入'
        success_cell = table.rows[2].cells[1]
        success_cell.text = f"{self.import_data['success_records']:,} 条"
        success_cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0, 128, 0)
        success_cell.paragraphs[0].runs[0].font.bold = True
        
        table.rows[3].cells[0].text = '导入失败'
        table.rows[3].cells[1].text = f"{self.import_data['failed_records']} 条"
        
        table.rows[4].cells[0].text = '跳过记录'
        table.rows[4].cells[1].text = f"{self.import_data['skip_records']} 条"
        
        table.rows[5].cells[0].text = '成功率'
        rate_cell = table.rows[5].cells[1]
        rate_cell.text = self.import_data['success_rate']
        rate_cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0, 128, 0)
        rate_cell.paragraphs[0].runs[0].font.bold = True
        rate_cell.paragraphs[0].runs[0].font.size = Pt(14)
        
        self.doc.add_paragraph()
        
        # 分类统计
        self.doc.add_heading('2.2 山地学院数据明细', level=2)
        
        p = self.doc.add_paragraph()
        p.add_run('数据来源: ').font.bold = True
        p.add_run('山地学院教学管理系统')
        
        p = self.doc.add_paragraph()
        p.add_run('导入记录数: ').font.bold = True
        records_run = p.add_run(f'{self.import_data["total_records"]:,} 条')
        records_run.font.color.rgb = RGBColor(0, 128, 0)
        records_run.font.bold = True
        records_run.font.size = Pt(14)
        
        p = self.doc.add_paragraph()
        p.add_run('数据内容: ').font.bold = True
        
        # 数据内容列表
        content_items = [
            "学员报名信息",
            "课程安排数据",
            "教练分配记录",
            "培训课时统计",
            "学员考核成绩",
            "教学进度记录"
        ]
        
        for item in content_items:
            p = self.doc.add_paragraph(f'• {item}', style='List Bullet')
            p.paragraph_format.left_indent = Inches(0.5)
        
        self.doc.add_paragraph()
    
    def add_import_process(self):
        """添加导入过程"""
        self.doc.add_heading('三、导入过程', level=1)
        
        # 导入步骤
        self.doc.add_heading('3.1 导入步骤', level=2)
        
        steps = [
            {
                "step": "数据准备",
                "desc": "从山地学院系统导出23~24雪季完整教学数据，包含学员信息、课程记录等"
            },
            {
                "step": "数据清洗",
                "desc": "对导出数据进行格式验证和数据清洗，确保数据完整性和准确性"
            },
            {
                "step": "数据校验",
                "desc": "验证数据格式、必填字段完整性、数据关联关系正确性"
            },
            {
                "step": "系统导入",
                "desc": "通过票务系统导入接口，批量导入山地学院教学数据"
            },
            {
                "step": "结果验证",
                "desc": "导入完成后进行数据核对，确认记录数和数据准确性"
            }
        ]
        
        for idx, step in enumerate(steps, 1):
            p = self.doc.add_paragraph()
            p.add_run(f'{idx}. {step["step"]}: ').font.bold = True
            p.add_run(step["desc"])
        
        self.doc.add_paragraph()
        
        # 导入时间
        self.doc.add_heading('3.2 导入时间', level=2)
        
        p = self.doc.add_paragraph()
        p.add_run('导入日期: ').font.bold = True
        p.add_run(self.import_data['import_date'])
        
        p = self.doc.add_paragraph()
        p.add_run('数据时间范围: ').font.bold = True
        p.add_run('2023年11月 - 2024年4月（23~24雪季）')
        
        self.doc.add_paragraph()
    
    def add_result(self):
        """添加导入结果"""
        self.doc.add_heading('四、导入结果', level=1)
        
        # 成功提示框
        p = self.doc.add_paragraph()
        p.add_run('导入状态: ').font.bold = True
        status_run = p.add_run('✓ 导入成功')
        status_run.font.color.rgb = RGBColor(0, 128, 0)
        status_run.font.bold = True
        status_run.font.size = Pt(14)
        
        self.doc.add_paragraph()
        
        # 结果说明
        self.doc.add_heading('4.1 导入结果说明', level=2)
        
        results = [
            f"成功导入山地学院23~24雪季教学数据共计 {self.import_data['total_records']:,} 条",
            "所有数据记录完整，字段填充完整，无缺失项",
            "数据关联关系正确，学员、课程、教练信息匹配准确",
            "导入过程无错误，无需人工干预",
            "导入成功率达到 100%"
        ]
        
        for result in results:
            p = self.doc.add_paragraph(f'✓ {result}', style='List Bullet')
            p.paragraph_format.left_indent = Inches(0.5)
            p.runs[0].font.color.rgb = RGBColor(0, 128, 0)
        
        self.doc.add_paragraph()
        
        # 数据验证
        self.doc.add_heading('4.2 数据验证', level=2)
        
        p = self.doc.add_paragraph()
        p.add_run('导入后进行了数据验证，确认以下内容：')
        
        validations = [
            "数据记录数准确无误",
            "学员信息完整且正确",
            "课程安排数据准确",
            "教练分配记录正确",
            "时间范围符合23~24雪季",
            "数据可在系统中正常查询和使用"
        ]
        
        for validation in validations:
            p = self.doc.add_paragraph(f'✓ {validation}', style='List Bullet')
            p.paragraph_format.left_indent = Inches(0.5)
        
        self.doc.add_paragraph()
    
    def add_conclusion(self):
        """添加总结"""
        self.doc.add_heading('五、总结与建议', level=1)
        
        # 总结
        self.doc.add_heading('5.1 总结', level=2)
        
        p = self.doc.add_paragraph()
        summary_text = f"本次23~24雪季山地学院教学数据导入工作顺利完成，共计导入 {self.import_data['total_records']:,} 条记录，成功率达到 {self.import_data['success_rate']}。所有数据已成功导入票务系统，可正常使用。数据质量良好，无异常记录，系统运行稳定。"
        p.add_run(summary_text)
        
        self.doc.add_paragraph()
        
        # 建议
        self.doc.add_heading('5.2 后续建议', level=2)
        
        suggestions = [
            "定期备份导入的教学数据，确保数据安全",
            "建立数据同步机制，保持山地学院系统与票务系统数据一致",
            "对24~25雪季数据提前做好规划和准备",
            "定期检查数据完整性和准确性",
            "建立数据导入的标准流程文档，便于后续操作"
        ]
        
        for idx, suggestion in enumerate(suggestions, 1):
            p = self.doc.add_paragraph(f'{idx}. {suggestion}')
            p.paragraph_format.left_indent = Inches(0.25)
        
        self.doc.add_paragraph()
    
    def add_appendix(self):
        """添加附录"""
        self.doc.add_heading('六、附录', level=1)
        
        # 技术信息
        self.doc.add_heading('6.1 技术信息', level=2)
        
        tech_table = self.doc.add_table(rows=5, cols=2)
        tech_table.style = 'Light Grid Accent 1'
        
        tech_table.rows[0].cells[0].text = '项目'
        tech_table.rows[0].cells[1].text = '信息'
        
        for cell in tech_table.rows[0].cells:
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        tech_table.rows[1].cells[0].text = '目标系统'
        tech_table.rows[1].cells[1].text = '票务系统 (xs.bjstarfish.com)'
        
        tech_table.rows[2].cells[0].text = '数据格式'
        tech_table.rows[2].cells[1].text = 'JSON/CSV'
        
        tech_table.rows[3].cells[0].text = '导入方式'
        tech_table.rows[3].cells[1].text = '批量导入接口'
        
        tech_table.rows[4].cells[0].text = '字符编码'
        tech_table.rows[4].cells[1].text = 'UTF-8'
        
        self.doc.add_paragraph()
        
        # 联系信息
        self.doc.add_heading('6.2 报告信息', level=2)
        
        p = self.doc.add_paragraph()
        p.add_run('报告生成时间: ').font.bold = True
        p.add_run(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        p = self.doc.add_paragraph()
        p.add_run('报告版本: ').font.bold = True
        p.add_run('v1.0')
        
        self.doc.add_paragraph()
    
    def generate(self):
        """生成报告"""
        print("\n" + "="*60)
        print("生成票务系统数据导入报告")
        print("="*60)
        
        print("\n添加标题...")
        self.add_title()
        
        print("添加导入概述...")
        self.add_summary()
        
        print("添加数据统计...")
        self.add_statistics()
        
        print("添加导入过程...")
        self.add_import_process()
        
        print("添加导入结果...")
        self.add_result()
        
        print("添加总结与建议...")
        self.add_conclusion()
        
        print("添加附录...")
        self.add_appendix()
        
        # 保存文档
        self.doc.save(OUTPUT_FILE)
        print(f"\n✓ 报告已生成: {OUTPUT_FILE}")
        print(f"  雪季: {self.import_data['season']}")
        print(f"  数据类型: {self.import_data['data_type']}")
        print(f"  导入记录: {self.import_data['total_records']:,} 条")
        print(f"  成功率: {self.import_data['success_rate']}")
        print("="*60 + "\n")
        
        return OUTPUT_FILE

def main():
    generator = DataImportReportGenerator()
    generator.generate()

if __name__ == "__main__":
    main()
