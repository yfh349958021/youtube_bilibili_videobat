# YouTube → Bilibili 自动搬运脚本

自动监控YouTube频道的视频并上传到B站。

## 功能特性

- 🎬 **自动监控**: 定时检查YouTube频道新视频
- 🔍 **关键词过滤**: 只处理包含指定关键词的视频
- 📥 **自动下载**: 支持最高4K60fps视频下载
- 📤 **自动上传**: 自动上传到B站
- 🗑️ **自动清理**: 上传完成后自动删除本地文件
- 🔄 **定时运行**: 可配置检查间隔（默认20分钟）

## 项目状态

⚠️ **注意**: 由于YouTube反爬虫限制，视频下载功能需要进一步优化。

当前可用功能：
- ✅ YouTube频道监控
- ✅ B站登录和上传
- ❌ YouTube视频下载（被反爬虫阻止）

## 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/youtube-to-bilibili.git
cd youtube-to-bilibili

# 安装依赖
pip install -r requirements.txt

# 安装Playwright浏览器
playwright install chromium

# 配置
cp config.py.example config.py
# 编辑config.py
```

## 配置

### 1. B站登录
```bash
# 首次运行需要登录B站
python bilibili_uploader.py
# 会打开浏览器，扫码登录
```

### 2. 修改配置
编辑 `config.py`:
- `YOUTUBE_CHANNEL`: 要监控的YouTube频道
- `KEYWORDS`: 视频关键词列表
- `CHECK_INTERVAL`: 检查间隔（秒）

## 运行

```bash
# 直接运行
python main.py

# 或使用systemd服务
sudo cp youtube2bilibili.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start youtube2bilibili
```

## 已知问题

### YouTube下载限制
YouTube会检测自动化访问，导致下载失败。解决方案：
1. 使用已登录的YouTube cookies
2. 使用第三方下载API
3. 手动下载后自动上传

详见项目文档。

## 技术栈

- Python 3.10+
- Playwright - 浏览器自动化
- yt-dlp - 视频下载
- xvfb - 虚拟显示

## License

MIT
