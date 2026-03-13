import logging
import time
import os
from playwright.sync_api import sync_playwright
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BilibiliUploader:
    def __init__(self):
        self.profile = config.BILIBILI_PROFILE
        
    def upload_video(self, video_path, title, description=""):
        """上传视频到B站"""
        if not os.path.exists(video_path):
            logger.error(f"视频文件不存在: {video_path}")
            return False
        
        logger.info(f"开始上传: {title}")
        
        with sync_playwright() as p:
            # 使用已登录的profile
            context = p.chromium.launch_persistent_context(
                self.profile,
                executable_path="/usr/bin/google-chrome",
                headless=False,
                viewport={'width': 1920, 'height': 1080},
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            
            try:
                page = context.pages[0] if context.pages else context.new_page()
                
                # 进入创作中心
                logger.info("进入创作中心...")
                page.goto("https://member.bilibili.com/platform/upload/video/frame", 
                         wait_until='networkidle', timeout=60000)
                time.sleep(5)
                
                # 检查是否登录
                if "登录" in page.title() or page.query_selector('.login-btn'):
                    logger.error("❌ 未登录或登录已失效")
                    context.close()
                    return False
                
                # 点击上传按钮
                logger.info("点击上传按钮...")
                upload_btn = page.query_selector('.upload-btn, .btn-upload')
                if upload_btn:
                    upload_btn.click()
                    time.sleep(3)
                
                # 上传文件
                logger.info(f"上传文件: {video_path}")
                file_input = page.query_selector('input[type="file"]')
                if file_input:
                    file_input.set_input_files(video_path)
                    logger.info("文件选择完成，等待上传...")
                    time.sleep(10)
                else:
                    logger.error("❌ 未找到文件上传输入框")
                    context.close()
                    return False
                
                # 填写标题
                logger.info("填写视频信息...")
                title_input = page.query_selector('input[placeholder*="标题"], input[name="title"]')
                if title_input:
                    title_input.fill(title[:80])  # B站标题限制80字
                
                # 填写简介
                if description:
                    desc_input = page.query_selector('textarea[placeholder*="简介"], textarea[name="desc"]')
                    if desc_input:
                        desc_input.fill(description[:2000])  # B站简介限制2000字
                
                # 等待上传完成
                logger.info("等待视频上传和转码...")
                time.sleep(30)
                
                # 检查上传状态
                # 这里需要根据实际页面结构调整
                
                logger.info("✅ 上传流程完成")
                context.close()
                return True
                
            except Exception as e:
                logger.error(f"❌ 上传失败: {e}")
                context.close()
                return False

if __name__ == "__main__":
    uploader = BilibiliUploader()
    # 测试
    print("B站上传器已就绪")
