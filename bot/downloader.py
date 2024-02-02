import os

import yt_dlp

from config import download_dir

def download_yt_video(url: str) -> str:
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)
    download_file_name = ""
    
    def hook(d):
        nonlocal download_file_name
        download_file_name = d.get("info_dict").get("_filename")
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': f'{download_dir}/%(title)s.%(ext)s',
        'progress_hooks': [hook],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return download_file_name

def download_yt_audio(url: str) -> str:
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)
    download_file_name = ""
    
    def hook(d):
        nonlocal download_file_name
        download_file_name = d.get("info_dict").get("_filename")
    
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio',
        'outtmpl': f'{download_dir}/%(title)s.%(ext)s',
        'progress_hooks': [hook],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return download_file_name