#!/usr/bin/env python3
import logging
import json
import os
import time
import youtube_monitor
import downloader
import bilibili_uploader
import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/root/youtube_to_bilibili/main.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_processed():
    """加载已处理的视频列表"""
    if os.path.exists(config.PROCESSED_FILE):
        with open(config.PROCESSED_FILE, 'r') as f:
            return json.load(f)
    return []

def save_processed(processed):
    """保存已处理的视频列表"""
    with open(config.PROCESSED_FILE, 'w') as f:
        json.dump(processed, f, indent=2)

def main():
    logger.info("="*50)
    logger.info("YouTube → Bilibili 自动上传服务启动")
    logger.info("="*50)
    
    uploader = bilibili_uploader.BilibiliUploader()
    
    while True:
        try:
            logger.info("\n🔍 检查新视频...")
            
            # 获取视频列表
            videos = youtube_monitor.get_video_list()
            logger.info(f"找到 {len(videos)} 个匹配的视频")
            
            # 加载已处理列表
            processed = load_processed()
            
            # 处理新视频
            for video in videos:
                if video['id'] in processed:
                    logger.info(f"跳过已处理: {video['title']}")
                    continue
                
                logger.info(f"\n处理视频: {video['title']}")
                
                # 下载视频
                video_path = downloader.download_video(video)
                if not video_path:
                    logger.error("下载失败，跳过")
                    continue
                
                # 上传到B站
                success = uploader.upload_video(
                    video_path,
                    video['title'],
                    f"来源: {video['url']}"
                )
                
                if success:
                    # 记录已处理
                    processed.append(video['id'])
                    save_processed(processed)
                    
                    # 删除本地文件
                    if os.path.exists(video_path):
                        os.remove(video_path)
                        logger.info(f"🗑️ 已删除本地文件: {video_path}")
                    
                    logger.info(f"✅ 视频处理完成: {video['title']}")
                else:
                    logger.error(f"❌ 上传失败: {video['title']}")
            
            logger.info(f"\n😴 等待 {config.CHECK_INTERVAL} 秒...")
            time.sleep(config.CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            logger.info("\n收到停止信号，退出...")
            break
        except Exception as e:
            logger.error(f"❌ 运行出错: {e}", exc_info=True)
            logger.info("等待60秒后重试...")
            time.sleep(60)

if __name__ == "__main__":
    main()
