#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成租赁设备私有化部署手册
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

OUTPUT_FILE = "/workspace/third_party_test_report/租赁设备私有化部署手册.docx"

class RentalPrivateDeploymentManualGenerator:
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
        title = self.doc.add_heading('租赁设备私有化部署手册', 0)
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
        p.add_run('本手册用于指导租赁设备客户端的私有化部署实施，确保租赁设备能够在客户私有环境中正常运行并与票务系统安全对接。')
        
        self.doc.add_paragraph()
        
        # 私有化部署说明
        self.doc.add_heading('1.1 私有化部署概述', level=2)
        
        p = self.doc.add_paragraph()
        p.add_run('私有化部署是指将租赁设备客户端完全部署在客户内网环境中，所有业务数据在客户自有服务器处理，确保数据安全、业务自主、系统可控。')
        
        self.doc.add_paragraph()
        
        deployment_features = [
            "数据安全：租赁业务数据完全存储在客户私有服务器",
            "内网运行：设备在内网环境运行，无需外网访问",
            "业务自主：客户完全掌控租赁业务流程和数据",
            "系统集成：与票务系统无缝对接，数据实时同步",
            "灵活扩展：可根据业务需求灵活增加设备数量"
        ]
        
        for feature in deployment_features:
            p = self.doc.add_paragraph(f'• {feature}')
            p.paragraph_format.left_indent = Inches(0.25)
        
        self.doc.add_paragraph()
        
        # 设备信息
        self.doc.add_heading('1.2 设备信息', level=2)
        
        table = self.doc.add_table(rows=10, cols=2)
        table.style = 'Light Grid Accent 1'
        
        table.rows[0].cells[0].text = '项目'
        table.rows[0].cells[1].text = '信息'
        
        for cell in table.rows[0].cells:
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        table.rows[1].cells[0].text = '应用名称'
        table.rows[1].cells[1].text = '租赁设备客户端'
        
        table.rows[2].cells[0].text = '部署模式'
        table.rows[2].cells[1].text = '私有化部署'
        
        table.rows[3].cells[0].text = '设备品牌'
        table.rows[3].cells[1].text = 'Sunmi (商米)'
        
        table.rows[4].cells[0].text = '设备型号'
        table.rows[4].cells[1].text = 'V2S'
        
        table.rows[5].cells[0].text = '设备数量'
        table.rows[5].cells[1].text = '15台'
        
        table.rows[6].cells[0].text = '适用平台'
        table.rows[6].cells[1].text = 'Android'
        
        table.rows[7].cells[0].text = '供应商'
        table.rows[7].cells[1].text = '亿思维科技有限公司'
        
        table.rows[8].cells[0].text = '部署日期'
        table.rows[8].cells[1].text = '2023-11-05'
        
        table.rows[9].cells[0].text = '对接系统'
        table.rows[9].cells[1].text = '票务系统 (xs.bjstarfish.com)'
        
        self.doc.add_paragraph()
    
    def add_deployment_preparation(self):
        """添加部署准备"""
        self.doc.add_heading('二、部署准备', level=1)
        
        # 设备要求
        self.doc.add_heading('2.1 设备要求', level=2)
        
        requirements = [
            "设备品牌：Sunmi (商米)",
            "设备型号：V2S",
            "Android系统版本：Android 5.0或以上",
            "存储空间：至少100MB可用空间",
            "网络连接：稳定的WiFi或4G/5G网络",
            "屏幕分辨率：建议1280x720或以上",
            "处理器：建议四核以上处理器"
        ]
        
        for req in requirements:
            p = self.doc.add_paragraph(f'• {req}')
            p.paragraph_format.left_indent = Inches(0.25)
        
        self.doc.add_paragraph()
        
        # 网络要求
        self.doc.add_heading('2.2 网络要求', level=2)
        
        network_requirements = [
            "租赁设备需与票务系统服务器在同一内网环境",
            "需要固定IP地址或DHCP保留地址",
            "建议网络带宽5Mbps或以上",
            "防火墙需开放必要端口（8080、443等）",
            "支持内网DNS解析或直接使用IP地址"
        ]
        
        for req in network_requirements:
            p = self.doc.add_paragraph(f'• {req}')
            p.paragraph_format.left_indent = Inches(0.25)
        
        self.doc.add_paragraph()
        
        # 软件准备
        self.doc.add_heading('2.3 软件准备', level=2)
        
        p = self.doc.add_paragraph()
        p.add_run('部署所需软件（由供应商提供）：')
        
        software_list = [
            "租赁设备客户端APK安装包（最新版本）",
            "系统配置文件",
            "部署文档和操作手册",
            "测试数据和测试用例"
        ]
        
        for software in software_list:
            p = self.doc.add_paragraph(f'• {software}')
            p.paragraph_format.left_indent = Inches(0.5)
        
        self.doc.add_paragraph()
        
        p = self.doc.add_paragraph()
        p.add_run('重要提示: ').font.bold = True
        warning = p.add_run('请确保从供应商官方渠道获取安装包，不要使用来历不明的APK文件，以确保系统安全。')
        warning.font.color.rgb = RGBColor(255, 0, 0)
        warning.font.bold = True
        
        self.doc.add_paragraph()
    
    def add_deployment_process(self):
        """添加部署流程"""
        self.doc.add_heading('三、私有化部署流程', level=1)
        
        p = self.doc.add_paragraph()
        p.add_run('请按照以下步骤完成租赁设备的私有化部署：')
        
        self.doc.add_paragraph()
        
        steps = [
            {
                "title": "步骤一：设备检查",
                "content": "检查所有租赁设备硬件状态，确认设备型号、序列号，记录设备MAC地址和预分配的IP地址。清点设备数量（15台），确保无遗漏。",
                "note": "设备信息将用于系统配置和资产管理，务必准确记录。"
            },
            {
                "title": "步骤二：网络配置",
                "content": "为每台设备配置网络连接，连接到内网WiFi或配置有线网络。确认设备可以访问票务系统服务器，测试网络连通性。",
                "note": "建议使用固定IP地址，便于管理和故障排查。"
            },
            {
                "title": "步骤三：安装应用程序",
                "content": "通过USB优盘或内网文件共享方式，将APK安装包传输到设备。进入设置允许安装未知来源应用，然后安装租赁设备客户端。",
                "note": "批量部署时可以先在一台设备上测试成功后再进行批量安装。"
            },
            {
                "title": "步骤四：系统配置",
                "content": "首次启动应用后，配置服务器地址（xs.bjstarfish.com或内网服务器IP）、设备编号、租赁点名称等基本信息。",
                "note": "每台设备的设备编号必须唯一，不能重复。"
            },
            {
                "title": "步骤五：账号登录",
                "content": "使用分配的账号密码登录系统。首次登录时系统会自动同步租赁产品信息、库存数据、价格策略等基础数据。",
                "note": "首次登录需要联网，同步时间取决于数据量，通常需要1-5分钟。"
            },
            {
                "title": "步骤六：功能测试",
                "content": "测试租赁下单、设备归还、库存查询、订单查询、支付功能等核心业务功能，确保所有功能正常。",
                "note": "建议使用测试数据进行完整业务流程测试。"
            },
            {
                "title": "步骤七：数据验证",
                "content": "验证设备上的租赁产品信息、库存数量、价格信息是否与服务器一致，确认数据同步准确无误。",
                "note": "数据准确性直接影响业务运营，必须仔细核对。"
            },
            {
                "title": "步骤八：培训与交付",
                "content": "对操作人员进行系统使用培训，包括租赁流程、异常处理、日常维护等。完成验收后正式交付使用。",
                "note": "操作人员培训是部署成功的关键，需确保培训到位。"
            }
        ]
        
        for idx, step in enumerate(steps, 1):
            # 步骤标题
            heading = self.doc.add_heading(step['title'], level=2)
            heading_run = heading.runs[0]
            heading_run.font.color.rgb = RGBColor(68, 114, 196)
            
            # 操作内容
            p = self.doc.add_paragraph()
            p.add_run('操作说明: ').font.bold = True
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
        p.add_run('xs.bjstarfish.com（或内网服务器IP地址）')
        
        p = self.doc.add_paragraph()
        p.add_run('通讯协议: ').font.bold = True
        p.add_run('HTTPS')
        
        p = self.doc.add_paragraph()
        p.add_run('数据格式: ').font.bold = True
        p.add_run('JSON')
        
        p = self.doc.add_paragraph()
        p.add_run('同步频率: ').font.bold = True
        p.add_run('实时同步（每笔业务）+ 定时同步（每30分钟）')
        
        self.doc.add_paragraph()
        
        # 业务配置
        self.doc.add_heading('4.2 业务配置', level=2)
        
        business_config = [
            "租赁点信息：租赁点名称、位置、营业时间",
            "产品信息：租赁产品列表、分类、价格策略",
            "库存管理：初始库存、安全库存、库存预警",
            "计费规则：按小时/按天计费、押金规则、优惠规则",
            "支付方式：现金、微信、支付宝、会员卡等",
            "打印设置：小票打印、订单打印（如需要）"
        ]
        
        for config in business_config:
            p = self.doc.add_paragraph(f'• {config}')
            p.paragraph_format.left_indent = Inches(0.25)
        
        self.doc.add_paragraph()
        
        # 设备参数
        self.doc.add_heading('4.3 设备参数配置', level=2)
        
        device_params = [
            "设备编号：每台设备唯一编号（如：ZL001-ZL015）",
            "设备名称：便于识别的设备名称",
            "所属租赁点：设备归属的租赁点",
            "操作员账号：分配给该设备的操作员账号",
            "离线模式：网络中断时的业务处理策略"
        ]
        
        for param in device_params:
            p = self.doc.add_paragraph(f'• {param}')
            p.paragraph_format.left_indent = Inches(0.25)
        
        self.doc.add_paragraph()
    
    def add_function_introduction(self):
        """添加功能介绍"""
        self.doc.add_heading('五、核心功能介绍', level=1)
        
        p = self.doc.add_paragraph()
        p.add_run('租赁设备客户端主要功能模块：')
        
        self.doc.add_paragraph()
        
        functions = [
            {
                "name": "租赁下单",
                "desc": "支持现场租赁下单，选择租赁产品、数量、时长，计算租金和押金，生成租赁订单，支持多种支付方式"
            },
            {
                "name": "设备归还",
                "desc": "处理租赁设备归还，扫描订单二维码或输入订单号，自动计算实际租赁时长和费用，处理押金退还"
            },
            {
                "name": "库存管理",
                "desc": "实时查看设备库存情况，包括可租数量、已租数量、损坏数量，支持库存盘点和调整"
            },
            {
                "name": "订单查询",
                "desc": "查询租赁订单信息，包括订单状态、租赁时长、费用明细，支持订单补打印和退款"
            },
            {
                "name": "数据同步",
                "desc": "与票务系统实时同步数据，确保产品信息、库存数据、订单数据的一致性"
            },
            {
                "name": "报表统计",
                "desc": "查看日报表、月报表，统计租赁收入、设备使用率等经营数据"
            }
        ]
        
        for func in functions:
            self.doc.add_heading(f'• {func["name"]}', level=2)
            p = self.doc.add_paragraph(func["desc"])
            p.paragraph_format.left_indent = Inches(0.25)
        
        self.doc.add_paragraph()
    
    def add_acceptance_criteria(self):
        """添加验收标准"""
        self.doc.add_heading('六、部署验收标准', level=1)
        
        p = self.doc.add_paragraph()
        p.add_run('私有化部署完成后，请逐项检查以下内容，确保系统满足验收标准：')
        
        self.doc.add_paragraph()
        
        # 验收清单
        checklist = [
            "□ 所有设备（15台）已成功安装应用程序",
            "□ 所有设备可以正常启动，无崩溃现象",
            "□ 网络连接正常，可以访问服务器",
            "□ 所有设备登录功能正常",
            "□ 租赁产品信息已同步且准确",
            "□ 库存数据显示正确，与服务器一致",
            "□ 租赁下单功能正常，订单生成准确",
            "□ 设备归还功能正常，费用计算准确",
            "□ 支付功能正常（所有支付方式）",
            "□ 订单查询功能正常",
            "□ 打印功能正常（如有）",
            "□ 数据同步正常，实时性满足要求",
            "□ 离线模式工作正常（如有）",
            "□ 报表统计功能正常",
            "□ 系统运行流畅，响应及时",
            "□ 操作人员培训完成，能够独立操作"
        ]
        
        for item in checklist:
            p = self.doc.add_paragraph(item)
            p.paragraph_format.left_indent = Inches(0.5)
            p.runs[0].font.size = Pt(11)
        
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
        
        # 日常维护
        self.doc.add_heading('7.1 日常运维', level=2)
        
        maintenance_tasks = [
            {
                "frequency": "每日",
                "tasks": ["检查所有设备运行状态", "确认数据同步正常", "核对库存数据"]
            },
            {
                "frequency": "每周",
                "tasks": ["清理设备缓存", "检查网络连接", "测试核心功能", "备份重要数据"]
            },
            {
                "frequency": "每月",
                "tasks": ["检查应用版本", "全面功能测试", "设备维护保养", "数据统计分析"]
            }
        ]
        
        for task in maintenance_tasks:
            p = self.doc.add_paragraph()
            p.add_run(f'{task["frequency"]}维护: ').font.bold = True
            
            for item in task["tasks"]:
                p = self.doc.add_paragraph(f'• {item}', style='List Bullet')
                p.paragraph_format.left_indent = Inches(0.5)
        
        self.doc.add_paragraph()
        
        # 技术支持
        self.doc.add_heading('7.2 技术支持', level=2)
        
        p = self.doc.add_paragraph()
        p.add_run('供应商提供以下技术支持服务：')
        
        support_services = [
            "技术热线支持（工作时间）",
            "远程技术支持和故障排查",
            "系统版本升级服务",
            "定期巡检和系统优化",
            "操作培训和技术指导",
            "应急响应服务（根据服务协议）"
        ]
        
        for service in support_services:
            p = self.doc.add_paragraph(f'✓ {service}')
            p.paragraph_format.left_indent = Inches(0.5)
            p.runs[0].font.color.rgb = RGBColor(0, 128, 0)
        
        self.doc.add_paragraph()
        
        # 支持信息
        table = self.doc.add_table(rows=4, cols=2)
        table.style = 'Light Grid Accent 1'
        
        table.rows[0].cells[0].text = '项目'
        table.rows[0].cells[1].text = '信息'
        
        for cell in table.rows[0].cells:
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        table.rows[1].cells[0].text = '供应商'
        table.rows[1].cells[1].text = '亿思维科技有限公司'
        
        table.rows[2].cells[0].text = '支持内容'
        table.rows[2].cells[1].text = '私有化部署、系统配置、故障排查、版本更新、培训服务'
        
        table.rows[3].cells[0].text = '支持方式'
        table.rows[3].cells[1].text = '电话支持、远程协助、现场服务'
        
        self.doc.add_paragraph()
        
        # 文档信息
        p = self.doc.add_paragraph()
        p.add_run('文档版本: ').font.bold = True
        p.add_run('v1.0')
        
        p = self.doc.add_paragraph()
        p.add_run('部署日期: ').font.bold = True
        p.add_run('2023-11-05')
        
        p = self.doc.add_paragraph()
        p.add_run('适用版本: ').font.bold = True
        p.add_run('所有租赁设备客户端版本')
        
        self.doc.add_paragraph()
    
    def generate(self):
        """生成文档"""
        print("\n" + "="*60)
        print("生成租赁设备私有化部署手册")
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
        
        print("添加功能介绍...")
        self.add_function_introduction()
        
        print("添加验收标准...")
        self.add_acceptance_criteria()
        
        print("添加运维支持...")
        self.add_maintenance_and_support()
        
        # 保存文档
        self.doc.save(OUTPUT_FILE)
        print(f"\n✓ 文档已生成: {OUTPUT_FILE}")
        print(f"  部署日期: 2023-11-05")
        print(f"  供应商: 亿思维科技有限公司")
        print(f"  设备品牌: Sunmi (商米)")
        print(f"  设备型号: V2S")
        print(f"  设备数量: 15台")
        print(f"  内容: 私有化部署流程、系统配置、验收标准、运维支持")
        print("="*60 + "\n")
        
        return OUTPUT_FILE

def main():
    generator = RentalPrivateDeploymentManualGenerator()
    generator.generate()

if __name__ == "__main__":
    main()
