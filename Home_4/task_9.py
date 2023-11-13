"""
Написать программу, которая скачивает изображения с заданных URL-адресов и
сохраняет их на диск. Каждое изображение должно сохраняться в отдельном
файле, название которого соответствует названию изображения в URL-адресе.
�Например URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
�Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
�Программа должна иметь возможность задавать список URL-адресов через
аргументы командной строки.
�Программа должна выводить в консоль информацию о времени скачивания
каждого изображения и общем времени выполнения программы.
Добавлена возможность скачивать картинки с адресов, где сама картинка вшита внутри адреса.
Добавлена проверка на расширение картинок.
"""
from __future__ import annotations

import argparse
import asyncio
import time
import multiprocessing
import threading
import requests
import aiohttp

urls_lst = [
    "https://gb.ru/_nuxt/img/6c757d5.png",
    "https://gb.ru/",
    "https://static.eldorado.ru/photos/mv/Big/400103320bb.jpg",
    "https://sypalo.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fsergey-and-jane-sypalo.c53803b4.jpg&w=640&q=75",
    "https://img4.traektoria.ru/upload/trk_iblock_img/0aa/tr5hbho7v6crld3cbxnlkb6omg3aiaj2.jpg",
    "https://sun30-1.userapi.com/impg/utsP44UcvVdi8CkqeQT4-28ASVv4skT5pEYTzA/-m8i3127h-Y.jpg?size=604x243&quality"
    "=96&sign=241d86db6d4d600ebbfbd99baec0735b&c_uniq_tag=GQFmKBi_Dumds-ru5BZWbBBey_B1OvAvIpcobdnEXLs&type=album",
    "https://cdnn21.img.ria.ru/images/07e7/09/0a/1895369908_0:0:3180:1789_640x0_80_0_0_d20b056e0afa24a0decfaa4ec01eaef9.jpg.webp",
]

extensions = ["png", "jpg", "jpeg", "pct", "pict", "bmp", "gif", "tiff"]


def get_filename(url: str) -> str | None:
    filename = None
    url_parts = url.split(".")
    for part in range(len(url_parts)):
        for ext in extensions:
            if url_parts[part].startswith(ext):
                name = url_parts[part - 1].split("/")[-1]
                filename = "uploads/" + name + "." + ext
    if filename is None:
        print(f"This URL {url} dont contain picture")
    return filename


def download_pic(url: str):
    start_time = time.time()
    response = requests.get(url)
    filename = get_filename(url)
    if filename:
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"{url} download in {time.time() - start_time:.4f} seconds")


async def a_download_pic(url: str):
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
            filename = get_filename(url)
            if filename:
                with open(filename, "wb") as file:
                    file.write(content)
                print(f"{url} download in {time.time() - start_time:.4f} seconds")


async def async_download():
    start_time = time.time()
    tasks = [asyncio.create_task(a_download_pic(url)) for url in urls_lst]
    await asyncio.gather(*tasks)
    print(f"Download async finished in {time.time() - start_time:.4f} seconds")


def multiproc_download():
    processes = []
    start_time = time.time()
    for url in urls_lst:
        process = multiprocessing.Process(target=download_pic, args=([url]))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    print(
        f"Download multiprocessing finished in {time.time() - start_time:.4f} seconds"
    )


def threads_download():
    threads = []
    start_time = time.time()
    for url in urls_lst:
        thread = threading.Thread(target=download_pic, args=[url])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print(f"Download threading finished in {time.time() - start_time:.4f} seconds")


def parse():
    parser = argparse.ArgumentParser(
        prog="parser module", description="programm for download pictures"
    )
    parser.add_argument(
        "-u", "--url", help="url of picture", type=str, default=urls_lst
    )

    arguments = parser.parse_args()
    urls = arguments.url
    return urls


if __name__ == "__main__":
    parse()
    multiproc_download()
    print("---------------------------")
    threads_download()
    print("---------------------------")
    asyncio.run(async_download())
