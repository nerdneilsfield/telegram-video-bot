import re


class RegexFilter():
    @staticmethod
    def is_bilibili_url(url: str) -> bool:
        bilibili_url_regex = re.compile(r"https?://(?:www\.)?bilibili\.com")
        bilibili_short_url_regex = re.compile(r"https?://(?:www\.b23\.tv)?")

        if bilibili_url_regex.match(url):
            return True
        elif bilibili_short_url_regex.match(url):
            return True
        else:
            return False        

    @staticmethod
    def is_youtube_url(url: str) -> bool:
        youtube_url_regex = re.compile(r"https?://(?:www\.)?youtube")
        if youtube_url_regex.match(url):
            return True
        else:
            return False