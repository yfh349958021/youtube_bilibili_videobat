import logging
from playwright.sync_api import sync_playwright
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_video_list():
    """获取YouTube频道的视频列表"""
    videos = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            logger.info(f"访问频道: {config.YOUTUBE_CHANNEL}")
            page.goto(config.YOUTUBE_CHANNEL, wait_until='networkidle', timeout=60000)
            page.wait_for_selector('ytd-rich-item-renderer', timeout=30000)
            
            # 获取视频元素
            video_elements = page.query_selector_all('ytd-rich-item-renderer')
            logger.info(f"找到 {len(video_elements)} 个视频")
            
            for elem in video_elements[:20]:
                try:
                    title_elem = elem.query_selector('#video-title')
                    if not title_elem:
                        continue
                    
                    title = title_elem.inner_text()
                    href = title_elem.get_attribute('href')
                    
                    if not href or not title:
                        continue
                    
                    video_id = None
                    if href:
                        if '/watch?v=' in href:
                            video_id = href.split('/watch?v=')[-1].split('&')[0]
                        elif '/shorts/' in href:
                            video_id = href.split('/shorts/')[-1].split('?')[0]
                    
                    if not video_id:
                        import hashlib
                        video_id = hashlib.md5(title.encode()).hexdigest()[:11]
                    
                    # 检查关键词
                    title_lower = title.lower()
                    if any(kw in title_lower for kw in config.KEYWORDS):
                        videos.append({
                            'id': video_id,
                            'title': title,
                            'url': f"https://www.youtube.com/watch?v={video_id}"
                        })
                        logger.info(f"✅ 匹配: {title}")
                    
                except Exception as e:
                    logger.debug(f"解析视频元素失败: {e}")
                    continue
                    
        finally:
            browser.close()
    
    return videos

if __name__ == "__main__":
    videos = get_video_list()
    print(f"\n找到 {len(videos)} 个匹配的视频:")
    for v in videos:
        print(f"  - {v['title']}")
