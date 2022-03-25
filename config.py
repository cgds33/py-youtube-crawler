####### GOOGLE YOUTUBE V3 API KEY
API_KEY = ""                  # You must fill it for the crawler to work (str)

####### SEARCH ENGINE
SEARCH_MODE = True            # Active search engine (bool)
SEARCH_WORD = "example"       # Search word (str)
MAX_PAGE = 60                 # Max research page (int)

####### CHANNEL CRAWL ENGINE
CHANNEL_MODE = False           # Active channel crawl engine (bool)
CHANNEL_LIST = []             # Target channel ID list (list)

####### CRAWLER SETTINGS 
DOWNLOAD_THUMBNAILS = True    # Download thumnails (bool)
DOWNLOAD_VIDEOS = True        # Download videos (bool)
LOGGING = True                # Detailed logging (bool)

####### CRAWLER FILTER 
TARGET_WORD = []              # Crawl by keyword in video title (list)

####### SAVE FOLDERS
VIDEO_DIR = './videos/'       # Downloaded videos folder (str)
LOG_DIR = "./logs/"           # Logger folder (str)
THUMB_DIR = "./thumbnails/"   # Downloaded thumbnails folder (str)
