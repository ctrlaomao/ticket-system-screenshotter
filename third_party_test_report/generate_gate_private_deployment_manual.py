#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成闸机系统私有化部署手册
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

OUTPUT_FILE = "/workspace/third_party_test_report/闸机系统私有化部署手册.docx"

class GatePrivateDeploymentManualGenerator:
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
        title = self.doc.add_heading('闸机系统私有化部署手册', 0)
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
        p.add_run('本文档用于指导闸机系统的私有化部署实施，包含完整的部署流程、系统配置、数据初始化和验收标准。')
        
        self.doc.add_paragraph()
        
        # 私有化部署说明
        self.doc.add_heading('1.1 私有化部署概述', level=2)
        
        p = self.doc.add_paragraph()
        p.add_run('私有化部署是指将闸机系统完全部署在客户自有的服务器和网络环境中，确保数据安全、系统独立运行、完全自主可控。')
        
        self.doc.add_paragraph()
        
        deployment_features = [
            "数据私有：所有业务数据存储在客户自有服务器，确保数据安全",
            "系统独立：闸机系统独立运行，不依赖外部云服务",
            "完全可控：客户拥有系统完整控制权，可自主管理维护",
            "定制化强：可根据客户需求进行系统定制和功能扩展",
            "内网部署：支持完全内网环境部署，无需连接互联网"
        ]
        
        for feature in deployment_features:
            p = self.doc.add_paragraph(f'• {feature}')
            p.paragraph_format.left_indent = Inches(0.25)
        
        self.doc.add_paragraph()
        
        # 供应商信息
        self.doc.add_heading('1.2 供应商信息', level=2)
        
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
        table.rows[2].cells[1].text = '私有化部署实施、系统配置、技术支持、运维培训'
        
        self.doc.add_paragraph()
    
    def add_deployment_preparation(self):
        """添加部署准备"""
        self.doc.add_heading('二、部署准备', level=1)
        
        # 硬件要求
        self.doc.add_heading('2.1 硬件要求', level=2)
        
        p = self.doc.add_paragraph()
        p.add_run('闸机硬件配置要求：')
        
        hardware_requirements = [
            "操作系统：Android 5.0或以上版本",
            "处理器：四核以上处理器",
            "内存：2GB RAM或以上",
            "存储：16GB ROM或以上",
            "网络：支持WiFi或以太网连接",
            "显示：触摸屏显示器",
            "外设：人脸识别摄像头、二维码扫描器"
        ]
        
        for req in hardware_requirements:
            p = self.doc.add_paragraph(f'• {req}')
            p.paragraph_format.left_indent = Inches(0.5)
        
        self.doc.add_paragraph()
        
        # 网络要求
        self.doc.add_heading('2.2 网络要求', level=2)
        
        network_requirements = [
            "闸机设备需要与服务器在同一局域网内",
            "网络带宽建议10Mbps或以上",
            "需要固定IP地址或DHCP保留地址",
            "防火墙需开放必要端口（5555、8080等）",
            "建议配置独立网段，与其他业务网络隔离"
        ]
        
        for req in network_requirements:
            p = self.doc.add_paragraph(f'• {req}')
            p.paragraph_format.left_indent = Inches(0.25)
        
        self.doc.add_paragraph()
        
        # 软件准备
        self.doc.add_heading('2.3 软件准备', level=2)
        
        p = self.doc.add_paragraph()
        p.add_run('部署所需软件包（由供应商提供）：')
        
        software_list = [
            "闸机系统APK安装包",
            "系统配置文件",
            "数据库初始化脚本",
            "远程管理工具（scrcpy-win64-v2.3.1.7z）",
            "部署文档和操作手册"
        ]
        
        for software in software_list:
            p = self.doc.add_paragraph(f'• {software}')
            p.paragraph_format.left_indent = Inches(0.5)
        
        self.doc.add_paragraph()
    
    def add_deployment_process(self):
        """添加部署流程"""
        self.doc.add_heading('三、私有化部署流程', level=1)
        
        p = self.doc.add_paragraph()
        p.add_run('重要提示: ').font.bold = True
        warning = p.add_run('部署过程需要由专业技术人员执行，确保按照步骤顺序进行，避免出现配置错误。')
        warning.font.color.rgb = RGBColor(255, 128, 0)
        warning.font.italic = True
        
        self.doc.add_paragraph()
        
        # 部署步骤
        steps = [
            {
                "title": "步骤一：环境检查",
                "content": "检查闸机硬件状态、网络连接、IP地址配置等，确保所有环境准备就绪。记录闸机设备的IP地址、MAC地址等信息。",
                "note": "环境检查是部署的基础，务必确认所有条件满足后再进行下一步。"
            },
            {
                "title": "步骤二：系统安装",
                "content": "将闸机系统APK安装包传输到设备，执行安装。可通过USB优盘或网络传输方式。安装过程中确保设备电量充足。",
                "note": "安装过程可能需要几分钟，请耐心等待，不要中断安装。"
            },
            {
                "title": "步骤三：基础配置",
                "content": "首次启动系统后，配置服务器地址、设备编号、通讯端口等基础信息。这些配置信息由系统管理员提供。",
                "note": "配置信息必须准确无误，否则会导致系统无法正常通讯。"
            },
            {
                "title": "步骤四：账号登录",
                "content": "使用管理员账号登录系统。账号信息由供应商提供，首次登录后建议修改密码。",
                "note": "管理员账号密码需妥善保管，避免泄露。"
            },
            {
                "title": "步骤五：数据同步",
                "content": "登录后系统自动从服务器同步基础数据，包括用户信息、人脸库、产品信息、权限配置等。同步时间根据数据量而定。",
                "note": "数据同步过程中不要操作系统，等待同步完成。"
            },
            {
                "title": "步骤六：功能测试",
                "content": "数据同步完成后，测试人脸识别、二维码扫描、刷卡等核心功能，确保所有通行方式正常工作。",
                "note": "测试时使用真实数据进行验证，确保识别准确率。"
            },
            {
                "title": "步骤七：系统优化",
                "content": "根据实际使用情况，调整系统参数，如识别灵敏度、闸机开关速度、屏幕亮度等，优化用户体验。",
                "note": "优化参数需要在实际运行中不断调整。"
            },
            {
                "title": "步骤八：验收交付",
                "content": "完成所有配置和测试后，进行系统验收，填写验收单，正式交付使用。同时进行操作培训。",
                "note": "验收标准见本文档第四章内容。"
            }
        ]
        
        for idx, step in enumerate(steps, 1):
            # 步骤标题
            heading = self.doc.add_heading(step['title'], level=2)
            heading_run = heading.runs[0]
            heading_run.font.color.rgb = RGBColor(68, 114, 196)
            
            # 操作内容
            p = self.doc.add_paragraph()
            p.add_run('操作内容: ').font.bold = True
            p.add_run(step['content'])
            
            # 注意事项
            if step.get('note'):
                p = self.doc.add_paragraph()
                p.add_run('注意事项: ').font.bold = True
                note_run = p.add_run(step['note'])
                note_run.font.color.rgb = RGBColor(255, 128, 0)
                note_run.font.italic = True
            
            self.doc.add_paragraph()
    
    def add_system_configuration(self):
        """添加系统配置"""
        self.doc.add_heading('四、系统配置说明', level=1)
        
        # 服务器配置
        self.doc.add_heading('4.1 服务器配置', level=2)
        
        p = self.doc.add_paragraph()
        p.add_run('服务器地址: ').font.bold = True
        p.add_run('票务系统服务器地址（xs.bjstarfish.com）')
        
        p = self.doc.add_paragraph()
        p.add_run('通讯协议: ').font.bold = True
        p.add_run('HTTPS/HTTP')
        
        p = self.doc.add_paragraph()
        p.add_run('数据格式: ').font.bold = True
        p.add_run('JSON')
        
        self.doc.add_paragraph()
        
        # 账号配置
        self.doc.add_heading('4.2 系统账号信息', level=2)
        
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
        account_cell.text = '130****7168'
        account_cell.paragraphs[0].runs[0].font.bold = True
        
        table.rows[2].cells[0].text = '登录密码'
        password_cell = table.rows[2].cells[1]
        password_cell.text = '********'
        password_cell.paragraphs[0].runs[0].font.bold = True
        password_cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(128, 128, 128)
        
        self.doc.add_paragraph()
        
        # 脱敏说明
        p = self.doc.add_paragraph()
        p.add_run('说明: ').font.bold = True
        note_run = p.add_run('上述账号信息已脱敏处理。完整账号密码由系统管理员和供应商维护人员掌握，如需获取请联系相关负责人。')
        note_run.font.color.rgb = RGBColor(255, 128, 0)
        note_run.font.italic = True
        
        self.doc.add_paragraph()
        
        # 设备配置
        self.doc.add_heading('4.3 设备参数配置', level=2)
        
        device_params = [
            "设备编号：根据实际部署位置分配唯一编号",
            "识别模式：人脸识别、二维码、刷卡等",
            "通行规则：单向/双向、是否需要验票等",
            "工作时间：营业时间段设置",
            "离线模式：网络中断时的处理策略"
        ]
        
        for param in device_params:
            p = self.doc.add_paragraph(f'• {param}')
            p.paragraph_format.left_indent = Inches(0.25)
        
        self.doc.add_paragraph()
    
    def add_remote_management(self):
        """添加远程管理"""
        self.doc.add_heading('五、远程管理方法', level=1)
        
        p = self.doc.add_paragraph()
        p.add_run('私有化部署后，支持通过远程工具对闸机进行管理和维护，无需现场操作。')
        
        self.doc.add_paragraph()
        
        # 远程工具信息
        self.doc.add_heading('5.1 远程工具', level=2)
        
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
        self.doc.add_heading('5.2 远程连接方法', level=2)
        
        remote_steps = [
            {
                "step": "确认网络连接",
                "desc": "确保管理电脑与闸机在同一局域网内，或可通过VPN访问闸机网络"
            },
            {
                "step": "获取闸机IP地址",
                "desc": "从部署记录中查询目标闸机的IP地址"
            },
            {
                "step": "运行远程工具",
                "desc": "解压scrcpy工具包，运行scrcpy.exe"
            },
            {
                "step": "建立远程连接",
                "desc": "在命令行输入：scrcpy -s <闸机IP地址>:5555 连接设备"
            },
            {
                "step": "远程操作管理",
                "desc": "连接成功后，可在电脑上远程查看和控制闸机"
            }
        ]
        
        for idx, step in enumerate(remote_steps, 1):
            p = self.doc.add_paragraph()
            p.add_run(f'{idx}. {step["step"]}: ').font.bold = True
            p.add_run(step["desc"])
        
        self.doc.add_paragraph()
    
    def add_acceptance_criteria(self):
        """添加验收标准"""
        self.doc.add_heading('六、验收标准', level=1)
        
        p = self.doc.add_paragraph()
        p.add_run('私有化部署完成后，需要进行全面验收，确保系统满足以下标准：')
        
        self.doc.add_paragraph()
        
        # 验收清单
        self.doc.add_heading('6.1 功能验收清单', level=2)
        
        checklist = [
            "□ 系统安装完成，可以正常启动",
            "□ 服务器连接正常，通讯稳定",
            "□ 管理员账号可以正常登录",
            "□ 基础数据同步完成且准确",
            "□ 人脸识别功能正常，识别率达标",
            "□ 二维码扫描功能正常",
            "□ 刷卡功能正常（如有）",
            "□ 通行规则配置正确，逻辑准确",
            "□ 闸机开关动作正常",
            "□ 数据上传下载正常",
            "□ 离线模式工作正常",
            "□ 远程管理工具可以连接",
            "□ 系统运行稳定，无异常报错",
            "□ 操作人员培训完成"
        ]
        
        for item in checklist:
            p = self.doc.add_paragraph(item)
            p.paragraph_format.left_indent = Inches(0.5)
            p.runs[0].font.size = Pt(11)
        
        self.doc.add_paragraph()
        
        # 性能指标
        self.doc.add_heading('6.2 性能指标', level=2)
        
        performance = [
            "人脸识别准确率：≥98%",
            "人脸识别速度：≤2秒",
            "二维码识别速度：≤1秒",
            "闸机开关时间：1-2秒",
            "数据同步延迟：≤3秒",
            "系统响应时间：≤1秒",
            "7×24小时稳定运行"
        ]
        
        for metric in performance:
            p = self.doc.add_paragraph(f'• {metric}')
            p.paragraph_format.left_indent = Inches(0.25)
            p.runs[0].font.bold = True
            p.runs[0].font.color.rgb = RGBColor(0, 128, 0)
        
        self.doc.add_paragraph()
        
        # 验收签字
        p = self.doc.add_paragraph()
        p.add_run('部署单位: ').font.bold = True
        p.add_run('_______________    ')
        p.add_run('验收日期: ').font.bold = True
        p.add_run('_______________')
        
        p = self.doc.add_paragraph()
        p.add_run('供应商: ').font.bold = True
        p.add_run('_______________    ')
        p.add_run('实施人员: ').font.bold = True
        p.add_run('_______________')
        
        self.doc.add_paragraph()
    
    def add_maintenance_and_support(self):
        """添加运维支持"""
        self.doc.add_heading('七、运维与技术支持', level=1)
        
        # 日常运维
        self.doc.add_heading('7.1 日常运维', level=2)
        
        maintenance_items = [
            "每日检查系统运行状态，确认无异常",
            "定期清理系统日志和缓存文件",
            "定期检查网络连接和服务器通讯",
            "定期更新人脸库等基础数据",
            "定期检查硬件设备状态（摄像头、扫描器等）",
            "做好系统运行记录和故障记录"
        ]
        
        for item in maintenance_items:
            p = self.doc.add_paragraph(f'• {item}')
            p.paragraph_format.left_indent = Inches(0.25)
        
        self.doc.add_paragraph()
        
        # 技术支持
        self.doc.add_heading('7.2 技术支持', level=2)
        
        p = self.doc.add_paragraph()
        p.add_run('供应商提供以下技术支持服务：')
        
        support_services = [
            "7×24小时技术热线支持",
            "远程技术支持和故障排查",
            "定期巡检和系统优化",
            "系统版本升级服务",
            "操作培训和技术指导",
            "应急响应和现场支持"
        ]
        
        for service in support_services:
            p = self.doc.add_paragraph(f'✓ {service}')
            p.paragraph_format.left_indent = Inches(0.5)
            p.runs[0].font.color.rgb = RGBColor(0, 128, 0)
        
        self.doc.add_paragraph()
        
        # 联系信息
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
        table.rows[2].cells[1].text = '私有化部署、系统维护、技术支持、培训服务'
        
        self.doc.add_paragraph()
        
        # 文档信息
        p = self.doc.add_paragraph()
        p.add_run('文档版本: ').font.bold = True
        p.add_run('v1.0')
        
        p = self.doc.add_paragraph()
        p.add_run('发布日期: ').font.bold = True
        p.add_run('2023-11-05')
        
        self.doc.add_paragraph()
    
    def generate(self):
        """生成文档"""
        print("\n" + "="*60)
        print("生成闸机系统私有化部署手册")
        print("="*60)
        
        print("\n添加标题...")
        self.add_title()
        
        print("添加文档说明...")
        self.add_overview()
        
        print("添加部署准备...")
        self.add_deployment_preparation()
        
        print("添加部署流程...")
        self.add_deployment_process()
        
        print("添加系统配置...")
        self.add_system_configuration()
        
        print("添加远程管理...")
        self.add_remote_management()
        
        print("添加验收标准...")
        self.add_acceptance_criteria()
        
        print("添加运维支持...")
        self.add_maintenance_and_support()
        
        # 保存文档
        self.doc.save(OUTPUT_FILE)
        print(f"\n✓ 文档已生成: {OUTPUT_FILE}")
        print(f"  部署日期: 2023-11-05")
        print(f"  供应商: 亿思维科技有限公司")
        print(f"  内容: 私有化部署流程、系统配置、验收标准、运维支持")
        print("="*60 + "\n")
        
        return OUTPUT_FILE

def main():
    generator = GatePrivateDeploymentManualGenerator()
    generator.generate()

if __name__ == "__main__":
    main()
