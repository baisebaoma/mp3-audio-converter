import os
import subprocess
import json
import time
import sys

def get_file_size_kb(file_path):
    """获取文件大小，单位KB"""
    return os.path.getsize(file_path) / 1024

def get_media_info(file_path):
    """使用FFmpeg获取媒体文件信息"""
    try:
        # 处理可能的中文路径问题
        cmd = ["ffprobe", "-v", "quiet", "-print_format", "json",
               "-show_format", "-show_streams", file_path]
        
        # 使用subprocess.DEVNULL避免编码问题
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, 
                               stderr=subprocess.DEVNULL, encoding='utf-8')
        
        if result.stdout:
            return json.loads(result.stdout)
        return None
    except subprocess.CalledProcessError:
        print("获取媒体信息失败")
        return None
    except json.JSONDecodeError:
        print("解析媒体信息失败")
        return None
    except Exception as e:
        print(f"获取媒体信息时发生错误: {e}")
        return None

def convert_to_mp3(input_path, output_path, target_size_kb=100):
    """将音频文件转换为不超过指定大小的MP3"""
    try:
        # 获取源文件信息 - 如果失败继续执行
        try:
            media_info = get_media_info(input_path)
        except:
            media_info = None
            print("获取媒体信息失败，将继续进行转换")
        
        # 第一次尝试：中等质量转换
        print("尝试初始转换...")
        subprocess.run([
            "ffmpeg", "-y", "-i", input_path,
            "-acodec", "libmp3lame", "-q:a", "4", output_path
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 检查文件大小
        current_size = get_file_size_kb(output_path)
        print(f"初始转换大小: {current_size:.2f}KB")
        
        # 如果文件已经小于目标大小，直接返回成功
        if current_size <= target_size_kb:
            print(f"初始转换即达标！文件大小: {current_size:.2f}KB")
            return True
        
        # 如果文件超过目标大小，进行迭代压缩
        attempt = 1
        quality = 4  # 初始质量 (VBR模式, 0-9, 0最好，9最差)
        
        while current_size > target_size_kb and attempt < 10:
            print(f"尝试 #{attempt+1}: 当前大小 {current_size:.2f}KB > 目标 {target_size_kb}KB")
            
            # 根据大小比例调整质量
            if current_size > target_size_kb * 2:
                quality = min(9, quality + 2)
            else:
                quality = min(9, quality + 1)
                
            # 如果质量已经很低但文件仍然很大，可能需要缩短时长
            duration_option = []
            if quality >= 7 and current_size > target_size_kb * 1.5:
                # 估算所需的持续时间比例
                target_duration_ratio = target_size_kb / current_size * 0.9
                if media_info and "format" in media_info and "duration" in media_info["format"]:
                    try:
                        orig_duration = float(media_info["format"]["duration"])
                        new_duration = orig_duration * target_duration_ratio
                        duration_option = ["-t", str(new_duration)]
                        print(f"需要缩短音频时长至原始时长的 {target_duration_ratio:.2%}")
                    except:
                        print("解析持续时间失败，不进行时长调整")
            
            # 重新转换
            subprocess.run([
                "ffmpeg", "-y", "-i", input_path
            ] + duration_option + [
                "-acodec", "libmp3lame", "-q:a", str(quality), output_path
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            current_size = get_file_size_kb(output_path)
            print(f"调整后大小: {current_size:.2f}KB (质量等级: {quality})")
            attempt += 1
        
        if current_size <= target_size_kb:
            print(f"成功转换！文件大小: {current_size:.2f}KB，使用的质量等级: {quality} (值越大质量越低)")
            return True
        else:
            # 最后尝试：固定低比特率
            print("尝试最终低比特率转换...")
            final_bitrate = max(8, int(target_size_kb * 8 / 1.5))  # 预留更多空间
            subprocess.run([
                "ffmpeg", "-y", "-i", input_path,
                "-acodec", "libmp3lame", "-b:a", f"{final_bitrate}k", 
                "-ac", "1", output_path  # 转为单声道
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            current_size = get_file_size_kb(output_path)
            print(f"最终转换大小: {current_size:.2f}KB (比特率: {final_bitrate}kbps, 单声道)")
            
            if current_size <= target_size_kb:
                print(f"最终转换成功！文件大小: {current_size:.2f}KB")
                return True
            else:
                print(f"警告：无法将文件压缩到{target_size_kb}KB以下。当前大小: {current_size:.2f}KB")
                return False
            
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg转换过程中出错: {str(e)}")
        return False
    except Exception as e:
        print(f"发生未预期的错误: {str(e)}")
        return False

def check_ffmpeg():
    """检查FFmpeg是否已安装"""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False
    except Exception:
        # 其他错误也可能意味着ffmpeg有问题
        return False

def main():
    print("=== 音频转MP3转换器 (输出文件不大于100KB) ===")
    
    if not check_ffmpeg():
        print("错误: 未检测到FFmpeg!")
        print("请安装FFmpeg: https://ffmpeg.org/download.html")
        print("确保ffmpeg命令可以在命令行中运行")
        return
    
    while True:
        print("\n" + "="*50)
        # 1. 询问文件路径
        input_path = input("请输入音频文件路径（或输入'q'退出）: ").strip()
        if input_path.lower() == 'q':
            break
        
        # 去除引号（用户可能从文件管理器复制带引号的路径）
        if (input_path.startswith('"') and input_path.endswith('"')) or \
           (input_path.startswith("'") and input_path.endswith("'")):
            input_path = input_path[1:-1]
        
        if not os.path.exists(input_path):
            print(f"错误: 文件 '{input_path}' 不存在!")
            continue
        
        # 2. 询问输出文件名
        output_filename = input("请输入输出MP3文件名 (不含路径和扩展名): ").strip()
        if not output_filename:
            output_filename = os.path.splitext(os.path.basename(input_path))[0] + "_compressed"
        
        # 确保文件名以.mp3结尾
        if not output_filename.lower().endswith('.mp3'):
            output_filename += '.mp3'
        
        # 获取输入文件的目录
        output_dir = os.path.dirname(input_path)
        if not output_dir:  # 如果是当前目录
            output_dir = os.getcwd()
        
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"正在处理: {input_path}")
        print(f"输出文件: {output_path}")
        
        # 3. 处理音频文件
        # 4. 输出到相同目录
        try:
            success = convert_to_mp3(input_path, output_path)
            
            if success:
                print(f"文件已保存到: {output_path}")
            else:
                print("转换未完全成功，但可能已生成文件。请检查输出文件质量。")
        except Exception as e:
            print(f"处理过程中发生错误: {str(e)}")
            print("请检查输入文件是否是有效的音频文件。")

if __name__ == "__main__":
    main()