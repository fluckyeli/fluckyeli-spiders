"""
下载工具模块 - download_utils.py
提供稳健的文件下载功能，支持断点续传、重试机制和进度显示
"""

import os
import sys
import time
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Callable
from tqdm import tqdm
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib3.exceptions import IncompleteRead, ProtocolError

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DownloadError(Exception):
    """自定义下载异常"""
    pass


class DownloadConfig:
    """下载配置类"""

    def __init__(
            self,
            max_retries: int = 5,
            timeout: int = 30,
            chunk_size: int = 1024 * 1024,  # 1MB
            user_agent: str = None,
            headers: Dict[str, str] = None,
            enable_progress_bar: bool = True,
            verify_ssl: bool = True,
            proxy: Dict[str, str] = None
    ):
        self.max_retries = max_retries
        self.timeout = timeout
        self.chunk_size = chunk_size
        self.user_agent = user_agent or (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
        self.headers = headers or {}
        if 'User-Agent' not in self.headers:
            self.headers['User-Agent'] = self.user_agent
        self.enable_progress_bar = enable_progress_bar
        self.verify_ssl = verify_ssl
        self.proxy = proxy

        # 添加默认请求头
        self.headers.update({
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
        })


class Downloader:
    """下载器主类"""

    def __init__(self, config: DownloadConfig = None):
        self.config = config or DownloadConfig()
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """创建带重试机制的会话"""
        session = requests.Session()

        # 配置重试策略
        retry_strategy = Retry(
            total=self.config.max_retries,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "HEAD"],
            raise_on_status=False
        )

        # 创建适配器
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=10
        )

        # 挂载适配器
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # 设置默认请求头
        session.headers.update(self.config.headers)

        return session

    def _get_file_size(self, url: str) -> Optional[int]:
        """获取文件大小"""
        try:
            response = self.session.head(
                url,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl,
                proxies=self.config.proxy
            )
            response.raise_for_status()

            # 尝试从不同头部获取文件大小
            size = None
            if 'Content-Length' in response.headers:
                size = int(response.headers['Content-Length'])
            elif 'content-length' in response.headers:
                size = int(response.headers['content-length'])

            return size
        except Exception as e:
            logger.warning(f"无法获取文件大小: {e}")
            return None

    def _download_chunk(
            self,
            url: str,
            file_path: Path,
            start_byte: int = 0,
            progress_callback: Callable = None
    ) -> bool:
        """下载文件块（支持断点续传）"""
        headers = {}
        if start_byte > 0:
            headers['Range'] = f'bytes={start_byte}-'
            logger.info(f"断点续传: 从字节 {start_byte} 开始")

        try:
            response = self.session.get(
                url,
                headers=headers,
                stream=True,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl,
                proxies=self.config.proxy
            )
            response.raise_for_status()

            # 检查响应状态
            if start_byte > 0 and response.status_code != 206:
                logger.warning("服务器不支持断点续传，将重新下载")
                return False

            # 获取文件总大小
            total_size = None
            if 'Content-Range' in response.headers:
                # 从 Content-Range 获取总大小
                content_range = response.headers['Content-Range']
                if '/' in content_range:
                    total_size = int(content_range.split('/')[-1])
            elif 'Content-Length' in response.headers:
                total_size = start_byte + int(response.headers['Content-Length'])

            # 打开文件（追加模式）
            mode = 'ab' if start_byte > 0 else 'wb'
            with open(file_path, mode) as f:
                if self.config.enable_progress_bar and total_size:
                    # 使用 tqdm 显示进度
                    with tqdm(
                            total=total_size,
                            initial=start_byte,
                            unit='B',
                            unit_scale=True,
                            unit_divisor=1024,
                            desc=file_path.name,
                            ascii=True
                    ) as pbar:
                        for chunk in response.iter_content(chunk_size=self.config.chunk_size):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))
                                if progress_callback:
                                    progress_callback(pbar.n, total_size)
                else:
                    # 不使用进度条
                    downloaded = start_byte
                    for chunk in response.iter_content(chunk_size=self.config.chunk_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if progress_callback:
                                progress_callback(downloaded, total_size)

            return True

        except (requests.exceptions.RequestException, IncompleteRead, ProtocolError) as e:
            logger.error(f"下载过程中出现错误: {e}")
            raise DownloadError(f"下载失败: {e}")

    def download(
            self,
            url: str,
            file_path: str,
            overwrite: bool = False,
            progress_callback: Callable = None
    ) -> bool:
        """
        下载文件

        Args:
            url: 下载URL
            file_path: 保存路径
            overwrite: 是否覆盖已存在文件
            progress_callback: 进度回调函数

        Returns:
            bool: 是否下载成功
        """
        file_path = Path(file_path)

        # 创建目录
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # 检查文件是否存在
        start_byte = 0
        if file_path.exists():
            if overwrite:
                logger.info(f"覆盖已存在文件: {file_path}")
                file_path.unlink()
            else:
                file_size = file_path.stat().st_size
                remote_size = self._get_file_size(url)

                if remote_size and file_size == remote_size:
                    logger.info(f"文件已存在且完整: {file_path}")
                    return True
                elif file_size > 0:
                    logger.info(f"检测到不完整文件，尝试断点续传: {file_path}")
                    start_byte = file_size

        # 尝试下载
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                logger.info(f"开始下载: {url}")
                logger.info(f"保存到: {file_path}")

                success = self._download_chunk(
                    url, file_path, start_byte, progress_callback
                )

                if success:
                    # 验证文件大小
                    final_size = file_path.stat().st_size
                    expected_size = self._get_file_size(url)

                    if expected_size and final_size != expected_size:
                        logger.warning(f"文件大小不匹配: 期望 {expected_size}, 实际 {final_size}")

                        if attempt < max_attempts - 1:
                            logger.info("重新下载...")
                            file_path.unlink()
                            start_byte = 0
                            continue
                        else:
                            raise DownloadError(f"文件大小不匹配: {final_size} != {expected_size}")

                    logger.info(f"下载完成: {file_path} ({final_size} 字节)")
                    return True

            except DownloadError as e:
                logger.error(f"下载失败 (尝试 {attempt + 1}/{max_attempts}): {e}")

                if attempt < max_attempts - 1:
                    wait_time = 2 ** attempt  # 指数退避
                    logger.info(f"等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    logger.error("已达到最大重试次数，下载失败")
                    return False

        return False

    def download_multiple(
            self,
            url_file_pairs: list,
            max_workers: int = 3,
            progress_callback: Callable = None
    ) -> Dict[str, bool]:
        """
        批量下载多个文件

        Args:
            url_file_pairs: [(url1, path1), (url2, path2), ...]
            max_workers: 最大并发数
            progress_callback: 进度回调函数

        Returns:
            Dict[str, bool]: 下载结果字典 {url: success}
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed

        results = {}

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交下载任务
            future_to_url = {
                executor.submit(self.download, url, file_path, False, progress_callback): url
                for url, file_path in url_file_pairs
            }

            # 处理完成的任务
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    success = future.result(timeout=self.config.timeout * 2)
                    results[url] = success
                    logger.info(f"任务完成: {url} - {'成功' if success else '失败'}")
                except Exception as e:
                    results[url] = False
                    logger.error(f"任务异常: {url} - {e}")

        return results

    def close(self):
        """关闭会话"""
        if self.session:
            self.session.close()


def simple_download(
        url: str,
        file_path: str,
        max_retries: int = 5,
        timeout: int = 30,
        show_progress: bool = True
) -> bool:
    """
    简单下载函数（快速使用）

    Args:
        url: 下载URL
        file_path: 保存路径
        max_retries: 最大重试次数
        timeout: 超时时间
        show_progress: 是否显示进度条

    Returns:
        bool: 是否下载成功
    """
    config = DownloadConfig(
        max_retries=max_retries,
        timeout=timeout,
        enable_progress_bar=show_progress
    )

    downloader = Downloader(config)

    try:
        return downloader.download(url, file_path)
    finally:
        downloader.close()


def download_with_callback(
        url: str,
        file_path: str,
        callback: Callable[[int, int], None]
) -> bool:
    """
    带回调函数的下载

    Args:
        url: 下载URL
        file_path: 保存路径
        callback: 回调函数，接收(已下载字节, 总字节数)

    Returns:
        bool: 是否下载成功
    """

    def progress_callback(downloaded, total):
        callback(downloaded, total)

    return simple_download(
        url, file_path, show_progress=False
    )


def example_usage():
    """使用示例"""

    # 示例1: 简单下载
    print("示例1: 简单下载")
    success = simple_download(
        "http://example.com/video.mp4",
        "downloads/video.mp4",
        show_progress=True
    )
    print(f"下载结果: {'成功' if success else '失败'}")

    # 示例2: 使用完整配置
    print("\n示例2: 使用完整配置")
    config = DownloadConfig(
        max_retries=5,
        timeout=60,
        chunk_size=512 * 1024,  # 512KB
        headers={
            'Referer': 'http://example.com/',
            'Accept': 'video/mp4,*/*'
        }
    )

    downloader = Downloader(config)
    try:
        success = downloader.download(
            "http://example.com/video.mp4",
            "downloads/video2.mp4"
        )
        print(f"下载结果: {'成功' if success else '失败'}")
    finally:
        downloader.close()

    # 示例3: 批量下载
    print("\n示例3: 批量下载")
    downloads = [
        ("http://example.com/file1.mp4", "downloads/file1.mp4"),
        ("http://example.com/file2.mp4", "downloads/file2.mp4"),
    ]

    downloader = Downloader()
    try:
        results = downloader.download_multiple(downloads, max_workers=2)
        for url, success in results.items():
            print(f"{url}: {'成功' if success else '失败'}")
    finally:
        downloader.close()

    # 示例4: 带进度回调
    print("\n示例4: 带进度回调")

    def on_progress(downloaded, total):
        if total:
            percent = (downloaded / total) * 100
            print(f"\r进度: {percent:.1f}% ({downloaded}/{total})", end='')
        else:
            print(f"\r已下载: {downloaded} 字节", end='')

    success = download_with_callback(
        "http://example.com/video.mp4",
        "downloads/video3.mp4",
        on_progress
    )
    print(f"\n下载结果: {'成功' if success else '失败'}")


if __name__ == "__main__":
    example_usage()