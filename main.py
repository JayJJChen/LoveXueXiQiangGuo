import os

from utils.bot import Bot

adb_path = os.path.join("platform-tools", "adb.exe")
temp_path = "tmp"

bot = Bot(adb_path=adb_path, temp_path=temp_path, sleep_sec=2)

if __name__ == "__main__":
    for _ in range(6):
        bot.take_exam()
