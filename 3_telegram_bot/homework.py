"""This is a Telegram bot which will notify you about your homework status."""

import logging
import os
import sys
import time
from http import HTTPStatus
from json import JSONDecodeError
from logging.handlers import RotatingFileHandler

import requests
import telegram
from dotenv import load_dotenv

import exceptions

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
TWO_WEEKS_TIMESTAMP = 1209600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS: dict[str, str] = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
HOMEWORK_VERDICTS: dict[str, str] = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
s_handler = logging.StreamHandler()
r_handler = RotatingFileHandler('main.log', maxBytes=50000000, backupCount=5)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
r_handler.setFormatter(formatter)
logger.addHandler(s_handler)
logger.addHandler(r_handler)


def check_tokens() -> bool:
    """Initializing required environment variables for correct work."""
    if TELEGRAM_CHAT_ID is None or TELEGRAM_CHAT_ID == '':
        logger.critical(
            f"Missing required environment variable: {'TELEGRAM_CHAT_ID'}"
        )
    if PRACTICUM_TOKEN is None or PRACTICUM_TOKEN == '':
        logger.critical(
            f"Missing required environment variable: {'PRACTICUM_TOKEN'}"
        )
    if TELEGRAM_TOKEN is None or TELEGRAM_TOKEN == '':
        logger.critical(
            f"Missing required environment variable: {'TELEGRAM_TOKEN'}"
        )
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def send_message(bot: telegram.Bot, message: str) -> None:
    """Send message to telegram chat."""
    logger.info('Trying to send message...')
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logger.debug(f'Message successfully sent: \n{message}')
    except Exception as error:
        logger.error(error)


def get_api_answer(timestamp: int) -> dict:
    """Get API response."""
    timestamp: int = {'from_date': timestamp}
    try:
        homework_statuses = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params=timestamp)
    except requests.RequestException as e:
        logger.error(e)
    if homework_statuses.status_code != HTTPStatus.OK:
        raise exceptions.APIDoNotResponde(
            f"Endpoint {ENDPOINT} doesn't work \n"
            f'API response code: {homework_statuses.status_code}'
        )
    try:
        return homework_statuses.json()
    except JSONDecodeError:
        raise exceptions.JSONFormatException(
            "API response coudn't recieve JSON format"
        )


def check_response(response: dict) -> dict:
    """Check if API response is valid."""
    if 'current_date' not in response:
        raise TypeError("response key access error: 'current_date'")
    homeworks_list: int = response['current_date']
    if 'homeworks' not in response:
        raise TypeError("response key access error: 'homeworks'")
    homeworks_list: dict = response['homeworks']
    if homeworks_list is None:
        raise TypeError(
            'In API response there is no dict with homework projects'
        )
    if not homeworks_list:
        raise exceptions.APIResponseException(
            'There are no homework projects lately'
        )
    if not isinstance(homeworks_list, list):
        raise TypeError(
            'In API response homework projects are not represented as a list'
        )
    return homeworks_list


def parse_status(homework: dict) -> str:
    """Get homework status from API response."""
    if 'homework_name' not in homework:
        raise KeyError("homework key access error: 'homework_name'")
    homework_name: str = homework.get('homework_name')
    if 'status' not in homework:
        raise KeyError("homework key access error: 'homework_status'")
    homework_status: str = homework.get('status')
    if homework_status not in HOMEWORK_VERDICTS.keys():
        raise ValueError(f'Unknown homework status: {homework_status}')
    verdict: str = HOMEWORK_VERDICTS[homework_status]
    message: str = f'Изменился статус проверки работы "{homework_name}". {verdict}'
    logger.debug(message)
    return message


def main():
    """Main bot logic."""
    logger.info('Bot has started')
    if not check_tokens():
        sys.exit('The program will be forced to stop')
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp: int = int(time.time() - TWO_WEEKS_TIMESTAMP)
    previous_status = None
    previous_error = None
    while True:
        try:
            response: dict = get_api_answer(timestamp)
            timestamp = response.get('current_date', timestamp)
            homeworks: dict = check_response(response)
            homework_status = homeworks[0].get('status')
            if homework_status == previous_status:
                logger.debug('No status updates')
            else:
                previous_status = homework_status
                message = parse_status(homeworks[0])
                send_message(bot, message)
        except Exception as error:
            message: str = f'Program crash: {error}'
            if previous_error != str(error):
                logger.error(error)
                send_message(bot, message)
                previous_error: str = str(error)
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
