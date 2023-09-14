"""
Написать программу, которая считывает список из 10 URL-
адресов и одновременно загружает данные с каждого
адреса. После загрузки данных нужно записать их в отдельные
файлы. Используйте асинхронный подход.
"""

import asyncio
import aiohttp

urls = [
    "https://www.google.ru/",
    "https://gb.ru/",
    "https://ya.ru/",
    "https://www.python.org/",
    "https://habr.com/ru/all/",
]


async def read_url(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            filename = (
                "uploads/acync_"
                + url.replace("https://", "").replace(".", "").replace("/", "_")
                + ".html"
            )
            with open(filename, "w", encoding="utf-8") as file:
                file.write(text[:50])
                print(f"{url} download")


async def main():
    tasks = []
    for url in urls:
        task = asyncio.create_task(read_url(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
