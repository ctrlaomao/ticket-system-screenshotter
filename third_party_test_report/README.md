# 第三方平台对接配置测试

## 📋 项目说明

本项目用于自动化查看票务系统中美团、携程、抖音三个第三方平台的对接配置信息，并生成专业的测试报告。

## 🎯 测试范围

1. **美团平台** - 查看回调域名、IP白名单等配置
2. **携程平台** - 查看回调域名、IP白名单等配置  
3. **抖音平台** - 查看连调配置信息

## 📁 文件结构

```
third_party_test_report/
├── README.md                          # 项目说明文档
├── run_test.py                        # 主运行脚本
├── test_third_party_platforms.py      # 自动化测试脚本
├── generate_test_report.py            # 报告生成脚本
├── screenshots/                       # 截图保存目录
├── test_result.json                   # 测试结果数据
└── 第三方平台对接测试报告.docx        # 最终测试报告
```

## 🔧 环境要求

- Python 3.7+
- 依赖包：
  - playwright
  - python-docx

## 📦 安装依赖

```bash
# 安装Python依赖
pip install playwright python-docx

# 安装Playwright浏览器
playwright install chromium
```

## 🚀 使用方法

### 方法一：一键运行（推荐）

```bash
cd /workspace/third_party_test_report
python run_test.py
```

### 方法二：分步执行

```bash
# 步骤1: 执行测试（登录系统并查找配置）
python test_third_party_platforms.py

# 步骤2: 生成报告
python generate_test_report.py
```

## 📊 输出文件

执行完成后，将生成以下文件：

1. **测试报告** - `第三方平台对接测试报告.docx`
   - Word格式专业报告
   - 包含配置截图和详细说明
   
2. **测试截图** - `screenshots/` 目录
   - 各平台配置页面截图
   - PNG格式，高清晰度

3. **测试数据** - `test_result.json`
   - JSON格式测试结果
   - 可用于后续分析

## 📝 配置说明

测试脚本从 `/workspace/config.json` 读取系统登录信息：

```json
{
  "login": {
    "url": "https://xs.bjstarfish.com/Account/Login",
    "base_url": "https://xs.bjstarfish.com",
    "username": "13811458301",
    "password": "Qaaaaa8080@",
    "language": "zh-CN"
  }
}
```

## ⚙️ 工作流程

1. **登录系统**
   - 使用配置的账号自动登录
   - 选择简体中文语言

2. **查找配置页面**
   - 遍历系统菜单查找美团、携程、抖音相关配置
   - 尝试访问常见配置路径

3. **截图保存**
   - 对找到的配置页面进行全页截图
   - 自动保存到screenshots目录

4. **生成报告**
   - 创建专业Word格式报告
   - 包含测试信息、截图、结论和建议

## 🔍 常见问题

### Q: 找不到配置页面怎么办？
A: 脚本会尝试多个可能的路径。如果未找到，可能需要：
- 检查账号权限
- 手动确认配置页面位置
- 联系系统管理员

### Q: 截图失败怎么办？
A: 检查：
- screenshots目录是否有写入权限
- 浏览器是否正常启动
- 页面是否正确加载

### Q: 如何调试？
A: 编辑 `test_third_party_platforms.py`，修改：
```python
browser = p.chromium.launch(headless=False)  # 显示浏览器窗口
```

## 📞 支持

如遇问题，请检查：
1. 网络连接是否正常
2. 系统登录信息是否正确
3. Python依赖是否完整安装

## 📄 许可

内部测试工具，仅供项目使用。

---

**最后更新**: 2025-11-03
**版本**: 1.0.0
