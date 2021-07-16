import requests as rq
import bs4 as bs4
import re
import time
import youtube_dl

def download_data_youtubedl(query, qtd_videos):

	with youtube_dl.YoutubeDL({"ignoreerrors": True}) as ydl:
	
		try:
			r = ydl.extract_info("ytsearchdate{}:{}".format(qtd_videos,query), download = False)
			for entry in r['entries']:
				if entry is not None:
					entry['_query'] = query
			return r['entries']
		
		except:
			pass
