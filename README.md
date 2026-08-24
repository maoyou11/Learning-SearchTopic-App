# 超星考试客户端工具  


---

- **窗口置顶与防录屏/截屏**：调用`SetWindowDisplayAffinity`，窗口始终置顶且无法被录屏/截屏工具捕获。
- **防止反截图**：使用网上大神的软件`DeAntiCapture.exe`使用`DLL`注入实现防止反截图。
- **模拟键盘输入**：使用软件`AutoHotkey_2.0.26`实现键盘输入。
- **窗口透明度调节**：右键一键切换（0.2/0.5），Ctrl+滚轮精细调节（0.1~1.0）。
- **字体大小调节**：Alt+滚轮随时调整题库/AI答案字体大小。
- **窗口快速隐藏/显示**：F3一键隐藏到屏幕边缘，再次按下恢复。
- **窗口自由拖动**：Ctrl+鼠标左键拖动窗口到任意位置。
- **ESC/快捷退出**：ESC或任意F6键可快速关闭程序（可自定义）。
- **自动点击答案/下一题**：使用`python opencv`实现自动点击。
- **API调用自动识别**：使用`百度 AipOcr`的API识别图片。

## 项目引用

- 基于[CX_EXAM_python](https://github.com/SJYssr/CX_EXAM_python)再开发
- 基于`AutoHotkey`实现`32/64`位系统自动打字
- 利用[DeAntiCapture](https://www.52pojie.cn/thread-2002346-1-1.html)反截图

## 其他实用功能
- **多线程处理**：AI问答、输入等操作均采用多线程，保证界面流畅不卡顿。
- **详细注释与易用配置**：所有代码文件均有详细头部说明和函数注释；`config.yaml`仅存放 Deepseek 配置，简单明了，便于二次开发。

---

## 代码结构与模块说明

本项目已重构为模块化结构，主入口为`./run/main.py`，各功能分为独立模块，便于维护和扩展。

---
### 启动程序
1. **运行程序**：在命令行中运行`python run/main.py`。
2. **主界面功能**：
   - 题库搜索：输入关键词，回车跳转下一个结果。
   - 设置/AI：顶部右侧“设置”按钮与“AI”按钮（已对调位置）。
   - 快捷输入：在输入框中输入内容，点击"输入"按钮自动输入。

### 常用快捷键与操作
- **F3**：窗口隐藏/恢复
- **Ctrl+鼠标左键**：拖动窗口
- **右键**：切换透明度
- **Ctrl+滚轮**：调整透明度
- **Alt+滚轮**：调整字体大小
- **回车**：题库搜索下一个
- **F2**：自动搜题
- **F6**：一键关闭
- **F5**：手动搜题
- **F7**：启动反反截图
---

## 运行

> 注意：本项目由`python 3.7.9-32位`运行。

1. 在[deepseek api](https://platform.deepseek.com/api_keys)申请deepseek密钥，复制api key
2. 在[百度 AipOcr](https://console.bce.baidu.com/ai-engine/ocr/app/list)创建应用，创建完应用，点击查看应用详情，复制app_id, api_key, secret_key
3. 运行`git clone https://github.com/maoyou11/Learning-SearchTopic-App.git`
4. 填入`./conf/config.yaml`
5. 运行`pip install -r requirements.txt`
6. 运行`./run/mian.py`

## 免责声明

> **本代码仅用于学习讨论，禁止用于盈利或违法用途。**

- 遵循 [GPL-3.0 License](https://github.com/SJYssr/CX_EXAM_python/blob/main/LICENSE) 协议：
  - 允许开源/免费使用、引用、修改、衍生
  - 禁止闭源商业发布、销售及盈利
  - 基于本代码的程序**必须**同样遵守GPL-3.0协议
- 他人或组织使用本代码进行的任何违法行为与本人无关

---