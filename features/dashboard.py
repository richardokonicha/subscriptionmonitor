from config import bot, wcapi, scheduler, channel_name
import re
import database as db
import datetime
from config import join_channel_markup
import telebot
from telebot import types


def dashboard(message):
    tasks = scheduler.get_jobs()
    message_text = "There are no task"
    if tasks:
        message_text = "The scheduled tasks are:\n\n"
        for task in tasks:
            message_text += f"- {task.name} -{task.id}\n{task.next_run_time.strftime('%A %d %B %Y')}\n"

    bot.send_message(message.chat.id, message_text)
