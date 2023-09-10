"""
Написать программу, которая считывает список из 10 URL-
адресов и одновременно загружает данные с каждого
адреса. После загрузки данных нужно записать их в отдельные
файлы. Используйте процессы.
"""
import multiprocessing
import requests

urls = ['https://www.google.ru/',
        'https://gb.ru/',
        'https://ya.ru/',
        'https://www.python.org/',
        'https://habr.com/ru/all/',
        ]


def read_url(url: str):
    response = requests.get(url)
    filename = ('uploads/process_' +
                url.replace('https://', '').
                replace('.', '').
                replace('/', '_') + '.html')
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(response.text[:50])
        print(f'{url} download')


processes = []

if __name__ == '__main__':
    for url in urls:
        process = multiprocessing.Process(target=read_url, args=[url])
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
