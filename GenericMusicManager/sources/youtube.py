import yt_dlp

from GenericMusicManager.gmm import Music

__url_regex__ = "youtube.com"
__youtube_dlp_options = {
    "quiet":    True,
    "no_warnings": True,
    "simulate": True,
    "format": "bestaudio/best",
}

def src_youtube(url: str) -> Music:
    with yt_dlp.YoutubeDL(__youtube_dlp_options) as yt:
        extracted_info = yt.extract_info(url, download=False)
    
    track_name = extracted_info["title"]
    track_artist = extracted_info["artist"]
    track_album = extracted_info["album"]
    track_duration = extracted_info["duration"]
    url = url
    download_url = extracted_info["url"]
    
    return Music(track_name, track_artist, track_album, track_duration, url, download_url, extracted_info)
