import GenericMusicManager
import requests
import tldextract

from GenericMusicManager.gmm import Music, HandlersProtocol

def gen_class(url: str) -> Music:
    parsed_url = requests.get(url).url
    parsed_domain = tldextract.extract(parsed_url).domain
    for domain, handler in GenericMusicManager.mapped_url_sources.items():
        if domain != parsed_domain:
            continue

        handler_class: HandlersProtocol = handler(url)
        return handler_class.gen_music_class()
    else:
        raise NotImplementedError

some = gen_class("https://music.youtube.com/watch?v=4VwtfInG-LU&feature=shared")

# print(some.to_json())
