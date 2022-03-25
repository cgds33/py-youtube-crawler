import requests
import json, time
import os
from pytube import YouTube
import rstr
import re
import urllib.request
from pyyoutube import Api
import sys
from config import API_KEY,SEARCH_MODE,SEARCH_WORD,MAX_PAGE,CHANNEL_MODE,CHANNEL_LIST,DOWNLOAD_THUMBNAILS,DOWNLOAD_VIDEOS,LOGGING,TARGET_WORD,VIDEO_DIR,LOG_DIR,THUMB_DIR


def create_folders():
	# create video folder
	if (not os.path.isdir(VIDEO_DIR)) and (DOWNLOAD_VIDEOS == True):
		os.makedirs(VIDEO_DIR)

	# create log folder
	if (not os.path.isdir(LOG_DIR)) and (LOGGING == True):
		os.makedirs(LOG_DIR)

	# create thumbnails folder
	if (not os.path.isdir(THUMB_DIR)) and (DOWNLOAD_THUMBNAILS == True):
		os.makedirs(THUMB_DIR)


def config_check():

	if API_KEY == "":
		print("ALERT: Fill in the API KEY section in the config file")
		sys.exit()

	if (SEARCH_MODE == False) and (CHANNEL_MODE == False):
		print("ALERT: Crawler is not active. Active to SEARCH_MODE or CHANNEL_MODE")
		sys.exit()

	if (CHANNEL_MODE == True) and (CHANNEL_LIST == []):
		print("ALERT: Fill CHANNEL_LIST with IDs in string format")
		sys.exit()


## All error logs
def error_logger(error_word):
	print(error_word)
	file = open(LOG_DIR + "Youtube_DF_Errors.log", 'a', encoding="utf-8")
	file.write(error_word +"\n")
	file.close


# All video logs
def logger(cdn_log_tags):
	file = open(LOG_DIR + "Youtube_DF_Samples.log", 'a', encoding="utf-8")
	file.write(str(cdn_log_tags)+"\n")
	file.close
	print("Log data was writed... \n")


# Video's thumbnail pic download
def thumbnail_downloader(v_thumbnails,v_file_name):

	opener = urllib.request.build_opener()
	opener.addheaders = [('user-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36')]
	urllib.request.install_opener(opener)

	thumbnails_name = THUMB_DIR + v_file_name + ".jpg"
	urllib.request.urlretrieve(v_thumbnails,thumbnails_name)


# video downloader
def downloader(v_url,file_name_origin):
	try:
		yt = YouTube(v_url)
		yt.streams.first().download(VIDEO_DIR, file_name_origin)
		print("Video was downloaded..")
		return True
	except:
		return False

# file check with video ID / for not again download same video
def file_check(v_id):
	if os.path.exists(LOG_DIR + "Youtube_DF_Samples.log"):
		file = open(LOG_DIR + "Youtube_DF_Samples.log", "r", encoding="utf-8")
		log_lines = file.read().split("'")
		file.close

		for i in log_lines:
			loged_id = re.findall(v_id,i)
			if loged_id:
				print("File check error... Video ID is = {}".format(v_id))
				return False
	return True

# keyword filter
def filter(v_title):
	if TARGET_WORD != []:
		for f in TARGET_WORD:
			filter = re.findall(str(f), v_title)
			if filter:
				return True
		print("There is not keyword in the title! Moving to next video..")
		return False
	else:
		return True


def starter_download_and_logger(cdn_log_tags,v_title,v_url,v_file_name,v_id,v_thumbnails):

	timeNow = time.time()
	filter_check = filter(v_title)
	if filter_check == True:
		last_check = file_check(v_id)
		if last_check == True:
			print("Video downloading...")
			download_check = downloader(v_url,v_file_name)
			if download_check == True:
				if LOGGING == True:
					logger(cdn_log_tags)
				if DOWNLOAD_THUMBNAILS == True:
					thumbnail_downloader(v_thumbnails,v_file_name)
			else:
				error_word = "Video downloader error!   Video URL: {}   Time:{}".format(v_url,timeNow)
				if LOGGING == True:
					error_logger(error_word)


