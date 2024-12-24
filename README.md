# TS to MP4 Converter

一个简单的 TS 视频转换为 MP4 格式的工具。

## 功能特点

- 简单的图形界面
- 支持多语言（中文/英文）
- 使用 ffmpeg 进行快速转换
- 保存上次使用的输出路径
- 进度显示

## 使用前提

1. 安装 Python 3.x
2. 安装 ffmpeg 并添加到系统环境变量
3. 安装依赖包：
```pip install -r requirements.txt```

## 使用方法

1. 运行程序
2. 设置保存路径
3. 选择要转换的 TS 文件
4. 等待转换完成

## 构建可执行文件

```bash
pyinstaller --clean --onefile --noconsole --add-data "C:\ffmpeg\bin\*.*;ffmpeg\bin" app.py
```

## 联系方式

如有问题请联系：lanlic@hotmail.com

## 许可证

MIT License
