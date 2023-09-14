"""
Написать программу, которая считывает список из 10 URL-
адресов и одновременно загружает данные с каждого
адреса.
После загрузки данных нужно записать их в отдельные
файлы.
Используйте потоки.
"""

import threading
import requests

urls = [
    "https://www.google.ru/",
    "https://gb.ru/",
    "https://ya.ru/",
    "https://www.python.org/",
    "https://habr.com/ru/all/",
]


def read_url(url: str):
    response = requests.get(url)
    filename = (
        "uploads/thread_"
        + url.replace("https://", "").replace(".", "").replace("/", "_")
        + ".html"
    )
    with open(filename, "w", encoding="utf-8") as file:
        file.write(response.text[:50])
        print(f"{url} download")


threads = []
for url in urls:
    t = threading.Thread(target=read_url, args=[url])
    threads.append(t)
    t.start()

for t in threads:
    t.join()
