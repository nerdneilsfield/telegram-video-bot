import logging
import re

import coloredlogs
from utils import get_redicrect_url, pure_bilibili_url

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
coloredlogs.install(logger=logger)


class RegexFilter():
    @staticmethod
    def is_bilibili_url(url: str) -> bool:
        bilibili_url_regex = re.compile(r"https?://(?:www\.)?bilibili\.com/video/\w+")
        bilibili_short_url_regex = re.compile(r"https?://b23\.tv/([a-zA-Z0-9]+)")

        if len(bilibili_url_regex.findall(url)) > 0:
            return True
        elif len(bilibili_short_url_regex.findall(url)) > 0:
            return True
        else:
            return False        
        
    @staticmethod
    def transform_bilibili_url(url: str) -> str:
        logger.info(f"transform_bilibili_url: {url}")
        bilibili_url_regex = re.compile(r"https?://(?:www\.)?bilibili\.com/video/[^\W]+")
        bilibili_short_url_regex = re.compile(r"https?://b23\.tv")
        bilibili_short_url_extract_regex = re.compile(r"https?://b23\.tv/([a-zA-Z0-9]+)")

        # an example url is "【宽体普京但是每次转弯身体就变宽-哔哩哔哩】 https://b23.tv/dR8jSYL"
        if len(bilibili_url_regex.findall(url)) > 0:
            bilibili_real_url = bilibili_url_regex.findall(url)[0]
            logger.info(f"bilibili_real_url: {bilibili_real_url}")
            bilibili_pure_url = pure_bilibili_url(bilibili_real_url)
            return bilibili_pure_url
            
        elif len(bilibili_short_url_regex.findall(url)) > 0:
            redict_ids = re.findall(bilibili_short_url_extract_regex, url)
            if len(redict_ids) == 1:
                redict_id = redict_ids[0]
                bilibili_short_url =  f"https://b23.tv/{redict_id}"
                logger.info(f"bilibili short url: {bilibili_short_url}")
                bilibili_real_url = get_redicrect_url(bilibili_short_url)
                logger.info(f"bilibili_real_url: {bilibili_real_url}")
                bilibili_pure_url = pure_bilibili_url(bilibili_real_url)
                return url.replace(bilibili_short_url, bilibili_pure_url)
            else:
                return "不是正常的 b23.tv 链接"
            
            

    @staticmethod
    def is_youtube_url(url: str) -> bool:
        youtube_url_regex = re.compile(r"https?://(?:www\.)?youtube")
        if youtube_url_regex.match(url):
            return True
        else:
            return False