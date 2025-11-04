#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成闸机维护与更新操作文档
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

OUTPUT_FILE = "/workspace/third_party_test_report/闸机维护与更新操作手册.docx"

class GateMaintenanceDocGenerator:
    def __init__(self):
        self.doc = Document()
        self.setup_styles()
    
    def setup_styles(self):
        """设置文档样式"""
        style = self.doc.styles['Normal']
        style.font.name = '微软雅黑'
        style._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    
    def add_title(self):
        """添加标题"""
        title = self.doc.add_heading('闸机维护与更新操作手册', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        title_run = title.runs[0]
        title_run.font.size = Pt(24)
        title_run.font.bold = True
        title_run.font.color.rgb = RGBColor(0, 51, 153)
        
        # 添加部署日期
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        date_run = p.add_run('部署日期：2023-11-05')
        date_run.font.size = Pt(14)
        date_run.font.color.rgb = RGBColor(68, 114, 196)
        
        self.doc.add_paragraph()
    
    def add_overview(self):
        """添加文档说明"""
        self.doc.add_heading('一、文档说明', level=1)
        
        p = self.doc.add_paragraph()
        p.add_run('本文档用于指导闸机系统的日常维护和软件更新操作，包含完整的更新流程、登录信息和远程操作方法。')
        
        self.doc.add_paragraph()
        
        # 供应商信息
        self.doc.add_heading('1.1 供应商信息', level=2)
        
        table = self.doc.add_table(rows=3, cols=2)
        table.style = 'Light Grid Accent 1'
        
        table.rows[0].cells[0].text = '项目'
        table.rows[0].cells[1].text = '信息'
        
        for cell in table.rows[0].cells:
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        table.rows[1].cells[0].text = '供应商名称'
        table.rows[1].cells[1].text = '亿思维科技有限公司'
        
        table.rows[2].cells[0].text = '服务内容'
        table.rows[2].cells[1].text = '闸机维护、软件更新、技术支持'
        
        self.doc.add_paragraph()
        
        # 维护说明
        self.doc.add_heading('1.2 维护方式', level=2)
        
        p = self.doc.add_paragraph()
        p.add_run('维护负责方: ').font.bold = True
        p.add_run('亿思维科技有限公司')
        
        p = self.doc.add_paragraph()
        p.add_run('维护内容: ').font.bold = True
        
        maintenance_items = [
            "闸机硬件日常维护",
            "系统软件更新升级",
            "故障排查与修复",
            "系统配置与优化",
            "远程技术支持"
        ]
        
        for item in maintenance_items:
            p = self.doc.add_paragraph(f'• {item}', style='List Bullet')
            p.paragraph_format.left_indent = Inches(0.5)
        
        self.doc.add_paragraph()
    
    def add_update_process(self):
        """添加更新流程"""
        self.doc.add_heading('二、闸机更新流程', level=1)
        
        p = self.doc.add_paragraph()
        p.add_run('重要提示: ').font.bold = True
        warning = p.add_run('更新前请确保已备份重要数据，并在系统空闲时段进行更新操作。')
        warning.font.color.rgb = RGBColor(255, 128, 0)
        warning.font.italic = True
        
        self.doc.add_paragraph()
        
        # 更新步骤
        steps = [
            {
                "title": "步骤一：确认系统版本",
                "content": "在设置里查看系统版本号，确认当前版本。",
                "note": "记录当前版本号，便于后续确认更新是否成功。"
            },
            {
                "title": "步骤二：准备更新并重启",
                "content": "插入优盘，关闭闸机电源开关，重启闸机，开机自检。系统检测到更新包后，给出是否更新提示，可以拔掉音响的USB，插上鼠标，确认安装。",
                "note": "确保优盘中包含正确的更新包文件。"
            },
            {
                "title": "步骤三：卸载旧版本并安装新版本",
                "content": "系统更新完毕后，卸载亿思维应用，直接拖动卸载。安装下载好的APK包，浏览器自动下载到系统的下载目录中。",
                "note": "确保新版本APK文件完整且未损坏。"
            },
            {
                "title": "步骤四：退出并重新登录",
                "content": "应用更新好后，进入系统，鼠标长按右下角版本号，退出当前账号重新登录。",
                "note": "重新登录以确保系统加载新版本配置。"
            },
            {
                "title": "步骤五：同步系统数据",
                "content": "登录后，单击左下角系统自动同步用户信息，包括人脸识别数据。",
                "note": "等待数据同步完成，不要中断同步过程。"
            },
            {
                "title": "步骤六：测试验证",
                "content": "测试人脸识别和二维码识别功能是否正常。",
                "note": "确保所有通行方式都能正常使用后才能投入运营。"
            }
        ]
        
        for idx, step in enumerate(steps, 1):
            # 步骤标题
            heading = self.doc.add_heading(step['title'], level=2)
            heading_run = heading.runs[0]
            heading_run.font.color.rgb = RGBColor(68, 114, 196)
            
            # 操作内容
            p = self.doc.add_paragraph()
            p.add_run('操作步骤: ').font.bold = True
            p.add_run(step['content'])
            
            # 注意事项
            if step.get('note'):
                p = self.doc.add_paragraph()
                p.add_run('注意事项: ').font.bold = True
                note_run = p.add_run(step['note'])
                note_run.font.color.rgb = RGBColor(255, 128, 0)
                note_run.font.italic = True
            
            self.doc.add_paragraph()
        
        # 更新完成检查清单
        self.doc.add_heading('2.1 更新完成检查清单', level=2)
        
        p = self.doc.add_paragraph()
        p.add_run('更新完成后，请逐项检查以下内容：')
        
        checklist = [
            "□ 系统版本号已更新到最新版本",
            "□ 用户信息同步完成",
            "□ 人脸识别功能正常",
            "□ 二维码识别功能正常",
            "□ 刷卡功能正常（如有）",
            "□ 网络连接正常",
            "□ 系统运行稳定，无异常提示"
        ]
        
        for item in checklist:
            p = self.doc.add_paragraph(item)
            p.paragraph_format.left_indent = Inches(0.5)
        
        self.doc.add_paragraph()
    
    def add_login_info(self):
        """添加登录信息"""
        self.doc.add_heading('三、系统登录信息', level=1)
        
        # 安全提示
        p = self.doc.add_paragraph()
        p.add_run('安全提示: ').font.bold = True
        security_note = p.add_run('以下为系统管理员账号，请妥善保管，不得泄露给无关人员。')
        security_note.font.color.rgb = RGBColor(255, 0, 0)
        security_note.font.bold = True
        
        self.doc.add_paragraph()
        
        # 登录信息表格
        table = self.doc.add_table(rows=3, cols=2)
        table.style = 'Light Grid Accent 1'
        
        table.rows[0].cells[0].text = '项目'
        table.rows[0].cells[1].text = '信息'
        
        for cell in table.rows[0].cells:
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        table.rows[1].cells[0].text = '登录账号'
        account_cell = table.rows[1].cells[1]
        account_cell.text = '13064767168'
        account_cell.paragraphs[0].runs[0].font.bold = True
        
        table.rows[2].cells[0].text = '登录密码'
        password_cell = table.rows[2].cells[1]
        password_cell.text = 'Zaji@@1234'
        password_cell.paragraphs[0].runs[0].font.bold = True
        password_cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 0, 0)
        
        self.doc.add_paragraph()
        
        # 使用说明
        self.doc.add_heading('3.1 使用说明', level=2)
        
        usage_notes = [
            "该账号用于闸机系统管理和维护操作",
            "登录后可进行系统设置、数据同步等操作",
            "请定期修改密码以确保系统安全",
            "如需修改密码，请及时通知相关维护人员"
        ]
        
        for note in usage_notes:
            p = self.doc.add_paragraph(f'• {note}')
            p.paragraph_format.left_indent = Inches(0.25)
        
        self.doc.add_paragraph()
    
    def add_remote_operation(self):
        """添加远程操作方法"""
        self.doc.add_heading('四、远程操作方法', level=1)
        
        p = self.doc.add_paragraph()
        p.add_run('当知道闸机IP地址时，可以使用远程工具连接闸机进行操作，无需现场操作。')
        
        self.doc.add_paragraph()
        
        # 远程工具信息
        self.doc.add_heading('4.1 远程工具', level=2)
        
        table = self.doc.add_table(rows=4, cols=2)
        table.style = 'Light Grid Accent 1'
        
        table.rows[0].cells[0].text = '项目'
        table.rows[0].cells[1].text = '信息'
        
        for cell in table.rows[0].cells:
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        table.rows[1].cells[0].text = '工具名称'
        table.rows[1].cells[1].text = 'scrcpy'
        
        table.rows[2].cells[0].text = '版本'
        table.rows[2].cells[1].text = 'scrcpy-win64-v2.3.1'
        
        table.rows[3].cells[0].text = '文件'
        table.rows[3].cells[1].text = 'scrcpy-win64-v2.3.1.7z'
        
        self.doc.add_paragraph()
        
        # 远程连接步骤
        self.doc.add_heading('4.2 远程连接步骤', level=2)
        
        remote_steps = [
            {
                "step": "确认网络连接",
                "desc": "确保操作电脑与闸机在同一网络环境下，或可通过VPN访问闸机网络"
            },
            {
                "step": "获取闸机IP地址",
                "desc": "从系统管理员处获取目标闸机的IP地址"
            },
            {
                "step": "解压并运行工具",
                "desc": "解压scrcpy-win64-v2.3.1.7z文件，运行scrcpy.exe"
            },
            {
                "step": "连接闸机",
                "desc": "在命令行中输入：scrcpy -s <闸机IP地址>:5555"
            },
            {
                "step": "开始远程操作",
                "desc": "连接成功后，即可在电脑上远程控制闸机进行操作"
            }
        ]
        
        for idx, step in enumerate(remote_steps, 1):
            p = self.doc.add_paragraph()
            p.add_run(f'{idx}. {step["step"]}: ').font.bold = True
            p.add_run(step["desc"])
        
        self.doc.add_paragraph()
        
        # 远程操作优势
        self.doc.add_heading('4.3 远程操作优势', level=2)
        
        advantages = [
            "无需现场操作，节省时间和人力成本",
            "可以同时管理多台闸机",
            "便于故障排查和问题定位",
            "支持远程更新和维护",
            "可记录操作过程，便于后续分析"
        ]
        
        for advantage in advantages:
            p = self.doc.add_paragraph(f'✓ {advantage}', style='List Bullet')
            p.paragraph_format.left_indent = Inches(0.5)
            p.runs[0].font.color.rgb = RGBColor(0, 128, 0)
        
        self.doc.add_paragraph()
    
    def add_precautions(self):
        """添加注意事项"""
        self.doc.add_heading('五、注意事项', level=1)
        
        # 安全注意事项
        self.doc.add_heading('5.1 安全注意事项', level=2)
        
        safety_items = [
            "更新操作必须由专业技术人员或经过培训的人员执行",
            "更新前务必备份重要数据和配置信息",
            "更新过程中不要断电或强制关机",
            "系统账号密码需严格保密，定期更换",
            "远程操作时确保网络连接稳定可靠"
        ]
        
        for item in safety_items:
            p = self.doc.add_paragraph(f'⚠ {item}')
            p.paragraph_format.left_indent = Inches(0.25)
            p.runs[0].font.color.rgb = RGBColor(255, 128, 0)
        
        self.doc.add_paragraph()
        
        # 操作建议
        self.doc.add_heading('5.2 操作建议', level=2)
        
        suggestions = [
            "选择系统空闲时段（如深夜或非营业时间）进行更新",
            "更新前告知相关人员，避免影响正常业务",
            "保持与供应商技术支持的沟通渠道畅通",
            "记录每次更新的时间、版本号和操作人员",
            "发现异常情况及时联系供应商技术支持"
        ]
        
        for suggestion in suggestions:
            p = self.doc.add_paragraph(f'• {suggestion}')
            p.paragraph_format.left_indent = Inches(0.25)
        
        self.doc.add_paragraph()
    
    def add_troubleshooting(self):
        """添加故障排查"""
        self.doc.add_heading('六、常见问题处理', level=1)
        
        problems = [
            {
                "problem": "更新失败或卡住",
                "solution": "重启闸机，重新执行更新流程；如仍失败，联系供应商技术支持"
            },
            {
                "problem": "人脸识别不工作",
                "solution": "检查数据同步是否完成；重新登录系统；清理摄像头镜头"
            },
            {
                "problem": "二维码无法识别",
                "solution": "检查扫描器是否正常工作；调整扫描区域光线；重启闸机"
            },
            {
                "problem": "无法登录系统",
                "solution": "确认账号密码正确；检查网络连接；联系供应商重置密码"
            },
            {
                "problem": "远程连接失败",
                "solution": "确认IP地址正确；检查网络连接；确认闸机端口5555已开放"
            }
        ]
        
        for idx, item in enumerate(problems, 1):
            self.doc.add_heading(f'6.{idx} {item["problem"]}', level=2)
            
            p = self.doc.add_paragraph()
            p.add_run('解决方案: ').font.bold = True
            p.add_run(item["solution"])
            
            self.doc.add_paragraph()
    
    def add_contact(self):
        """添加联系方式"""
        self.doc.add_heading('七、技术支持', level=1)
        
        p = self.doc.add_paragraph()
        p.add_run('如遇到无法解决的问题，请及时联系供应商技术支持。')
        
        self.doc.add_paragraph()
        
        # 联系信息表格
        table = self.doc.add_table(rows=3, cols=2)
        table.style = 'Light Grid Accent 1'
        
        table.rows[0].cells[0].text = '项目'
        table.rows[0].cells[1].text = '信息'
        
        for cell in table.rows[0].cells:
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        table.rows[1].cells[0].text = '供应商'
        table.rows[1].cells[1].text = '亿思维科技有限公司'
        
        table.rows[2].cells[0].text = '服务内容'
        table.rows[2].cells[1].text = '闸机维护、软件更新、故障排查、技术咨询'
        
        self.doc.add_paragraph()
        
        # 报告信息
        p = self.doc.add_paragraph()
        p.add_run('文档版本: ').font.bold = True
        p.add_run('v1.0')
        
        p = self.doc.add_paragraph()
        p.add_run('更新日期: ').font.bold = True
        p.add_run('2023-11-05')
        
        self.doc.add_paragraph()
    
    def generate(self):
        """生成文档"""
        print("\n" + "="*60)
        print("生成闸机维护与更新操作手册")
        print("="*60)
        
        print("\n添加标题...")
        self.add_title()
        
        print("添加文档说明...")
        self.add_overview()
        
        print("添加更新流程...")
        self.add_update_process()
        
        print("添加登录信息...")
        self.add_login_info()
        
        print("添加远程操作方法...")
        self.add_remote_operation()
        
        print("添加注意事项...")
        self.add_precautions()
        
        print("添加故障排查...")
        self.add_troubleshooting()
        
        print("添加技术支持...")
        self.add_contact()
        
        # 保存文档
        self.doc.save(OUTPUT_FILE)
        print(f"\n✓ 文档已生成: {OUTPUT_FILE}")
        print(f"  供应商: 亿思维科技有限公司")
        print(f"  内容: 闸机更新流程、登录信息、远程操作方法")
        print("="*60 + "\n")
        
        return OUTPUT_FILE

def main():
    generator = GateMaintenanceDocGenerator()
    generator.generate()

if __name__ == "__main__":
    main()
