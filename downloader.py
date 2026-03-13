import logging
import subprocess
import os
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_video(video_info):
    """下载YouTube视频"""
    video_id = video_info['id']
    title = video_info['title']
    url = video_info['url']
    
    # 清理文件名
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
    output_path = os.path.join(config.DOWNLOAD_DIR, f"{safe_title}.mp4")
    
    if os.path.exists(output_path):
        logger.info(f"视频已存在: {safe_title}")
        return output_path
    
    logger.info(f"开始下载: {title}")
    
    # yt-dlp命令
    cmd = [
        'yt-dlp',
        '-f', f'bestvideo[height<={config.MAX_RESOLUTION[:-1]}][fps<={config.MAX_FPS}]+bestaudio/best',
        '--merge-output-format', 'mp4',
        '-o', output_path,
        url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)  # 30分钟超时
        
        if result.returncode == 0:
            logger.info(f"✅ 下载完成: {output_path}")
            return output_path
        else:
            logger.error(f"❌ 下载失败: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        logger.error("❌ 下载超时")
        return None
    except Exception as e:
        logger.error(f"❌ 下载出错: {e}")
        return None

if __name__ == "__main__":
    # 测试
    test_video = {
        'id': 'test123',
        'title': 'Test Video',
        'url': 'https://www.youtube.com/watch?v=test123'
    }
    result = download_video(test_video)
    print(f"下载结果: {result}")
