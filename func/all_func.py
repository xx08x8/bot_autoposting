import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List
from config.config import (
    BLOCKED_USERS_FILE, 
    DELAY_HOURS, 
    LOG_FILE, 
    ADMIN_ID
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, "w", "utf-8"), logging.StreamHandler()],
)


user_last_post_time: Dict[int, datetime] = {}


async def save_posts(posts: List[dict], file_path: str):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)


# Функция для загрузки постов из json
async def load_posts(file_path: str) -> List[dict]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# Функция блокировки пользователя
async def block_user(user_id: int):
    blocked_users = load_posts(BLOCKED_USERS_FILE)
    if user_id not in blocked_users:
        blocked_users.append(user_id)
        await save_posts(blocked_users, BLOCKED_USERS_FILE)
        logging.info(f"Пользователь <code>{user_id}</code> заблокирован.")


# Функция разблокировки пользователя
async def unblock_user(user_id: int):
    blocked_users = load_posts(BLOCKED_USERS_FILE)
    if user_id in blocked_users:
        blocked_users.remove(user_id)
        await save_posts(blocked_users, BLOCKED_USERS_FILE)
        logging.info(f"Пользователь <code>{user_id}</code> разблокирован.")


# Функция проверки блокировки пользователя
async def is_user_blocked(user_id: int) -> bool:
    blocked_users = await load_posts(BLOCKED_USERS_FILE)
    return user_id in blocked_users


# Функция для проверки задержки
async def can_post(user_id: int) -> bool:
    if user_id == ADMIN_ID:
        return True, 0, 0
    last_time = user_last_post_time.get(user_id)
    if last_time:
        delta = datetime.now() - last_time
        if delta < timedelta(hours=DELAY_HOURS):
            remaining = timedelta(hours=DELAY_HOURS) - delta
            minutes = remaining.seconds // 60
            seconds = remaining.seconds % 60
            return False, minutes, seconds
    return True, 0, 0