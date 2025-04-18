# mp3-audio-converter

## 轻量级批量音频转换工具

[English](#lightweight-batch-audio-conversion-tool)

最近在重操旧业写 [新月杀（FreeKill）](https://github.com/Qsgs-Fans/FreeKill/) 武将时遇到了下列需求：首先需要找到那个武将的音频素材，然后需要将收集来的各种格式的素材都转化成 mp3 格式，而且还要控制音频文件大小，最后还要修改其文件名（如 `jy_jianwu1.mp3`）。之前都是使用高级音频工具一个一个手工改的，有些过于麻烦了，于是写了这么一个小工具来帮助我快速做这些事情。希望对你也有帮助。

### ✨ 特点

- 将任意音频格式转换为不超过100KB的MP3文件
- 支持多种音频格式（任何FFmpeg可以处理的格式）
- 智能压缩策略：
  - 逐步降低质量直到达到目标大小
  - 必要时调整音频时长
  - 在极端情况下使用单声道
- 用户友好的命令行界面，提供交互式提示
- 在源文件相同目录下处理文件
- Python 3.13 版本中移除了 `pyaudioop` 库。这个版本使用纯 `ffmpeg`，所以不用担心。

### 📋 要求

- Python 3.x
- FFmpeg（必须安装并在PATH中可用）

### 🚀 安装

1. 克隆此仓库：
   ```
   git clone https://github.com/YourUsername/mp3-audio-converter.git
   cd mp3-audio-converter
   ```

2. 确保FFmpeg已安装：
   - Windows：从[ffmpeg.org](https://ffmpeg.org/download.html)下载并添加到PATH
   - macOS：`brew install ffmpeg`
   - Linux：`sudo apt install ffmpeg`或适用于您的发行版的等效命令

3. 运行脚本：
   ```
   python converter.py
   ```

### 💻 使用方法

1. 运行脚本
2. 在提示时输入音频文件路径
3. 输入所需的输出文件名（不含路径和扩展名）
4. 脚本将处理文件并将压缩后的MP3保存到相同目录

示例：
```
=== 音频转MP3转换器 (输出文件不大于100KB) ===

==================================================
请输入音频文件路径（或输入'q'退出）: /path/to/your/audio.wav
请输入输出MP3文件名 (不含路径和扩展名): jy_jianwu1
正在处理: /path/to/your/audio.wav
输出文件: /path/to/your/jy_jianwu1.mp3
...
文件已保存到: /path/to/your/jy_jianwu1.mp3
```

### 🔍 工作原理

该脚本使用多阶段压缩策略：

1. 首先使用中等质量设置进行转换
2. 如果结果超过100KB，则逐步降低质量
3. 如果在质量降低后仍超过限制，可选择缩短音频时长
4. 作为最后的手段，使用固定的低比特率转换为单声道

### 📄 许可证

本项目采用MIT许可证 - 详情请参阅LICENSE文件。

### 🤝 贡献

欢迎贡献、问题和功能请求！请随时查看issues页面。

---

## Lightweight Batch Audio Conversion Tool

Recently, while working on character development for [FreeKill](https://github.com/Qsgs-Fans/FreeKill/), I encountered the following requirements: first, I needed to find audio materials for characters, then convert collected materials of various formats to MP3 format, control the audio file size, and finally modify their filenames (e.g., `jy_jianwu1.mp3`). Previously, I was using professional audio tools to modify these files one by one, which was quite cumbersome. So I created this small tool to help me quickly accomplish these tasks. Hope it helps you too.

### ✨ Features

- Convert any audio format to MP3 files under 100KB
- Support for multiple audio formats (anything that FFmpeg can handle)
- Intelligent compression strategy:
  - Progressively reduces quality until target size is achieved
  - Adjusts audio duration if necessary
  - Uses mono channel for extreme compression cases
- User-friendly command-line interface with interactive prompts
- Processes files in the same directory as the source
- Python 3.13 removed the `pyaudioop` library. This version uses pure `ffmpeg`, so no need to worry.

### 📋 Requirements

- Python 3.x
- FFmpeg (must be installed and available in your PATH)

### 🚀 Installation

1. Clone this repository:
   ```
   git clone https://github.com/YourUsername/mp3-audio-converter.git
   cd mp3-audio-converter
   ```

2. Make sure FFmpeg is installed:
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg` or equivalent for your distribution

3. Run the script:
   ```
   python converter.py
   ```

### 💻 Usage

1. Run the script
2. Enter the path to your audio file when prompted
3. Enter the desired output filename (without path and extension)
4. The script will process the file and save the compressed MP3 to the same directory

Example:
```
=== 音频转MP3转换器 (输出文件不大于100KB) ===

==================================================
请输入音频文件路径（或输入'q'退出）: /path/to/your/audio.wav
请输入输出MP3文件名 (不含路径和扩展名): jy_jianwu1
正在处理: /path/to/your/audio.wav
输出文件: /path/to/your/jy_jianwu1.mp3
...
文件已保存到: /path/to/your/jy_jianwu1.mp3
```

### 🔍 How It Works

The script uses a multi-stage compression strategy:

1. First conversion with medium quality settings
2. If the result exceeds 100KB, progressively lower the quality
3. If still over the limit after quality reduction, optionally shorten the audio duration
4. As a last resort, convert to mono with a fixed low bitrate

### 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

### 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