def all_information(sw,i):
	# Unique file name generator
	v_file_name = str(rstr.digits(32))

	# first response type 
	if (sw == 0):
		v_id = (i['id'])
		v_id = (v_id['videoId'])
		_snippet = (i['snippet'])
		_thumnails = (_snippet['thumbnails'])

		try:
			t_high = (_thumnails['high'])
			v_thumbnail = (t_high['url'])
		except:
			try:
				t_medium = (_thumnails['medium'])
				v_thumbnail = (t_medium['url'])
			except:
				t_default = (_thumnails['default'])
				v_thumbnail = (t_default['url'])

	# second response type 
	if (sw == 1):
		_snippet = (i['snippet'])
		_contentDetails = (i['contentDetails'])
		_contentDetails = (_contentDetails['upload'])
		v_id = (_contentDetails['videoId'])

		_thumb_content = (_snippet['thumbnails'])
		try:
			t_max = (_thumb_content['maxres'])
			v_thumbnail = (t_max['url'])
		except:
			try:
				t_high = (_thumb_content['high'])
				v_thumbnail = (t_high['url'])
			except:
				t_default = (_thumb_content['default'])
				v_thumbnail = (t_default['default'])


	#### parse video informations ####
	v_ptime = (_snippet['publishedAt'])
	v_channel_id = (_snippet['channelId'])
	v_channel_name = (_snippet['channelTitle'])
	v_title = (_snippet['title'])
	v_url = "https://www.youtube.com/watch?v={}".format(v_id)


	#### get video info ######
	info_url = "https://www.googleapis.com/youtube/v3/videos?part=statistics&id={}&key={}".format(v_id,API_KEY)
	_v_info = requests.get(info_url)
	time.sleep(1)

	if LOGGING == True:
		try:
			_v_info = _v_info.json()
			v_info_json = json.dumps(_v_info, indent=4)
			v_info_json = json.loads(v_info_json)
			v_info_items = (v_info_json['items'])

			for inf in v_info_items:

				v_info_statistic = (inf['statistics'])

				try:
					v_view = (v_info_statistic['viewCount'])
				except:
					v_view = "No info"
				try:
					v_like = (v_info_statistic['likeCount'])
				except:
					v_like = "No info"
				try:
					v_dislike = (v_info_statistic['dislikeCount'])
				except:
					v_dislike = "No info"
				try:
					v_comment = (v_info_statistic['commentCount'])
				except:
					v_comment = "No info"

		except:
			print("\nAPI INFO ITEM ERROR: {}\n".format(info_url))
			sys.exit() ### Fatal error

		logged_time = time.time()
		cdn_log_tags = {
			'filename': v_file_name + ".mp4",
			'video-id': v_id,
			'v-url': v_url,
			'title': v_title,
			'views': v_view,
			'likes': v_like,
			'dislikes': v_dislike,
			'comment': v_comment,
			'channel-name': v_channel_name,
			'channel-id': v_channel_id,
			'published-time': v_ptime,
			'log-time': logged_time
			}

	print("\nVideo-url: {}\nTitle: {}".format(v_url,v_title))
	starter_download_and_logger(cdn_log_tags,v_title,v_url,v_file_name,v_id,v_thumbnail)
	time.sleep(1)


def search_with_channel_id(channel_id_list):

	api = Api(api_key=API_KEY)
	for cID in channel_id_list:
		channel_by_id = api.get_activities_by_channel(channel_id=cID,count=999,limit=999)
		calc = 0

		while True:
			try:
				c_video_info = channel_by_id.items[calc].to_json()
				try:
					c_video_info = str(c_video_info).replace('null','" "')
					c_video_info: dict = eval(c_video_info)
					c_video_info = json.dumps(c_video_info, indent=4)
					c_video_info = json.loads(c_video_info)
					sw = 1
					all_information(sw,c_video_info)
				except:
					pass
				calc += 1
			except:
				print("There is {} videos on channel".format(calc))
				break


def json_parser(result):

	json_string = json.dumps(result, indent=4)
	json_string = json.loads(json_string)

	try:
		p_info = (json_string['pageInfo'])
		to_result = (p_info['totalResults'])
		re_pr_page = (p_info['resultsPerPage'])
		page_info = ("Total Results: {}   Results Per Page: {}".format(to_result,re_pr_page))
		print(page_info)

		page_results = (result['items'])
	except:
		return

	for i in page_results:
		sw = 0
		all_information(sw,i)


def search_with_keyword(max_page,search_word):
	number_of_page = 1
	nextPageToken = ""

	while True:
		print("\nNumber of search page: {}".format(number_of_page))
		api = Api(api_key=API_KEY)
		page_results = api.search_by_keywords(q=search_word, search_type=["video"],page_token=nextPageToken, return_json=True, limit=25)

		json_parser(page_results)
		page_string = json.dumps(page_results, indent=4)
		page_string = json.loads(page_string)
		nextPageToken = (page_string['nextPageToken'])

		if number_of_page == max_page:
			print("Scanning process finished... Number of last page: {}".format(number_of_page))
			return
		number_of_page += 1


def crawler_starter():

	# Searcher with keyword
	if SEARCH_MODE == True:
		search_with_keyword(MAX_PAGE,SEARCH_WORD)

	# Search with channel ID
	if (CHANNEL_MODE == True) and (CHANNEL_LIST != []):
		for ch in CHANNEL_LIST:
			search_with_channel_id(str(ch))


if __name__ == "__main__":
	config_check()
	create_folders()
	crawler_starter()

