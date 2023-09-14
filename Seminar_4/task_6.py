"""
Создать программу, которая будет производить подсчет
количества слов в каждом файле в указанной директории и
выводить результаты в консоль. Используйте асинхронный подход.
"""

import asyncio
import time
from pathlib import Path

DIR_PATH = Path(".")
counter = 0


async def count_words(file_path):
    global counter
    with open(file_path, "r", encoding="utf-8") as file:
        contents = file.read().split()
        counter += len(contents)
    print(f"Now {counter} words. Count in {time.time() - start_time:.4f} seconds")


start_time = time.time()


async def main():
    file_paths = [file_path for file_path in DIR_PATH.iterdir() if file_path.is_file()]
    tasks = [asyncio.create_task(count_words(file_path)) for file_path in file_paths]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
    print(f"Final counter: {counter} words.")
