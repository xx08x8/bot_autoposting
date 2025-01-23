import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
POSTS_FILE = "data_json/posts.json"
PENDING_POSTS_FILE = "data_json/pending_posts.json"
BLOCKED_USERS_FILE = "data_json/blocked_users.json"
IMAGE_FOLDER = "images"
DELAY_HOURS = 1
LOG_FILE = "logs/bot.log"
POSTS_PER_PAGE = 1
ADMIN_ID = 
CHANNEL_ID = 
