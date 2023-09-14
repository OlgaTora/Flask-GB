"""
Создать программу, которая будет производить подсчет
количества слов в каждом файле в указанной директории и
выводить результаты в консоль. Используйте потоки.
"""
import threading
import time
from pathlib import Path

DIR_PATH = Path(".")
counter = 0


def count_words(file_path):
    global counter
    with open(file_path, "r", encoding="utf-8") as file:
        counter += len(file.read().split())
        print(f"Now {counter} words. Count in {time.time() - start_time:.4f} seconds")


start_time = time.time()

if __name__ == "__main__":
    threads = []
    file_paths = [file_path for file_path in DIR_PATH.iterdir() if file_path.is_file()]
    for file_path in file_paths:
        t = threading.Thread(target=count_words, args=[file_path])
        threads.append(t)
        t.start()
        time.sleep(0.5)

    for t in threads:
        t.join()

    print(f"Final counter: {counter} words.")
