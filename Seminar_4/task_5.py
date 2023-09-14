"""
�Создать программу, которая будет производить подсчет
количества слов в каждом файле в указанной директории и
выводить результаты в консоль. Используйте процессы.
"""

import multiprocessing
import time
from pathlib import Path

DIR_PATH = Path(".")
counter = multiprocessing.Value("i", 0)


def count_words(file_path, cnt):
    with open(file_path, "r", encoding="utf-8") as file:
        with cnt.get_lock():
            cnt.value += len(file.read().split())
    print(
        f"Now counter: {cnt.value:_} words. Count in {time.time() - start_time:.4f} seconds"
    )


start_time = time.time()

if __name__ == "__main__":
    processes = []
    file_paths = [file_path for file_path in DIR_PATH.iterdir() if file_path.is_file()]
    for file_path in file_paths:
        process = multiprocessing.Process(target=count_words, args=(file_path, counter))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(
        f"Final counter: {counter.value:_} words. Count in {time.time() - start_time:.4f} seconds"
    )
