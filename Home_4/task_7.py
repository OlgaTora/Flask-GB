"""
Напишите программу на Python, которая будет находить
сумму элементов массива из 1 000 000 целых чисел.
Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
Массив должен быть заполнен случайными целыми числами
от 1 до 100.
При решении задачи нужно использовать многопоточность,
многопроцессорность и асинхронность. Подсчет запускать на срезы.
В каждом решении нужно вывести время выполнения
вычислений.
"""

import asyncio
import random
import time
import multiprocessing
import threading

ELEM = 1_000_000
MIN_NUM = 1
MAX_NUM = 100
PARTS = 5

sum_threads = 0
sum_proc = multiprocessing.Value("i", 0)
sum_async = 0


def get_random_array() -> list[list[int]]:
    part_arr = []
    for i in range(PARTS):
        arr = [
            random.randint(MIN_NUM, MAX_NUM) for _ in range(1, int(ELEM / PARTS) + 1)
        ]
        part_arr.append(arr)
    return part_arr


def get_sum_threads(arr: list[int]):
    global sum_threads
    for i in arr:
        sum_threads += i
    print(
        f"Summa of part: {sum_threads}, counts in {time.time() - start_time:.4f} seconds"
    )


def get_sum_proc(arr: list[int], summ):
    for i in arr:
        with summ.get_lock():
            summ.value += i
    print(
        f"Summa of part: {summ.value}, counts in {time.time() - start_time:.4f} seconds"
    )


async def get_sum_async(arr: list[int]):
    global sum_async
    for i in arr:
        sum_async += i
    print(f"{sum_async} counts in {time.time() - start_time:.4f} seconds")


async def main():
    tasks = [asyncio.create_task(get_sum_async(arr)) for arr in arrays]
    await asyncio.gather(*tasks)


arrays = get_random_array()
threads = []
processes = []

if __name__ == "__main__":
    start_time = time.time()
    for arr in arrays:
        t = threading.Thread(target=get_sum_threads, args=[arr])
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    print(
        f"Threads:\n"
        f"Summa of 1_000_000 elements: {sum_threads}, counts in {time.time() - start_time:.4f} seconds"
    )
    print("___________________________")

    start_time = time.time()
    for arr in arrays:
        p = multiprocessing.Process(target=get_sum_proc, args=(arr, sum_proc))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print(
        f"Multiprocessing:\n"
        f"Summa of 1_000_000 elements: {sum_proc.value}, counts in {time.time() - start_time:.4f} seconds"
    )
    print("___________________________")

    start_time = time.time()
    asyncio.run(main())
    print(
        f"Async\n"
        f"Summa of 1_000_000 elements: {sum_async}, counts in {time.time() - start_time:.4f} seconds"
    )
